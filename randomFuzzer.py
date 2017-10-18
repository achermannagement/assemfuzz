"""
creates a random valid Hack assembly file

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

from definitions import *
import hack

class RandomFuzzer():
  def __init__(self, fileName):
    self.length = hack.MAX_SIZE
    self.contents = []
    self.variables = []
    self.labels = []
    self.fileName = fileName
    for i in range(self.length):
      self.contents.append(self.makeRandomInstruction())
    self.contents = "\n".join(self.contents)
    self.file = open(fileName, "wb")

  def outFile(self):
    return self.fileName

  def prepareFile(self):
    self.file.write(self.contents.encode("utf-8"))

  def load(self):
    if random.choice(["NEW", "EXISTING"]) == "EXISTING":
      choices = [random.randint(0,hack.MAX_SIZE-1)]
      choices.append(random.choice(hack.PREDEFINED_SYMBOLS))
      if self.variables:
        choices.append(random.choice(self.variables))
      if self.labels:
        choices.append(random.choice(self.labels))
      returned = random.choice(choices)
    else:
      returned = self.makeValidName()
      self.variables.append(returned)
    return returned

  def makeValidName(self):
    valid = random.choice(hack.VALID_SYMBOL_CHARS
    + string.ascii_lowercase + string.ascii_uppercase)
    size = random.randint(SYMBOL_NAME_MIN_SIZE
    , SYMBOL_NAME_MAX_SIZE)
    for _ in range(size-1):
      valid += random.choice(hack.VALID_SYMBOL_CHARS
      + string.ascii_lowercase + string.ascii_uppercase + string.digits)
    return valid

  def log(self):
    return "RandomFuzzer file: {} length: {}".format(self.file,
    self.length)

  def dest(self):
    return random.choice(hack.DESTS)

  def operand(self):
    return random.choice(hack.OPS)

  def jump(self):
    return random.choice(hack.JUMPS)

  def makeRandomInstruction(self):
    inst_type = random.choice(["ADDR", "COMP", "JUMP", "LABEL"
    , "EMPTY"])
    if inst_type == "ADDR":
      inst = hack.ADDR_INST.format(self.load())
    elif inst_type == "COMP":
      inst = hack.COMP_INST.format(self.dest(), self.operand())
    elif inst_type == "LABEL":
      label = self.makeValidName()
      self.labels.append(label)
      inst = hack.LABEL_INST.format(label)
    elif inst_type == "JUMP":
      inst = hack.JUMP_INST.format(random.choice(hack.JUMP_LABELS), self.jump())
    else:
      inst = "" # empty line (might have comment)
    if random.choice(["COMMENT", "NO"]) == "COMMENT":
      # add comment containing many characters
      inst += hack.TEST_COMMENT
    return inst
