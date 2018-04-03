"""
handles the fuzzer and programs to be fuzzed
this handler is designed to input a known bad input and tests the program
fails gracefully with a helpful message

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
from handler import Handler, program_had_error
import randombadfuzzer

class FailHandler(Handler):
    """The handler takes in the fuzzer and uses it to generate the input files,
runs the fuzzed program against the reference program and compares the results.
It also does cleanup."""

    def __init__(self, test_input, test_output, lang_spec, data):
        super().__init__(
            test_input, test_output, lang_spec, data)
        self.my_cond = data["conds"][0]
        self.their_cond = data["conds"][1]

    def prepare_fuzzer(self):
        return randombadfuzzer.RandomBadFuzzer(self.test_input, self.lang_spec)

    def run_test(self, my_result, their_result):
        res = False
        self.talk("My error message: {}".format(my_result.stderr))
        self.talk("Their error message: {}".format(their_result.stderr))
        if self.my_cond and self.their_cond:
            res = self.my_cond(my_result.stderr) == self.their_cond(their_result.stderr)
        else:
            res = program_had_error(my_result) and program_had_error(their_result)
        return res
