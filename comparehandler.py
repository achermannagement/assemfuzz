"""
handles the fuzzer and programs to be fuzzed

Copyright (C) 2017  Joshua Achermann

  This file is part of assem-fuzz.

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
import shutil
import filecmp
import difflib

import definitions

class CompareHandler():
    """The handler takes in the fuzzer and uses it to generate the input files,
runs the fuzzed program against the reference program and compares the results.
It also does cleanup."""
    def __init__(self, fuzzer, test_output, program, ref_program, windows=False):
        self.result = False
        self.fuzzer = fuzzer
        self.program = program
        self.ref_program = ref_program
        self.test_output = test_output
        self.windows = windows
        # have fuzzer prepare input file
        self.fuzzer.prepare_file()
        self.clean()
        # copy to each directory
        shutil.copy(self.fuzzer.out_file(),
                    os.path.join(definitions.MY_FOLDER, self.fuzzer.out_file()))
        shutil.copy(self.fuzzer.out_file(),
                    os.path.join(definitions.THEIR_FOLDER, self.fuzzer.out_file()))

        # do my assembler
        self.program_under_test()

        # move result to folder
        os.rename(self.test_output, os.path.join(definitions.MY_FOLDER, self.test_output))

        # run the standard assembler
        self.reference_program()

        # need to compare files by contents
        self.compare_output()

    def program_under_test(self):
        """Runs the program function for the program under test"""
        result = self.program(None)
        self.check_result(result)

    def reference_program(self):
        """Runs the program function for the reference program"""
        result = self.ref_program(None, self.windows)
        self.check_result(result)

    def clean(self):
        """Clean test output."""
        if os.path.exists(os.path.join(definitions.MY_FOLDER, self.fuzzer.out_file())):
            os.remove(os.path.join(definitions.MY_FOLDER, self.fuzzer.out_file()))
        if os.path.exists(os.path.join(definitions.THEIR_FOLDER, self.fuzzer.out_file())):
            os.remove(os.path.join(definitions.THEIR_FOLDER, self.fuzzer.out_file()))
        if os.path.exists(os.path.join(definitions.MY_FOLDER, self.test_output)):
            os.remove(os.path.join(definitions.MY_FOLDER, self.test_output))
        if os.path.exists(os.path.join(definitions.THEIR_FOLDER, self.test_output)):
            os.remove(os.path.join(definitions.THEIR_FOLDER, self.test_output))

    def check_result(self, result):
        """Check the result of the program execution."""
        if result.returncode != 0:
            print("Exception! @ " + self.fuzzer.log())
            except_type = str(result.stderr).split(":")[0][2:]
            print("Type: {}".format(except_type))
            raise Exception()

    def compare_output(self):
        """Compares the output of the generated files and updates the result field accordingly."""
        if filecmp.cmp(os.path.join(definitions.MY_FOLDER, self.test_output),
                       os.path.join(definitions.THEIR_FOLDER, self.test_output),
                       shallow=False):
            self.result = True
        else:
            my_result = open(os.path.join(definitions.MY_FOLDER, self.test_output), "r")
            their_result = open(os.path.join(definitions.THEIR_FOLDER, self.test_output), "r")
            diff = difflib.unified_diff(my_result.readlines(), their_result.readlines())
            diff_file = open(definitions.DIFF_FILE_NAME, "w")
            for line in diff:
                diff_file.write(line)

    def success(self):
        """Returns whether the test succeeded (generated files were identical)."""
        return self.result
