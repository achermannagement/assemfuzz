"""


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
#!/bin/python3

import os
import subprocess

from assemfuzz.definitions import MY_FOLDER

PATH_TO_ASSEMBLER = "Assembler"
RUN_STRING = "java -cp {} {} {}"

def my_cond(err):
    """extract error line from my error message"""
    return int(err.split()[4][:-1])

def convert_name(name):
    return "{}.hack".format(name[:-4])

# TODO fix this
# these specify the running of the programs
def my_assembler(input_path, on_windows=False):
    """This is the function we pass into the handler to run our program"""
    test_output = convert_name(input_path)
    result = subprocess.run(RUN_STRING.format(MY_FOLDER, PATH_TO_ASSEMBLER, input_path),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        os.rename(test_output, os.path.join(MY_FOLDER, test_output)) # never sure I need this?
    return result
