"""
Creates a file according to a language specification.

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

class Fuzzer(ABC):
    """Base class for fuzzer (produces files for fuzzing)"""
    def __init__(self, file_name, lang_spec):
        self.lang_spec = lang_spec
        self.file_name = file_name
        self.contents = [] # gets turned into a string tho
        self.file = None

    @abstractmethod
    def prepare_file(self):
        """Prepare a fuzzing input file for testing"""
        pass

    @abstractmethod
    def log(self):
        """Returns some debugging information"""
        pass

    @abstractmethod
    def write_file(self):
        """Once the fuzzer has generated the code, this function writes it to the file"""
        pass
