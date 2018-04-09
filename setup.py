from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os
import io

import assemfuzz

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["--cov", "assemfuzz"]
        self.test_suite = True

    def run_tests(self):
        import pytest
        import pylint
        errcode = pylint.run_pylint()
        if errcode:
            sys.exit(errcode)
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)
        

setup(
    name='assemfuzz',
    version=assemfuzz.__version__,
    url='http://github.com/achermannagement/assemfuzz',
    license='GPLv3',
    #tests_require=['pytest', 'pytest-pylint', 'pytest-cov'],
    install_requires=['pytest', 'pytest-pylint', 'pytest-cov'],
    cmdclass={'test': PyTest},
    author='Joshua Achermann',
    author_email='joshua.achermann@gmail.com',
    description='A package for fuzzing Hack assemblers from the Nand2Tetris course',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['contrib','docs','tests']),
    include_package_data=True,
    platforms='any',
    test_suite='assemfuzz.test.test_assemfuzz',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Topic :: Education',
        ],
    keywords='education development testing',
    extras_require={
    #'test': ['pytest'],
    },
)