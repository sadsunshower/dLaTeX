import abc, json, os, re, sys, typing
import messages

'''
Generates messages, based on the LaTeX source or the output
'''
class Generator(abc.ABC):
    
    def __init__(self):
        super().__init__()

    def trigger_line(self, line: str, number: int) -> typing.List[messages.Message]:
        return []

    def trigger_output(self, output: typing.List[str], file: typing.List[str]) -> typing.List[messages.Message]:
        return []

'''
Most error messages can just be looked up, this deals with that
'''
class GeneratorLookup(Generator):

    def __init__(self):
        super().__init__()

        with open(os.path.join(sys.path[0], 'errors.json'), 'r') as f:
            self._errors = json.loads(f.read())
    
    def _error_lookup(self, msg: str) -> str:
        for error in self._errors:
            if msg.startswith(error):
                return self._errors[error]
        
        return f'Unknown error: {msg}'
    
    def trigger_output(self, output: typing.List[str], file: typing.List[str]) -> typing.List[messages.Message]:
        ret = []

        for output_num, line in enumerate(output):
            if line.startswith('!'):
                curr = output_num
                while not output[curr].startswith('l.'):
                    curr += 1
                
                    if curr == len(output):
                        curr = -1
                        break
                
                if curr != -1:
                    num = int(re.search(r'^l.([0-9]+) ', output[curr]).group(1))
                    pos = len(re.sub(r'^l.[0-9]+ ', r'', output[curr]))
                    msg = re.sub(r'^! ', r'', line)

                    ret.append(messages.Message(
                        messages.PositionInfo((pos - 1, ), file[num - 1], num),
                        self._error_lookup(msg),
                        messages.Severity.ERROR
                    ))
                else:
                    ret.append(messages.Message(
                        None,
                        self._error_lookup(re.sub(r'^! ', r'', line)),
                        messages.Severity.ERROR
                    ))

        return ret