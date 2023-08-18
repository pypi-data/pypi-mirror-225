from pathlib import Path

import boto3

s3 = boto3.client('s3')


class FileWalker:
    @staticmethod
    def get_all_subdirectories_s3(bucket, prefix, delimiter):
        continuation_token = None
        suffixes = []
        while True:
            if continuation_token is None:
                res = s3.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                    Delimiter=delimiter,
                    MaxKeys=2
                )
            else:
                res = s3.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                    Delimiter=delimiter,
                    ContinuationToken=continuation_token
                )

            if res['KeyCount'] == 0:
                break
            for content in res['CommonPrefixes']:
                suffixes.append(content['Prefix'].replace(prefix, ''))

            # ContinuationTokenが渡されなかったらそこで終わり
            continuation_token = res.get('NextContinuationToken')
            if continuation_token is None:
                break
        return suffixes

    @staticmethod
    def get_all_files_s3(bucket, prefix):
        continuation_token = None
        suffixes = []
        while True:
            if continuation_token is None:
                res = s3.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                    MaxKeys=2
                )
            else:
                res = s3.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                    ContinuationToken=continuation_token
                )

            if res['KeyCount'] == 0:
                break
            for content in res['Contents']:
                suffixes.append(content['Prefix'].replace(prefix, ''))

            # ContinuationTokenが渡されなかったらそこで終わり
            continuation_token = res.get('NextContinuationToken')
            if continuation_token is None:
                break
        return suffixes

    @staticmethod
    def get_all_subdirectories_local(root_dir: str) -> list[str]:
        root_path = Path(root_dir)
        return [str(d.stem) for d in root_path.glob("*") if d.is_dir()]

    @staticmethod
    def get_all_files_local(root_dir: str) -> list[str]:
        root_path = Path(root_dir)
        return [str(f.name) for f in root_path.rglob("*") if f.is_file()]
