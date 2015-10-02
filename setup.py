from setuptools import setup, find_packages

setup(name='ampcountpy',
    version='0.1',
    description='Some python functions to count the expected amplifications for genomic regions given a set of primer binding locations for a multiple displacement amplification reaction.',
    url='http://github.com/sherrillmix/ampCountPy',
    author='Scott Sherrill-Mix',
    author_email='shescott@upenn.edu',
    license='GPL-2',
    packages=find_packages(),
    zip_safe=True
)
