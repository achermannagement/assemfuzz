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
from abc import ABC, abstractmethod
import os
import shutil

from definitions import MY_FOLDER, THEIR_FOLDER

def program_had_error(result):
    """Helper function to detect errors"""
    return result.stderr != b""

class Handler(ABC):
    """A handler is in charge in running the fuzzer, testing the programs, checking results"""
    def __init__(self, test_input, test_output, lang_spec, data):
        self.data = data
        self.test_input = test_input
        self.test_output = test_output
        self.lang_spec = lang_spec
        self.fuzzer = self.prepare_fuzzer()
        self.success = False

    @abstractmethod
    def prepare_fuzzer(self):
        """Prepares the fuzzer for use"""
        pass

    @abstractmethod
    def run_test(self, my_result, their_result):
        """Once the results are obtained, success is determined in here"""
        pass

    def handle(self):
        """Perform the fuzz, handle the results"""
        self.clean()
        self.fuzzer.prepare_file()
        self.fuzzer.write_file()
        shutil.copy(self.test_input,
                    os.path.join(MY_FOLDER, self.test_input))
        shutil.copy(self.test_input,
                    os.path.join(THEIR_FOLDER, self.test_input))

        my_result = self.program_under_test()
        if not program_had_error(my_result):
            os.rename(self.test_output, os.path.join(MY_FOLDER, self.test_output))

        their_result = self.reference_program()

        #os.rename(self.test_output, os.path.join(THEIR_FOLDER, self.test_output))
        self.success = self.run_test(my_result, their_result)

        if self.success:
            self.talk("Test success")
            self.clean()
        else:
            self.talk("Test failed")
            self.log()

    def talk(self, msg):
        """Uses the talking stick to write to stdout without contention"""
        if self.data["log_tuple"][2] != None:
            self.data["log_tuple"][2].acquire()
            print(msg)
            self.data["log_tuple"][2].release()

    def clean(self):
        """Clean test output."""
        if os.path.exists(os.path.join(MY_FOLDER, self.test_input)):
            os.remove(os.path.join(MY_FOLDER, self.test_input))
        if os.path.exists(os.path.join(THEIR_FOLDER, self.test_input)):
            os.remove(os.path.join(THEIR_FOLDER, self.test_input))
        if os.path.exists(os.path.join(MY_FOLDER, self.test_output)):
            os.remove(os.path.join(MY_FOLDER, self.test_output))
        if os.path.exists(os.path.join(THEIR_FOLDER, self.test_output)):
            os.remove(os.path.join(THEIR_FOLDER, self.test_output))
        if os.path.exists(self.test_input):
            os.remove(self.test_input)
        if os.path.exists(os.path.join(self.test_output)):
            os.remove(os.path.join(self.test_output))

    def program_under_test(self):
        """Runs the program function for the program under test"""
        return self.data["programs"][0](self.test_input)

    def reference_program(self):
        """Runs the program function for the reference program"""
        return self.data["programs"][1](self.test_input, self.data["on_windows"])

    def log(self):
        """Logs a test failure in the error log."""
        self.data["log_tuple"][1].acquire()
        errlog = open(self.data["log_tuple"][0], "a")
        errlog.write("Test failure: {} ".format(self.test_input))
        self.data["log_tuple"][1].release()

    def check_success(self):
        """Returns whether the test succeeded"""
        return self.success
