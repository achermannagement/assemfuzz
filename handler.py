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

from definitions import *

class Handler():
  def __init__(self, fuzzer, testOutput, onWindows=True):
    self.result = False
    self.fuzzer = fuzzer
    self.testOutput = testOutput
    # have fuzzer prepare input file
    self.fuzzer.prepareFile()
    self.clean()
    # copy to each directory
    shutil.copy(self.fuzzer.outFile(), MY_FOLDER
    + self.fuzzer.outFile())
    shutil.copy(self.fuzzer.outFile(), THEIR_FOLDER
    + self.fuzzer.outFile())
    # do my assembler
    result = subprocess.run(RUN_STRING, stdout=subprocess.PIPE,
    stderr = subprocess.PIPE, shell=True)
    # check result
    self.check_result(result)
    # move result to folder
    os.rename(self.testOutput, MY_FOLDER + self.testOutput)
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
    if os.path.exists(MY_FOLDER + self.fuzzer.outFile()):
      os.remove(MY_FOLDER + self.fuzzer.outFile())
    if os.path.exists(THEIR_FOLDER + self.fuzzer.outFile()):
      os.remove(THEIR_FOLDER + self.fuzzer.outFile())
    if os.path.exists(MY_FOLDER + self.testOutput):
      os.remove(MY_FOLDER + self.testOutput)
    if os.path.exists(THEIR_FOLDER + self.testOutput):
      os.remove(THEIR_FOLDER + self.testOutput)

  def check_result(self, result):
    if(result.returncode != 0):
      print("Exception! @ " + self.fuzzer.log())
      type = str(result.stderr).split(":")[0][2:]
      print("Type: {}".format(type))
      raise(Exception())

  def compare_output(self):
    if filecmp.cmp(MY_FOLDER + self.testOutput, THEIR_FOLDER
    + self.testOutput, shallow=False):
      self.result = True
      print("Test passed")
    else:
      print("Test failed")
      diff = difflib.unified_diff(open(MY_FOLDER + self.testOutput
      , "r").readlines(),
      open(THEIR_FOLDER + self.testOutput, "r").readlines())
      diff_file = open("diff", "w")
      for line in diff:
        diff_file.write(line)

  def success(self):
    return self.result
