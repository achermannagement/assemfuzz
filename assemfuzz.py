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
import subprocess
import multiprocessing as mp

import hack
from definitions import (MY_FOLDER, THEIR_FOLDER, DEFAULT_ERR_LOG,
                         PATH_TO_TEST_FILE, PATH_TO_FUZZ_OUTPUT)
import comparehandler
import failhandler

PATH_TO_ASSEMBLER = "Assembler"
RUN_STRING = "java -cp {} {} {}"
COMP_RUN_STRING_WINDOWS = "{} {}"
COMP_RUN_STRING_LINUX = "{} {}"

# these specify the extraction of fail line number
def my_cond(err):
    return int(err.split()[4][:-1])

def their_cond(err):
    return int(err.split()[2][:-1])

# these specify the running of the programs
def my_assembler(input_path):
    """This is the function we pass into the handler to run our program"""
    return subprocess.run(RUN_STRING.format(MY_FOLDER, PATH_TO_ASSEMBLER, input_path),
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, shell=True)

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

def fuzz(queue, i, j, fail_test, errlog, log_lock, on_windows, talking_stick=None):
    """This is the function that is passed to worker processes."""
    try:
        lang_spec = hack.Hack()
        if talking_stick != None:
            if not fail_test:
                handler_inst = comparehandler.CompareHandler(PATH_TO_FUZZ_OUTPUT.format(j, i),
                                                             PATH_TO_TEST_FILE.format(j, i),
                                                             lang_spec,
                                                             my_assembler, their_assembler, errlog,
                                                             log_lock, on_windows, talking_stick)
            else:
                handler_inst = failhandler.FailHandler(PATH_TO_FUZZ_OUTPUT.format(j, i),
                                                       PATH_TO_TEST_FILE.format(j, i),
                                                       lang_spec, my_assembler, their_assembler,
                                                       errlog, log_lock, my_cond, their_cond, on_windows, talking_stick)
        else:
            if not fail_test:
                handler_inst = comparehandler.CompareHandler(PATH_TO_FUZZ_OUTPUT.format(j, i),
                                                             PATH_TO_TEST_FILE.format(j, i),
                                                             lang_spec,
                                                             my_assembler, their_assembler, errlog,
                                                             log_lock, on_windows)
            else:
                handler_inst = failhandler.FailHandler(PATH_TO_FUZZ_OUTPUT.format(j, i),
                                                       PATH_TO_TEST_FILE.format(j, i),
                                                       lang_spec, my_assembler, their_assembler,
                                                       errlog, log_lock, my_cond, their_cond, on_windows)
        handler_inst.handle()
        queue.put(handler_inst.check_success())
    except Exception as e:
        print(e)
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

def perform(tests, cores, errlog, halt_fail_count, fail_test, verbose, on_windows):
    """Perform the fuzzing with the given options"""    
    passed = True
    fail_count = 0

    for i in range(tests // cores):
        results = mp.Queue() # pool to collect results
        log_lock = mp.Lock()
        if verbose:
            talking_stick = mp.Lock()
        else:
            talking_stick = None
        processes = [mp.Process(target=fuzz,
                                args=(results, i, x, fail_test, errlog, log_lock, on_windows, talking_stick))
                     for x in range(cores)]

        if verbose:
            print("Running test set {}".format(i))

        # start a process for each core
        for j in range(cores):
            processes[j].start()

        # join all completed tasks
        for j in range(cores):
            processes[j].join()

        # pool the results into an array of bools
        results = [results.get() for p in processes]
        fail_count += results.count(False)

        if halt_fail_count <= fail_count:
            if verbose:
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
            tests = 1
        else:
            tests = args.tests

        if not args.cores:
            cores = 1
        else:
            cores = args.cores

        if not args.errlog:
            errlog = DEFAULT_ERR_LOG
        else:
            errlog = args.errlog

        if not args.halt_on_fail_count:
            halt_fail_count = 1
        else:
            halt_fail_count = args.halt_on_fail_count

        fail_test = args.fail
        verbose = args.verbose

        if verbose:
            print("{} tests over {} cores, errors logged @ {}, halt on {} failed tests".format(tests, cores, errlog, halt_fail_count))
            if fail_test:
                print("These tests will be run with invalid code")

        # detect whether the platform I am running on is Windows
        on_windows = False
        if os.name == 'nt':
            on_windows = True

        perform(tests, cores, errlog, halt_fail_count, fail_test, verbose, on_windows)

if __name__ == "__main__":
    main()
