import re

class WarningOperators(Warning):

    def __init__(self):
        super().__init__()
    
    def warn_line(self, line):
        match = re.search(r'(^|[^\\a-zA-Z0-9])((arc)?(sin|cos|tan|sec|csc|cot)h?)|(ln|log)([^a-zA-Z0-9]|$)', line)
        if match:
            return {
                'message' : 'This looks like it isn\'t a math operator (\\sin, \\cos, etc.) when it should be',
                'start' : match.start(1)+1
            }
        else:
            return None
