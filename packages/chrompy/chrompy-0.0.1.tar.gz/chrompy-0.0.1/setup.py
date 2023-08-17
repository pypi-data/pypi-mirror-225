import unittest

from setuptools import setup, find_packages


def testsuite():
    return unittest.TestLoader().discover('tests', pattern='test_*.py')


setup(
    name='chrompy',
    version='0.0.1',
    packages=[_ for _ in find_packages() if _ != "tests"],
    url='https://github.com/Platob/Chrompy.git',
    license='Apache License 2.0',
    author='Fillot Nicolas',
    author_email='nfillot.pro@gmail.com',
    description='Chrome driver fully automated',
    long_description="Chrome driver fully automated",
)
