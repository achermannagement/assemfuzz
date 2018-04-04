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
import sys
import argparse
import subprocess
import multiprocessing as mp
import traceback

import hack
from definitions import (THEIR_FOLDER, DEFAULT_ERR_LOG,
                         PATH_TO_TEST_FILE, PATH_TO_FUZZ_OUTPUT)
from myprogram import my_assembler, my_cond
import comparehandler
import failhandler

PATH_TO_ASSEMBLER = "Assembler"
COMP_RUN_STRING_WINDOWS = "{} {}"
COMP_RUN_STRING_LINUX = "{} {}"

def their_cond(err):
    """extract error line from reference assembler error message"""
    return int(err.split()[2][:-1])

def their_assembler(input_path, windows=False):
    """This is the function to run the Nand2Tetris reference assembler"""
    if not windows:
        result = subprocess.run(COMP_RUN_STRING_LINUX.format(os.path.join(THEIR_FOLDER,
                                                                          PATH_TO_ASSEMBLER +
                                                                          ".sh"),
                                                             os.path.join(THEIR_FOLDER,
                                                                          input_path)),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
    else:
        result = subprocess.run(COMP_RUN_STRING_WINDOWS.format(os.path.join(THEIR_FOLDER,
                                                                            PATH_TO_ASSEMBLER +
                                                                            ".bat"),
                                                               os.path.join(THEIR_FOLDER,
                                                                            input_path)),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
    return result

def fuzz(queue, name, fail_test, log_tuple, on_windows):
    """This is the function that is passed to worker processes."""
    try:
        lang_spec = hack.Hack()
        (i, j) = name
        programs = (my_assembler, their_assembler)
        conds = (my_cond, their_cond)
        data = {"programs":programs, "conds":conds,
                "log_tuple":log_tuple, "on_windows":on_windows}
        if not fail_test:
            handler_inst = comparehandler.CompareHandler(
                PATH_TO_FUZZ_OUTPUT.format(j, i),
                PATH_TO_TEST_FILE.format(j, i),
                lang_spec, data)
        else:
            handler_inst = failhandler.FailHandler(
                PATH_TO_FUZZ_OUTPUT.format(j, i),
                PATH_TO_TEST_FILE.format(j, i),
                lang_spec, data)
        handler_inst.handle()
        queue.put(handler_inst.check_success())
    except Exception as exc:
        print(exc)
        traceback.print_tb(sys.exc_info()[2])
        queue.put(False)

def specify_args():
    """Specifies the arguments handled by this program"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--license", help="show license information and then exit",
                        action="store_true")
    parser.add_argument("-t", "--tests", help="number of tests to run, defaults to 1",
                        type=int)
    parser.add_argument("-c", "--cores", help="number of threads to run, defaults to 1",
                        type=int)
    parser.add_argument("-f", "--fail", help="whether to test invalid programs",
                        action="store_true")
    parser.add_argument("-e", "--errlog", help="file path to log failed tests summary",
                        type=argparse.FileType('w'))
    parser.add_argument("-v", "--verbose", help="print more information",
                        action="store_true")
    parser.add_argument("-fn", "--halt_on_fail_count",
                        help="""how many failed tests can occur before execution stops
                                , defaults to 1""")
    return parser.parse_args()

def perform(args, on_windows):
    """Perform the fuzzing with the given options"""
    passed = True
    fail_count = 0
    for i in range(args.tests // args.cores):
        results = mp.Queue() # pool to collect results
        log_lock = mp.Lock()
        if args.verbose:
            talking_stick = mp.Lock()
        else:
            talking_stick = None
        log_tuple = (args.errlog, log_lock, talking_stick)
        processes = [mp.Process(
            target=fuzz,
            args=(
                results, (i, x), args.fail, log_tuple,
                on_windows))
                     for x in range(args.cores)]

        if args.verbose:
            print("Running test set {}".format(i))

        # start a process for each core
        for j in range(args.cores):
            processes[j].start()

        # join all completed tasks
        for j in range(args.cores):
            processes[j].join()

        # pool the results into an array of bools
        results = [results.get() for p in processes]
        fail_count += results.count(False)

        if args.halt_fail_count <= fail_count:
            if args.verbose:
                print("Halt fail count exceeded, halting testing")
            break

    if fail_count > 0:
        passed = False

    print("PASSED ALL TESTS: " + str(passed))

def main():
    """Uses the default handler and random fuzzer to run multiple
    fuzzing rounds on the assembler defined in defintions.py
    """
    args = specify_args()
    if args.license:
        print("assem-fuzz  Copyright (C) 2017  Joshua Achermann")
        print("This program comes with ABSOLUTELY NO WARRANTY")
        print("This is free software, and you are welcome to redistribute it "
              "under certain conditions")
        print("Please read LICENSE file for more information")
    else:

        if not args.tests:
            args.tests = 1

        if not args.cores:
            args.cores = 1

        if not args.errlog:
            args.errlog = DEFAULT_ERR_LOG

        if not args.halt_on_fail_count:
            args.halt_fail_count = 1

        if args.verbose:
            print("{} tests over {} cores, errors logged @ {},"
                  " halt on {} failed tests".format(args.tests, args.cores,
                                                    args.errlog, args.halt_fail_count))
            if args.fail:
                print("These tests will be run with invalid code")

        # detect whether the platform I am running on is Windows
        on_windows = False
        if os.name == 'nt':
            on_windows = True

        perform(args, on_windows)

if __name__ == "__main__":
    main()
