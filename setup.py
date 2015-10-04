from setuptools import setup, find_packages
import sys
from setuptools.command.test import test as TestCommand

#https://pytest.org/latest/goodpractises.html
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(name='ampcountpy',
    version='0.1',
    description='Some python functions to count the expected amplifications for genomic regions given a set of primer binding locations for a multiple displacement amplification reaction.',
    url='http://github.com/sherrillmix/ampCountPy',
    author='Scott Sherrill-Mix',
    author_email='shescott@upenn.edu',
    license='GPL-2',
    packages=find_packages(),
    zip_safe=True,
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
)
