"""
helpful functions that help setup tests

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
import os
import subprocess

import assemfuzz.hack as hack
from assemfuzz.definitions import (
    THEIR_FOLDER, THEIR_FOLDER2, DEFAULT_ERR_LOG,
    PATH_TO_TEST_FILE, PATH_TO_FUZZ_OUTPUT)
import assemfuzz.comparehandler as comparehandler
import assemfuzz.failhandler as failhandler
import assemfuzz.definitions
from assemfuzz.common import run, their_assembler, their_cond

def my_assembler(input_path, windows=False):
    return run(THEIR_FOLDER2, input_path, windows)

def fuzz(fail_test, on_windows):
    lang_spec = hack.Hack()
    programs = (my_assembler, their_assembler)
    conds = (their_cond, their_cond)
    folders = (THEIR_FOLDER, THEIR_FOLDER2)
    data = {"programs":programs, "conds":conds,
            "log_tuple":(None, None, None), "on_windows":on_windows,
            "folders": folders}
    if not fail_test:
        handler_inst = comparehandler.CompareHandler(
            PATH_TO_FUZZ_OUTPUT.format(0, 0),
            PATH_TO_TEST_FILE.format(0, 0),
            lang_spec, data)
    else:
        handler_inst = failhandler.FailHandler(
            PATH_TO_FUZZ_OUTPUT.format(0, 0),
            PATH_TO_TEST_FILE.format(0, 0),
            lang_spec, data)
    handler_inst.handle()
    assert handler_inst.check_success()

def on_win():
    """Uses the default handler and random fuzzer to run multiple
    fuzzing rounds on the assembler defined in defintions.py
    """
    # detect whether the platform I am running on is Windows
    on_windows = False
    if os.name == 'nt':
        on_windows = True

    return on_windows
