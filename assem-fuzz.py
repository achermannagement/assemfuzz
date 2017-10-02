import subprocess
import random
import shutil
import filecmp
import os
import difflib
import string

N = 100000000
MAX_SIZE=2**15-1

SYMBOL_NAME_MIN_SIZE = 5
SYMBOL_NAME_MAX_SIZE = 12

FILE_TITLE = "fuzz"
PATH_TO_TEST_FILE = FILE_TITLE + ".asm"
PATH_TO_TEST_OUTPUT = FILE_TITLE + ".hack"
PATH_TO_ASSEMBLER = "Assembler"
RUN_STRING = "java {} {}".format(PATH_TO_ASSEMBLER, PATH_TO_TEST_FILE)
COMP_RUN_STRING_WINDOWS = "Assembler.bat {}".format(PATH_TO_TEST_FILE)
COMP_RUN_STRING_LINUX = "Assembler.sh {}".format(PATH_TO_TEST_FILE)

DESTS = ["A", "M", "D", "AM", "AD", "MD", "AMD"]
OPS = ["0", "1", "-1", "D", "A", "!D", "!A", "-D", "-A", "D+1", "A+1", "D-1", "A-1", "D+A", "D-A", "D&A", "D|A", "M", "!M", "-M", "M+1", "M-1", "D+M", "D-M", "M-D", "D&M", "D|M"]
JUMPS = ["JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]
PREDEFINED_SYMBOLS = ["SP", "LCL", "ARG", "THIS", "THAT", "SCREEN", "KBD"]
for i in range(16):
    PREDEFINED_SYMBOLS.append("R{}".format(i))

def main():
    passed = True
    onWindows = False
    if os.name == 'nt': # detect whether the platform I am running on is Windows
        onWindows = True
        
    for i in range((N // MAX_SIZE)+1):
        fuzzer = RandomFuzzer()
        handler = Handler(fuzzer, onWindows)
        if not handler.success():
            passed = False
    print("PASSED ALL TESTS? " + str(passed))

class Handler():

    def __init__(self, fuzzer, onWindows=True):

        self.result = False
      
        # have fuzzer prepare input file
        fuzzer.prepareFile()

        # clean test folders
        if os.path.exists("mine/" + PATH_TO_TEST_FILE):
            os.remove("mine/" + PATH_TO_TEST_FILE)

        if os.path.exists("theirs/" + PATH_TO_TEST_FILE):
            os.remove("theirs/" + PATH_TO_TEST_FILE)

        if os.path.exists("mine/" + PATH_TO_TEST_OUTPUT):
            os.remove("mine/" + PATH_TO_TEST_OUTPUT)

        if os.path.exists("theirs/" + PATH_TO_TEST_OUTPUT):
            os.remove("theirs/" + PATH_TO_TEST_OUTPUT)

        # copy to each directory
        shutil.copy(PATH_TO_TEST_FILE, "mine/" + PATH_TO_TEST_FILE)
        shutil.copy(PATH_TO_TEST_FILE, "theirs/" + PATH_TO_TEST_FILE)

        # do my assembler
        os.chdir("mine")
        result = subprocess.run(RUN_STRING, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if(result.returncode != 0):
            print("Exception! @ " + fuzzer.log())
            type = str(result.stderr).split(":")[0][2:]
            print("Type: {}".format(type))
            raise(Exception())

        os.chdir("../theirs")
        if onWindows == True:
            result = subprocess.run(COMP_RUN_STRING_WINDOWS, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            result = subprocess.run(COMP_RUN_STRING_LINUX, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir("..")
        # need to compare files by contents
        if filecmp.cmp("mine/" + PATH_TO_TEST_OUTPUT, "theirs/" + PATH_TO_TEST_OUTPUT, shallow=False):
            self.result = True
            print("Test passed")
        else:
            print("Test failed")
            diff = difflib.unified_diff(open("mine/" + PATH_TO_TEST_OUTPUT, "r").readlines(),
            open("theirs/" + PATH_TO_TEST_OUTPUT, "r").readlines())
            diff_file = open("diff", "w")
            for line in diff:
                diff_file.write(line)
                
    def success(self):
      return self.result

class RandomFuzzer():

    def __init__(self):
        self.length = MAX_SIZE
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
            choices = [random.randint(0,MAX_SIZE)]
            choices.append(random.choice(PREDEFINED_SYMBOLS))
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
        valid = random.choice("_.$:" + string.ascii_lowercase + string.ascii_uppercase)
        size = random.randint(SYMBOL_NAME_MIN_SIZE, SYMBOL_NAME_MAX_SIZE)
        for _ in range(size-1):
            valid += random.choice("_.$:" + string.ascii_lowercase + string.ascii_uppercase + string.digits)
        return valid

    def log(self):
        return "RandomFuzzer file: {} length: {}".format(self.file, self.length)

    def dest(self):
        return random.choice(DESTS)

    def operand(self):
        return random.choice(OPS)

    def jump(self):
        return random.choice(JUMPS)

    def makeRandomInstruction(self):
        inst_type = random.choice(["ADDR", "COMP", "JUMP", "LABEL", "EMPTY"])
        if inst_type == "ADDR":
            inst = "@{}".format(self.load())
        elif inst_type == "COMP":
            inst = "{}={}".format(self.dest(), self.operand())
        elif inst_type == "LABEL":
            label = self.makeValidName()
            self.labels.append(label)
            inst = "({})".format(label)
        elif inst_type == "JUMP":
            inst = "{};{}".format(random.choice("AMD0"), self.jump())
        else:
            inst = ""
            
        if random.choice(["COMMENT", "NO"]) == "COMMENT":
            inst += " // comment !@#$%^&*()'\"\\/*"
            
        return inst

if __name__ == "__main__":
    main()
