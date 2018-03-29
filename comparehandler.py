"""
handles the fuzzer and programs to be fuzzed
this handler is designed to fuzz the program with known valid inputs and compare
the generated output to a reference program

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
import filecmp

from definitions import MY_FOLDER, THEIR_FOLDER

from handler import Handler
import randomfuzzer

class CompareHandler(Handler):
    """The handler takes in the fuzzer and uses it to generate the input files,
runs the fuzzed program against the reference program and compares the results.
It also does cleanup."""

    def prepare_fuzzer(self):
        return randomfuzzer.RandomFuzzer(self.test_input, self.lang_spec)        

    def run_test(self, my_result, their_result):
        """Compares the output of the generated files and updates the result field accordingly."""
        res = False        
        if my_result and their_result and filecmp.cmp(os.path.join(MY_FOLDER, self.test_output),
                       os.path.join(THEIR_FOLDER, self.test_output),
                       shallow=False):
            res = True
        return res
