"""
setup file for assemfuzz

Copyright (C) 2017  Joshua Achermann

assem-fuzz is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

email: joshua.achermann@gmail.com
"""
import os
import sys

from distutils.command.clean import clean
from setuptools import setup, find_packages
from setuptools import Command

import assemfuzz.common

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'README.md')) as readme:
    LONG_DESCRIPTION = readme.read()

class MyClean(clean):
    """Extending the setup.py clean command"""
    def run(self):
        super().run()
        assemfuzz.common.clean_testbench()

class PrepareCommand(Command):
    """This command prepares the fuzzing platform for use"""
    description = "Prepares the fuzzing platform for use"
    user_options = [
        ('path=', None, 'Specify the path to the Nand2Tetris zip file'),
        ('test=', None, 'Prepare for testing'),
    ]
    def initialize_options(self):
        """Set initial option values"""
        self.path = None
        self.test = False
    def finalize_options(self):
        """Check final option values"""
        if self.path is None:
            print("Please provide a path")
            sys.exit(1)
    def run(self):
        """Run the prepare command"""
        assemfuzz.common.make_folders()
        if self.test:
            assemfuzz.common.extract_their2_toolchain(self.path)
        assemfuzz.common.extract_their_toolchain(self.path)

setup(
    name='assemfuzz',
    version=assemfuzz.__version__,
    url='http://github.com/achermannagement/assemfuzz',
    license='GPLv3',
    install_requires=['setuptools'],
    setup_requires=['tox', 'pytest', 'pytest-pylint', 'pytest-cov'],
    #tests_require=['tox', 'pytest', 'pytest-pylint', 'pytest-cov'],
    cmdclass={'prepare': PrepareCommand, 'clean':MyClean},
    author='Joshua Achermann',
    author_email='joshua.achermann@gmail.com',
    description='A package for fuzzing Hack assemblers from the Nand2Tetris course',
    long_description=LONG_DESCRIPTION,
    #long_description_content_type='text/markdown',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    platforms='any',
    test_suite='assemfuzz.tests',
    classifiers=[
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
)
