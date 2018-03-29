from abc import ABC, abstractmethod

class Fuzzer(ABC):

    def __init__(self, file_name, lang_spec):
        self.lang_spec = lang_spec
        self.file_name = file_name

    @abstractmethod
    def prepare_file(self):
        pass

    def write_file(self):
        """Once the fuzzer has generated the code, this function writes it to the file"""
        self.file = open(self.file_name, "wb")
        self.file.write(self.contents.encode("utf-8"))

    def log(self):
        """Returns some debugging information"""
        return "RandomFuzzer file: {} length: {}".format(self.file,
                                                         self.length)