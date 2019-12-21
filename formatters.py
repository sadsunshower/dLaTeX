import abc, json, typing
import messages

'''
Any kind of formatter for a list of messages
'''
class Formatter(abc.ABC):

    def __init__(self):
        self._messages = []

    def _msg_sort_key(self, msg: messages.Message) -> typing.Tuple[int, int]:
        if msg.position is None:
            return (0, 0)
        else:
            if msg.position.marker is None:
                return (msg.position.line, 0)
            else:
                return (msg.position.line, msg.position.marker[0])

    def add_messages(self, msgs: typing.List[messages.Message]) -> None:
        self._messages.extend(msgs)
    
    def is_error(self) -> bool:
        for msg in self._messages:
            if msg.severity == messages.Severity.ERROR:
                return True
        
        return False

    @abc.abstractmethod
    def format(self) -> str:
        pass

'''
Formats output for the terminal
'''
class TerminalFormatter(Formatter):

    def __init__(self):
        super().__init__()

    def _format_message(self, msg: messages.Message) -> str:
        ret = {
            messages.Severity.INFO : '\n\033[94m\033[1mLaTeX Info\033[0m\n',
            messages.Severity.WARNING : '\n\033[93m\033[1mLaTeX Warning\033[0m\n',
            messages.Severity.ERROR : '\n\033[91m\033[1mLaTeX Error\033[0m\n',
        }[msg.severity]

        ret += msg.message + '\n'

        if msg.position is not None:
            ret += f'\033[1mLine {msg.position.number}:\033[0m ' + msg.position.line + '\n'

            if msg.position.marker is not None:
                if len(msg.position.marker) == 1:
                    ret += '\033[94m' + (' ' * (msg.position.marker[0] + len(str(msg.position.number)) + 7)) + '^\033[0m\n'
                else:
                    ret += '\033[94m' + (' ' * (msg.position.marker[0] + len(str(msg.position.number)) + 7)) + ('^' * (msg.position.marker[1] - msg.position.marker[0])) + '\033[0m\n'

        return ret
    
    def format(self) -> str:
        ret = ''

        for msg in self._messages:
            ret += self._format_message(msg)

        if self.is_error():
            ret += '\nErrors detected, output PDF may have unexpected results.\n'
        else:
            ret += '\nNo errors, output PDF okay.\n'
        
        return ret

'''
Formats output as JSON, for use in web apps
'''
class JSONFormatter(Formatter):

    def __init__(self):
        super().__init__()
    
    def _format_message(self, msg: messages.Message) -> typing.Dict:
        obj = {
            'severity' : {
                messages.Severity.INFO : 'info',
                messages.Severity.WARNING : 'warning',
                messages.Severity.ERROR : 'error'
            }[msg.severity],
            'message' : msg.message,
        }

        if msg.position is not None:
            obj['line'] = msg.position.line
            obj['num'] = msg.position.number
            if msg.position.marker is not None:
                obj['marker'] = list(msg.position.marker)
        
        return obj
    
    def format(self) -> str:
        ret = {
            'messages' : [],
            'error' : self.is_error()
        }

        for msg in self._messages:
            ret['messages'].append(self._format_message(msg))
        
        return json.dumps(ret)