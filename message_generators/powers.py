import re, typing
import message_generators.generator, messages

class GeneratorPowers(message_generators.generator.Generator):

    def __init__(self):
        super().__init__()
    
    def trigger_line(self, line: str, number: int) -> typing.List[messages.Message]:
        ret = []

        for match in re.finditer(r'\^-', line):
            ret.append(messages.Message(
                messages.PositionInfo((match.start(0), ), line, number),
                'Remember to add curly braces `{}` around powers with more than one symbol.',
                messages.Severity.WARNING
            ))
        
        return ret