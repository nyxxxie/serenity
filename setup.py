#!/usr/bin/env python
from setuptools import setup
import unittest

def spade_test_suite():
    test_loader = unittest.TestLoader()
    test_squite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

setup(name='spade',
      version='0.1',
      description='File format reverse engineering tool.',
      url='https://github.com/nyxxxie/spade',
      author='Nyxxie et al.',
      author_email='nyxxxxie@gmail.com',
      license='GNU GPL v3',
      test_squite='setup.spade_test_suite',
      packages=['spade'],
      zip_safe=False)
