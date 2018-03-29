from abc import ABC, abstractmethod
import os
import shutil

from definitions import MY_FOLDER, THEIR_FOLDER

class Handler(ABC):

    def __init__(self, test_input, test_output, lang_spec,
                 program, ref_program, errlog, log_lock, windows=False, talking_stick=None):
        self.program = program
        self.ref_program = ref_program
        self.test_input = test_input
        self.test_output = test_output
        self.lang_spec = lang_spec
        self.windows = windows
        self.errlog = errlog
        self.log_lock = log_lock
        self.fuzzer = self.prepare_fuzzer()
        self.talking_stick = talking_stick

    @abstractmethod
    def prepare_fuzzer(self):
        pass

    @abstractmethod
    def run_test(self, my_result, their_result):
        pass

    def handle(self):
        """Perform the fuzz, handle the results"""
        self.clean()
        self.fuzzer.prepare_file()
        self.fuzzer.write_file()
        shutil.copy(self.test_input,
                    os.path.join(MY_FOLDER, self.test_input))
        shutil.copy(self.test_input,
                    os.path.join(THEIR_FOLDER, self.test_input))

        my_result = self.program_under_test()
        if not self.program_had_error(my_result):
            os.rename(self.test_output, os.path.join(MY_FOLDER, self.test_output))

        their_result = self.reference_program()

        #os.rename(self.test_output, os.path.join(THEIR_FOLDER, self.test_output))
        self.success = self.run_test(my_result, their_result)

        if self.success:
            self.talk("Test success")
            self.clean()
        else:
            self.talk("Test failed")
            self.log()

    def talk(self, msg):
        if self.talking_stick != None:
            self.talking_stick.acquire()
            print(msg)
            self.talking_stick.release()

    def clean(self):
        """Clean test output."""
        if os.path.exists(os.path.join(MY_FOLDER, self.test_input)):
            os.remove(os.path.join(MY_FOLDER, self.test_input))
        if os.path.exists(os.path.join(THEIR_FOLDER, self.test_input)):
            os.remove(os.path.join(THEIR_FOLDER, self.test_input))
        if os.path.exists(os.path.join(MY_FOLDER, self.test_output)):
            os.remove(os.path.join(MY_FOLDER, self.test_output))
        if os.path.exists(os.path.join(THEIR_FOLDER, self.test_output)):
            os.remove(os.path.join(THEIR_FOLDER, self.test_output))
        if os.path.exists(self.test_input):
            os.remove(self.test_input)
        if os.path.exists(os.path.join(self.test_output)):
            os.remove(os.path.join(self.test_output))

    def program_under_test(self):
        """Runs the program function for the program under test"""
        return self.program(self.test_input)

    def reference_program(self):
        """Runs the program function for the reference program"""
        return self.ref_program(self.test_input, self.windows)

    def log(self):
        """Logs a test failure in the error log."""
        self.log_lock.acquire()
        errlog = open(self.errlog, "a")
        errlog.write("Test failure: {} ".format(self.test_input))
        self.log_lock.release()
    
    def program_had_error(self, result):
        return result.stderr != b""

    def check_success(self):
        """Returns whether the test succeeded"""
        return self.success
