from setuptools import setup, find_packages

setup(
    name='localcrypto',
    version='0.0.1',
    packages=find_packages(
        where='localcrypto',
    ),
    install_requires=[
        'requests',
        'importlib; python_version == "3.7.6"',
    ],
)