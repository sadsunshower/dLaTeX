import abc, enum, typing

'''
Position information about which line the message applies to and where on that line
'''
class PositionInfo(object):
    
    def __init__(self, marker: typing.Union[None, typing.Tuple[int], typing.Tuple[int, int]], line: str, number: int):
        self._marker = marker
        self._line = line
        self._number = number
    
    @property
    def marker(self) -> typing.Union[None, typing.Tuple[int], typing.Tuple[int, int]]:
        return self._marker
    
    @property
    def line(self) -> str:
        return self._line
    
    @property
    def number(self) -> int:
        return self._number

'''
A message severity
'''
class Severity(enum.Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2

'''
Any kind of message which should be displayed by the formatter, e.g. a warning or an error
'''
class Message():
    
    def __init__(self, position: typing.Optional[PositionInfo], message: str, severity: Severity):
        self._position = position
        self._message = message
        self._severity = severity
    
    @property
    def position(self) -> typing.Optional[PositionInfo]:
        return self._position
    
    @property
    def message(self) -> str:
        return self._message
    
    @property
    def severity(self) -> Severity:
        return self._severity