from setuptools import setup


def read_requirements_txt():
    lines = open('requirements.txt', 'r').readlines()
    return [l.strip() for l in lines]


setup(
    name='glue_ray_etl',
    version='0.0.1',
    packages=['glue_ray_etl', 'glue_ray_etl.io'],
    url='https://github.com/archiba/glue-ray-etl',
    license='',
    author='archiba',
    author_email='',
    description='',
    install_requires=read_requirements_txt()
)
