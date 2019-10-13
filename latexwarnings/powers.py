import re

class WarningPowers(Warning):

    def __init__(self):
        super().__init__()
    
    def warn_line(self, line):
        match = re.search(r'\^-', line)
        if match:
            return {
                'message' : 'Remember to add curly braces {} around powers with more than one symbol.',
                'start' : match.start(0)
            }
        else:
            return None