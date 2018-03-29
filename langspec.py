from abc import ABC, abstractmethod

class LangSpec(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def make_random_program(self):
        pass

    @abstractmethod
    def make_invalid_program(self):
        pass
    
    @abstractmethod
    def make_random_instruction(self):
        pass

    @abstractmethod
    def make_invalid_instruction(self):
        pass
