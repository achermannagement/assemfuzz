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

import os
import argparse

from definitions import *
import hack
import handler
import randomFuzzer

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
    fuzzer = randomFuzzer.RandomFuzzer(PATH_TO_TEST_FILE)
    handlerInst = handler.Handler(fuzzer, PATH_TO_TEST_OUTPUT, onWindows)
    if not handlerInst.success():
      passed = False
  print("PASSED ALL TESTS? " + str(passed))

if __name__ == "__main__":
  print("assem-fuzz  Copyright (C) 2017  Joshua Achermann")
  print("This program comes with ABSOLUTELY NO WARRANTY")
  print("This is free software, and you are welcome to redistribute it \
under certain conditions")
  print("Please read LICENSE file for more information")
  main()
