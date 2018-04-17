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
import os

import assemfuzz.__init__ as __init__

MY_FOLDER = "mine"
THEIR_FOLDER = "theirs"

FILE_TITLE = "fuzz"
PATH_TO_TEST_FILE = FILE_TITLE + "_{}_{}.hack"
PATH_TO_FUZZ_OUTPUT = FILE_TITLE + "_{}_{}.asm"
DIFF_FILE_NAME = "diff"

DEFAULT_ERR_LOG = "err.log"
