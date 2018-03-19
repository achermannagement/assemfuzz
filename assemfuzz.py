"""
generates long strings of valid hack assembly and compares against a
reference assembler

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
import argparse
import subprocess

import definitions
import hack
import handler
import randomfuzzer

def my_assembler(output_path):
    """This is the function we pass into the handler to run our program
    you will need to edit the run string in the definitions file to fit"""
    return subprocess.run(definitions.RUN_STRING, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, shell=True)

def their_assembler(output_path, windows=False):
    """This is the function to run the Nand2Tetris reference assembler"""
    if not windows:
        result = subprocess.run(definitions.COMP_RUN_STRING_LINUX,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, shell=True)
    else:
        result = subprocess.run(definitions.COMP_RUN_STRING_WINDOWS,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, shell=True)
    return result

def main():
    """Uses the default handler and random fuzzer to run multiple
    fuzzing rounds on the assembler defined in defintions.py
    """
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("lines",
                        help="rough # of lines of assembly code to fuzz", type=int)
    args = parser.parse_args()
    # begin the program
    passed = True
    on_windows = False
    # detect whether the platform I am running on is Windows
    if os.name == 'nt':
        on_windows = True
    for i in range((args.lines // hack.MAX_SIZE)+1):
        lang_spec = hack.Hack()
        fuzzer = randomfuzzer.RandomFuzzer(definitions.PATH_TO_TEST_FILE, lang_spec)
        handler_inst = handler.Handler(fuzzer, definitions.PATH_TO_TEST_OUTPUT,
                                       my_assembler, their_assembler, on_windows)
        print("Test {}: Passed? {}".format(i, handler_inst.success()))
        if not handler_inst.success():
            passed = False
    print("PASSED ALL TESTS? " + str(passed))

if __name__ == "__main__":
    print("assem-fuzz  Copyright (C) 2017  Joshua Achermann")
    print("This program comes with ABSOLUTELY NO WARRANTY")
    print("This is free software, and you are welcome to redistribute it "
          "under certain conditions")
    print("Please read LICENSE file for more information")
    main()
