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
import hack

class RandomFuzzer():
    """This fuzzer prepares a valid code for the language spec provided.
It will be filled with random valid instructions for the specification language.
The output then can be fed into the fuzzed program to find problems."""
    def __init__(self, file_name, lang_spec):
        self.lang_spec = lang_spec
        self.length = hack.MAX_SIZE
        self.contents = []
        self.file_name = file_name
        for _ in range(self.length):
            self.contents.append(self.lang_spec.make_random_instruction())
        self.contents = "\n".join(self.contents)
        self.file = open(self.file_name, "wb")

    def out_file(self):
        """Returns the name of the fuzzer produced file."""
        return self.file_name

    def prepare_file(self):
        """Once the fuzzer has generated the code, this function writes it to the file"""
        self.file.write(self.contents.encode("utf-8"))

    def log(self):
        """Returns some debugging information"""
        return "RandomFuzzer file: {} length: {}".format(self.file,
                                                         self.length)
