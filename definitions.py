"""
definitions for the handler and fuzzer not relevant to the hack language

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

FILE_TITLE = "fuzz"
PATH_TO_TEST_FILE = FILE_TITLE + ".asm"
PATH_TO_TEST_OUTPUT = FILE_TITLE + ".hack"
PATH_TO_ASSEMBLER = "Assembler"
RUN_STRING = "java -cp mine {} {}".format(PATH_TO_ASSEMBLER
, PATH_TO_TEST_FILE)
COMP_RUN_STRING_WINDOWS = "theirs/Assembler.bat {}".format(
"theirs/" + PATH_TO_TEST_FILE)
COMP_RUN_STRING_LINUX = "theirs/Assembler.sh {}".format(
"theirs/" + PATH_TO_TEST_FILE)

SYMBOL_NAME_MIN_SIZE = 5
SYMBOL_NAME_MAX_SIZE = 12
