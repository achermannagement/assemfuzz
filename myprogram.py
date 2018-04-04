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

import subprocess

from definitions import MY_FOLDER

PATH_TO_ASSEMBLER = "Assembler"
RUN_STRING = "java -cp {} {} {}"

def my_cond(err):
    """extract error line from my error message"""
    return int(err.split()[4][:-1])

# these specify the running of the programs
def my_assembler(input_path):
    """This is the function we pass into the handler to run our program"""
    return subprocess.run(RUN_STRING.format(MY_FOLDER, PATH_TO_ASSEMBLER, input_path),
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, shell=True)
