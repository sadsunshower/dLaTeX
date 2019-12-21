import re, typing
import message_generators.generator, messages

class GeneratorOperators(message_generators.generator.Generator):

    def __init__(self):
        super().__init__()
    
    def trigger_line(self, line: str, number: int) -> typing.List[messages.Message]:
        ret = []

        for match in re.finditer(r'(^|[^\\a-zA-Z0-9])((arc)?(sin|cos|tan|sec|csc|cot)h?)|(ln|log)([^a-zA-Z0-9]|$)', line):
            ret.append(messages.Message(
                messages.PositionInfo((match.start(1)+1, ), line, number),
                'This looks like it isn\'t a math operator (\\sin, \\cos, etc.) when it should be',
                messages.Severity.WARNING
            ))
        
        return ret