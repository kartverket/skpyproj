from setuptools import setup

setup(     
    name='mypackage',
    author='Sveinung Himle',
    version='1.0',
    install_requires=[
        'laspy',
        'numpy',
        'progress',
        'pyproj',
    ],
    # ... more options/metadata
)