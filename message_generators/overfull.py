import re, typing
import message_generators.generator, messages

class GeneratorOverfull(message_generators.generator.Generator):

    def __init__(self):
        super().__init__()
    
    def trigger_output(self, output: typing.List[str], file: typing.List[str]) -> typing.List[messages.Message]:
        ret = []
        for line in output:
            if line.startswith('Overfull'):
                num = int(re.search(r'lines ([0-9]+)--', line).group(1))
                wideness = int(re.search(r'([0-9]+).[0-9]pt too wide', line).group(1))

                msg, severity = ('slightly too wide', messages.Severity.WARNING) if ('badness' not in line and wideness <= 50) else ('much too wide', messages.Severity.ERROR)

                ret.append(messages.Message(
                    messages.PositionInfo(None, file[num - 1], num),
                    f'Overfull horizontal box ({msg}). Consider reducing the width of the content in this block.',
                    severity
                ))
            
            return ret