import re

class WarningAutosize(Warning):

    def __init__(self):
        super().__init__()
    
    def warn_line(self, line):
        match = re.search(r'\(([^\)]*(\\frac|\\sum|\\int)[^\)]*)\)', line)
        if match and not ('\\left(' + match.group(1) in line or '\\(' + match.group(1) in line):
            return {
                'message' : 'Did you mean to auto-size these brackets with \\left and \\right?',
                'start' : match.start(0),
                'end' : match.end(0)-2
            }
        else:
            return None
