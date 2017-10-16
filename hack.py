"""
specifications of the hack assembly language

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

# hack has 15 bit pointers pointing to program memory
MAX_SIZE=2**15

# valid labels for instruction parts
DESTS = ["A", "M", "D", "AM", "AD", "MD", "AMD"]
OPS = ["0", "1", "-1", "D", "A", "!D", "!A", "-D", "-A",
"D+1", "A+1", "D-1", "A-1", "D+A", "D-A", "D&A", "D|A",
"M", "!M", "-M", "M+1", "M-1", "D+M", "D-M", "M-D", "D&M", "D|M"]
JUMPS = ["JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]
JUMP_LABELS = "AMD0"

# instruction structure
ADDR_INST = "@{}"
COMP_INST = "{}={}"
LABEL_INST = "({})"
JUMP_INST = "{};{}"

# special symbols used by the assembler
PREDEFINED_SYMBOLS = ["SP", "LCL", "ARG", "THIS", "THAT", "SCREEN"
, "KBD"]
# register symbols
for i in range(16):
  PREDEFINED_SYMBOLS.append("R{}".format(i))

# valid symbol characters that can be symbol names
VALID_SYMBOL_CHARS = "_.$:"

# test comment
TEST_COMMENT = " // comment !@#$%^&*()'\"\\/*"
