"""
Creates a random valid Hack assembly file.

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
from assemfuzz.fuzzer import Fuzzer
import assemfuzz.hack as hack

class RandomFuzzer(Fuzzer):
    """This fuzzer prepares a valid code for the language spec provided.
It will be filled with random valid instructions for the specification language.
The output then can be fed into the fuzzed program to find problems."""
    def __init__(self, file_name, lang_spec):
        super().__init__(file_name, lang_spec)
        self.length = hack.MAX_SIZE

    def prepare_file(self):
        for _ in range(self.length):
            self.contents.append(self.lang_spec.make_random_instruction())
        self.contents = "\n".join(self.contents)

    def log(self):
        return "RandomFuzzer file: {} length: {}".format(self.file,
                                                         self.length)

    def write_file(self):
        self.file = open(self.file_name, "wb")
        self.file.write(self.contents.encode("utf-8"))
