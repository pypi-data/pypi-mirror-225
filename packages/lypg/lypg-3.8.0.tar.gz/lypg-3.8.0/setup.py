from setuptools import setup, find_packages

setup(
    name='lypg',
    version='3.8.0',
    packages=find_packages(),
    package_data={
        'lypg': ['*.so']
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
    ],
)

