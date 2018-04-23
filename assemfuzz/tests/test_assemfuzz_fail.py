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
import argparse

from assemfuzz.__main__ import perform, on_win
from assemfuzz.definitions import DEFAULT_ERR_LOG

def test_assemfuzz():
    """Uses the default handler and random fuzzer to run multiple
    fuzzing rounds on the assembler defined in defintions.py
    """
    args = argparse.ArgumentParser()
    args.license = False
    args.tests = 1
    args.cores = 1
    args.errlog = DEFAULT_ERR_LOG
    args.halt_fail_count = 1
    args.verbose = False
    args.fail = True

    perform(args, on_win())

if __name__ == "__main__":
    test_assemfuzz()
