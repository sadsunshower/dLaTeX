import re, typing
import message_generators.generator, messages

class GeneratorAutosize(message_generators.generator.Generator):

    def __init__(self):
        super().__init__()
    
    def trigger_line(self, line: str, number: int) -> typing.List[messages.Message]:
        ret = []

        for match in re.finditer(r'\(([^\)]*(\\frac|\\sum|\\int)[^\)]*)\)', line):
            if not ('\\left(' + match.group(1) in line or '\\(' + match.group(1) in line):
                ret.append(messages.Message(
                    messages.PositionInfo((match.start(0), match.end(0)), line, number),
                    'Did you mean to auto-size these brackets with \\left and \\right?',
                    messages.Severity.WARNING
                ))
        
        return ret