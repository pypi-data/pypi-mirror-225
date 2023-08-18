from typing import Optional, Any, Callable

import pandas
import numpy
import pyarrow
import ray
from ray.data import Dataset
from ray.data.datasource import BlockWritePathProvider


class HiveIO:
    @staticmethod
    def read_ese_hive_parquet(root_dir):
        partition = ray.data.datasource.partitioning.Partitioning(
            "dir", base_dir=root_dir
        )

        df_blocks = ray.data.read_parquet(
            root_dir,
            dataset_kwargs={'partitioning': partition}
        )
        return df_blocks

    @staticmethod
    @ray.remote
    def _read_df_block(data_path, partition_keys: dict[str, Any], load_partition_keys: bool = False):
        try:
            df = pandas.read_parquet(data_path, partitioning=None)
            if not load_partition_keys:
                return df
            df_length = len(df)
            for partition_key, partition_value in partition_keys.items():
                df[partition_key] = [partition_value] * df_length
            return df
        except:
            return pandas.DataFrame()

    @staticmethod
    def read_hive_parquet(root_dir: str,
                          keys: list[dict[str, Any]],
                          key_formatters: Optional[dict[str, Callable[[Any], str]]] = None,
                          path_separator: str = '/',
                          load_partition_keys: bool = False):
        pandas_df_refs = []
        for set_of_key in keys:
            path = HiveIO._build_hive_data_ref(root_dir, set_of_key, key_formatters, path_separator)
            pandas_df_refs.append(HiveIO._read_df_block.remote(path, set_of_key, load_partition_keys))
        return ray.data.from_pandas_refs(pandas_df_refs)

    @staticmethod
    def _format_root_str(base_path: str, path_separator: str):
        root = base_path
        while root.endswith(path_separator):
            root = root[:-1]
        return root

    @staticmethod
    def _build_hive_data_ref(root_dir: str, keys: dict[str, Any],
                             key_formatters: Optional[dict[str, Callable[[Any], str]]] = None,
                             path_separator: str = "/"):
        root_dir = HiveIO._format_root_str(root_dir, path_separator)
        _key_formatters = {}
        for key in keys:
            if key_formatters is not None and key in key_formatters.keys():
                _key_formatters[key] = key_formatters[key]
            else:
                _key_formatters[key] = str
        suffixes = []
        for key in keys:
            suffixes.append(f"{key}={_key_formatters[key](keys[key])}")
        return path_separator.join([root_dir] + suffixes)

    @staticmethod
    def _execution_status_wrapper(fn):
        def wrapped_function(*args):
            try:
                fn(*args)
                return {'status': numpy.array([True])}
            except:
                return {'status': numpy.array([False])}

        return wrapped_function

    @staticmethod
    def to_hive_parquet(dataset: Dataset, path: str, partition_cols: list[str], **kwargs: dict[str, Any]):
        writer_blocks = dataset.map_batches(
            HiveIO._execution_status_wrapper(
                lambda df: df.to_parquet(
                    path=path,
                    engine='pyarrow',
                    partition_cols=partition_cols,
                    **kwargs
                )
            ),
            batch_format='pandas'
        )
        return writer_blocks.fully_executed()


class HiveLikeBlockWritePathProvider(BlockWritePathProvider):
    def __init__(self, hive_keys: list[str], key_formatters: Optional[dict[Any, Callable[[Any], str]]] = None,
                 path_separator: str = '/',
                 filename: str = 'data.parquet',
                 add_dataset_uuid_suffix: bool = False):
        self.hive_keys = hive_keys

        self.key_formatters = key_formatters
        self.path_separator = path_separator
        self.filename = filename
        self.add_dataset_uuid_suffix = add_dataset_uuid_suffix

    def _get_write_path_for_block(
            self,
            base_path: str,
            *,
            filesystem: Optional["pyarrow.fs.FileSystem"] = None,
            dataset_uuid: Optional[str] = None,
            block: pandas.DataFrame = None,
            block_index: Optional[int] = None,
            file_format: Optional[str] = None,
    ) -> str:
        base_path = self._format_root_str(base_path)
        suffixes: list[str] = []

        for key in self.hive_keys:
            assert key in block.columns, f"{key} is not found in dataframe"
            assert (block[key] == block[key].iloc[0]).all(), f"{key} is not unique over the block"

        if self.add_dataset_uuid_suffix:
            suffixes.append(dataset_uuid)
        keys = {key: block[key].iloc[0] for key in self.hive_keys}
        return build_hive_data_ref(base_path, keys, self.key_formatters, self.path_separator)
