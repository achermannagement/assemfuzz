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
import random
import string

from assemfuzz.langspec import LangSpec

# hack has 15 bit pointers pointing to program memory
MAX_SIZE = 2**15

# this is not a strict requirement for hack assembly
SYMBOL_NAME_MIN_SIZE = 5
SYMBOL_NAME_MAX_SIZE = 12

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
PREDEFINED_SYMBOLS = ["SP", "LCL", "ARG", "THIS", "THAT", "SCREEN", "KBD"]
# register symbols
for i in range(16):
    PREDEFINED_SYMBOLS.append("R{}".format(i))

# valid symbol characters that can be in symbol names
VALID_SYMBOL_CHARS = "_.$:"
INVALID_SYMBOL_CHARS = ["@"]

# test comment
TEST_COMMENT = " // comment !@#$%^&*()'\"\\/*"

def make_valid_name():
    """Make a valid name for the provided language spec"""
    valid = random.choice(VALID_SYMBOL_CHARS +
                          string.ascii_lowercase + string.ascii_uppercase)
    size = random.randint(SYMBOL_NAME_MIN_SIZE,
                          SYMBOL_NAME_MAX_SIZE)
    for _ in range(size):
        valid += random.choice(VALID_SYMBOL_CHARS +
                               string.ascii_lowercase +
                               string.ascii_uppercase + string.digits)
    return valid

def make_invalid_name():
    """Make a name that does not follow the language spec"""
    invalid = random.choice(string.digits)
    size = random.randint(SYMBOL_NAME_MIN_SIZE,
                          SYMBOL_NAME_MAX_SIZE)
    for _ in range(size):
        invalid += chr(random.randint(0, 255)) # can use any char to create invalid
    return invalid

def dest():
    """Returns a destination instruction"""
    return random.choice(DESTS)

def operand():
    """Returns an operand"""
    return random.choice(OPS)

def jump():
    "Selects a random jump type"
    return random.choice(JUMPS)

class Hack(LangSpec):
    """This is a language specification wrapper class for the Hack assembly language."""

    def __init__(self):
        super().__init__()
        self.variables = []
        self.labels = []

    def load(self):
        """Loads a variable, but also has the choice to generate a new one"""
        if random.choice(["NEW", "EXISTING"]) == "EXISTING":
            choices = [random.randint(0, MAX_SIZE-1)]
            choices.append(random.choice(PREDEFINED_SYMBOLS))
            if self.variables:
                choices.append(random.choice(self.variables))
            if self.labels:
                choices.append(random.choice(self.labels))
            returned = random.choice(choices)
        else:
            returned = make_valid_name()
            self.variables.append(returned)
        return returned

    def make_random_program(self):
        pass

    def make_invalid_program(self):
        pass

    def make_random_instruction(self):
        """Generates a random valid instruction for the for the hack assembly language"""
        inst_type = random.choice(["ADDR", "COMP", "JUMP", "LABEL", "EMPTY"])
        if inst_type == "ADDR":
            inst = ADDR_INST.format(self.load())
        elif inst_type == "COMP":
            inst = COMP_INST.format(dest(), operand())
        elif inst_type == "LABEL":
            label = make_valid_name()
            self.labels.append(label)
            inst = LABEL_INST.format(label)
        elif inst_type == "JUMP":
            inst = JUMP_INST.format(random.choice(JUMP_LABELS), jump())
        else:
            inst = "" # empty line (might have comment)
        if random.choice(["COMMENT", "NO"]) == "COMMENT":
            inst += TEST_COMMENT # add comment containing many characters
        return inst

    def make_invalid_instruction(self):
        """Generates an invalid instruction"""
        return make_invalid_name()
