#!/usr/bin/python3

from latexwarnings.autosize import WarningAutosize
from latexwarnings.operators import WarningOperators
from latexwarnings.powers import WarningPowers

import json, re, subprocess, sys

def markers(num, pos1, pos2=None):
    if pos2 is not None:
        return '\033[94m' + (' ' * (pos1 + 7 + len(str(num)))) + '^' + (' ' * (pos2 - pos1)) + '^\033[0m'
    else:
        return '\033[94m' + (' ' * (pos1 + 7 + len(str(num)))) + '^\033[0m'

def check_source(lines):
    warnings = [
        WarningAutosize(),
        WarningOperators(),
        WarningPowers()
    ]

    for num in range(len(lines)):
        line = lines[num]

        for warning in warnings:
            w = warning.warn_line(line)
            if w is not None:
                print('\n\033[93m\033[1mLaTeX Warning\033[0m')
                print(w['message'])
                print(f'\033[1mLine {num+1}:\033[0m ' + lines[num])
                if 'end' in w:
                    print(markers(num+1, w['start'], w['end']))
                else:
                    print(markers(num+1, w['start']))

    print()

def nicer_error(msg, errors):
    msg = re.sub(r'^! ', r'', msg)
    return errors.get(msg, f'Unknown error: {msg}')

if __name__ == '__main__':
    print('This is dLaTeX version 0.1')

    errors = {}
    with open(sys.argv[2], 'r') as errors_file:
        errors = json.loads(errors_file.read())

    with subprocess.Popen(['pdflatex', sys.argv[1]], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as pdflatex, open(sys.argv[1], 'r') as texfile:
        pdflatex.stdin.write(b'q\n')
        pdflatex.stdin.close()

        file = texfile.read().split('\n')
        check_source(file)

        output = pdflatex.stdout.read().decode('utf-8', 'ignore').split('\n')

        error = False

        for num in range(len(output)):
            line = output[num]

            if line.startswith('This is ') or line.startswith('LaTeX2e'):
                print(line)
            if line.startswith('!'):
                error = True
                print('\n\033[91m\033[1mLaTeX Error\033[0m')

                curr = num
                while not output[curr].startswith('l.'):
                    curr += 1
        
                num = int(re.search(r'^l.([0-9]+) ', output[curr]).group(1))
                pos = len(re.sub(r'^l.[0-9]+ ', r'', output[curr]))

                print(nicer_error(line, errors))
                print(f'\033[1mLine {num}:\033[0m ' + file[num-1])
                print(markers(num, pos-1))
            if line.startswith('Overfull'):
                num = int(re.search(r'lines ([0-9]+)--', line).group(1))
                wideness = int(re.search(r'([0-9]+).[0-9]pt too wide', line).group(1))
                if 'badness' in line or wideness > 50:
                    error = True
                    print('\n\033[91m\033[1mLaTeX Error\033[0m')
                    print('Overfull horizontal box (much too wide). Try reducing the width of the content in this block.')
                    print(f'\033[1mLine {num}:\033[0m ' + file[num-1])
                else:
                    print('\n\033[93m\033[1mLaTeX Warning\033[0m')
                    print('Overfull horizontal box (slightly too wide). Consider reducing the width of the content in this block.')
                    print(f'\033[1mLine {num}:\033[0m ' + file[num-1])
        
        if error:
            print('\nErrors detected, output PDF may have unexpected results.')
        else:
            print('\nNo errors, output PDF okay.')