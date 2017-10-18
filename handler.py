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
import os
import subprocess
import shutil
import filecmp
import difflib

import definitions

class Handler():
  def __init__(self, fuzzer, testOutput, onWindows=True):
    self.result = False
    self.fuzzer = fuzzer
    self.test_output = testOutput
    # have fuzzer prepare input file
    self.fuzzer.prepare_file()
    self.clean()
    # copy to each directory
    shutil.copy(self.fuzzer.out_file(), definitions.MY_FOLDER
    + self.fuzzer.out_file())
    shutil.copy(self.fuzzer.out_file(), definitions.THEIR_FOLDER
    + self.fuzzer.out_file())
    # do my assembler
    result = subprocess.run(definitions.RUN_STRING, stdout=subprocess.PIPE,
    stderr = subprocess.PIPE, shell=True)
    # check result
    self.check_result(result)
    # move result to folder
    os.rename(self.test_output, definitions.MY_FOLDER + self.test_output)
    # run the standard assembler
    if onWindows is True:
      result = subprocess.run(definitions.COMP_RUN_STRING_WINDOWS,
      stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:
      result = subprocess.run(definitions.COMP_RUN_STRING_LINUX,
      stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # check result
    self.check_result(result)
    # need to compare files by contents
    self.compare_output()

  def clean(self):
    # clean test folders
    if os.path.exists(definitions.MY_FOLDER + self.fuzzer.out_file()):
      os.remove(definitions.MY_FOLDER + self.fuzzer.out_file())
    if os.path.exists(definitions.THEIR_FOLDER + self.fuzzer.out_file()):
      os.remove(definitions.THEIR_FOLDER + self.fuzzer.out_file())
    if os.path.exists(definitions.MY_FOLDER + self.test_output):
      os.remove(definitions.MY_FOLDER + self.test_output)
    if os.path.exists(definitions.THEIR_FOLDER + self.test_output):
      os.remove(definitions.THEIR_FOLDER + self.test_output)

  def check_result(self, result):
    if result.returncode != 0:
      print("Exception! @ " + self.fuzzer.log())
      except_type = str(result.stderr).split(":")[0][2:]
      print("Type: {}".format(except_type))
      raise Exception()

  def compare_output(self):
    if filecmp.cmp(definitions.MY_FOLDER + self.test_output, definitions.THEIR_FOLDER
    + self.test_output, shallow=False):
      self.result = True
    else:
      diff = difflib.unified_diff(open(definitions.MY_FOLDER + self.test_output
      , "r").readlines(),
      open(definitions.THEIR_FOLDER + self.test_output, "r").readlines())
      diff_file = open("diff", "w")
      for line in diff:
        diff_file.write(line)

  def success(self):
    return self.result
