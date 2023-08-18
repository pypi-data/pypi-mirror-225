#!/usr/bin/env python
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

_description = (
    "Python transformation library inspired by Stephan Saalfeld's "
    "MPICBG Java Library."
)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import shlex
        import pytest
        self.pytest_args += " --cov=mpyicbg --cov-report html "\
                            "--junitxml=test-reports/test.xml"

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


with open('test_requirements.txt', 'r') as f:
    test_required = f.read().splitlines()

with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()

setup(name='mpyicbg',
      description=_description,
      author='Russel Torres',
      author_email='RussTorres@gmail.com',
      setup_requires=['setuptools_scm'],
      use_scm_version=True,
      url='https://github.com/RussTorres/m-py-icbg',
      packages=find_packages(),
      install_requires=required,
      tests_require=test_required,
      cmdclass={'test': PyTest},)
