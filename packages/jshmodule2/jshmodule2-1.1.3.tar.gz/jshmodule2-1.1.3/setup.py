from setuptools import setup, find_packages

setup(
    name='jshmodule2',
    version='1.1.3',
    packages=find_packages(exclude=[]),
    package_data={
        'jshmodule2': ['data/*'],
    },
    install_requires=[
        'geopandas',
        'shapely',
        'requests',
        'pyproj'
    ],
)