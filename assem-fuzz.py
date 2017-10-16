"""
generates long strings of valid hack assembly and compares against a
reference assembler

Copyright (C) 2017  Joshua Achermann

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
#!/bin/python3

import subprocess
import random
import shutil
import filecmp
import os
import difflib
import string
import argparse

from definitions import *
import hack

def main():
  # parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("lines"
  , help="rough # of lines of assembly code to fuzz", type=int)
  args = parser.parse_args()
  # begin the program
  passed = True
  onWindows = False
  # detect whether the platform I am running on is Windows
  if os.name == 'nt':
    onWindows = True
  for i in range((args.lines // hack.MAX_SIZE)+1):
    fuzzer = RandomFuzzer()
    handler = Handler(fuzzer, onWindows)
    if not handler.success():
      passed = False
  print("PASSED ALL TESTS? " + str(passed))

class Handler():
  def __init__(self, fuzzer, onWindows=True):
    self.result = False
    self.fuzzer = fuzzer
    # have fuzzer prepare input file
    self.fuzzer.prepareFile()
    self.clean()
    # copy to each directory
    shutil.copy(PATH_TO_TEST_FILE, "mine/" + PATH_TO_TEST_FILE)
    shutil.copy(PATH_TO_TEST_FILE, "theirs/" + PATH_TO_TEST_FILE)
    # do my assembler
    result = subprocess.run(RUN_STRING, stdout=subprocess.PIPE,
    stderr = subprocess.PIPE, shell=True)
    # check result
    self.check_result(result)
    # move result to folder
    os.rename(PATH_TO_TEST_OUTPUT, "mine/" + PATH_TO_TEST_OUTPUT)
    # run the standard assembler
    if onWindows == True:
      result = subprocess.run(COMP_RUN_STRING_WINDOWS,
      stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:
      result = subprocess.run(COMP_RUN_STRING_LINUX,
      stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # check result
    self.check_result(result)
    # need to compare files by contents
    self.compare_output()

  def clean(self):
    # clean test folders
    if os.path.exists("mine/" + PATH_TO_TEST_FILE):
      os.remove("mine/" + PATH_TO_TEST_FILE)
    if os.path.exists("theirs/" + PATH_TO_TEST_FILE):
      os.remove("theirs/" + PATH_TO_TEST_FILE)
    if os.path.exists("mine/" + PATH_TO_TEST_OUTPUT):
      os.remove("mine/" + PATH_TO_TEST_OUTPUT)
    if os.path.exists("theirs/" + PATH_TO_TEST_OUTPUT):
      os.remove("theirs/" + PATH_TO_TEST_OUTPUT)

  def check_result(self, result):
    if(result.returncode != 0):
      print("Exception! @ " + self.fuzzer.log())
      type = str(result.stderr).split(":")[0][2:]
      print("Type: {}".format(type))
      raise(Exception())

  def compare_output(self):
    if filecmp.cmp("mine/" + PATH_TO_TEST_OUTPUT, "theirs/"
    + PATH_TO_TEST_OUTPUT, shallow=False):
      self.result = True
      print("Test passed")
    else:
      print("Test failed")
      diff = difflib.unified_diff(open("mine/" + PATH_TO_TEST_OUTPUT
      , "r").readlines(),
      open("theirs/" + PATH_TO_TEST_OUTPUT, "r").readlines())
      diff_file = open("diff", "w")
      for line in diff:
        diff_file.write(line)

  def success(self):
    return self.result

class RandomFuzzer():
  def __init__(self):
    self.length = hack.MAX_SIZE
    self.contents = []
    self.variables = []
    self.labels = []
    for i in range(self.length):
      self.contents.append(self.makeRandomInstruction())
    self.contents = "\n".join(self.contents)
    self.file = open(PATH_TO_TEST_FILE, "wb")

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

if __name__ == "__main__":
  print("assem-fuzz  Copyright (C) 2017  Joshua Achermann")
  print("This program comes with ABSOLUTELY NO WARRANTY")
  print("This is free software, and you are welcome to redistribute it \
under certain conditions")
  print("Please read LICENSE file for more information")
  main()
