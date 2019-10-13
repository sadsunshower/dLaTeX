import abc

class Warning(abc.ABC):
    
    def __init__(self):
        super().__init__()
    
    @abc.abstractmethod
    def warn_line(self, line):
        pass