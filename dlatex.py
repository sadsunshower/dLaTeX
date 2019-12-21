#!/usr/bin/python3

import json, re, subprocess, sys

import message_generators.all
import formatters

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f'Usage: {sys.argv[0]} (latex file) [json]')
        print('Add \'json\' to get JSON format output')
        sys.exit(1)

    with subprocess.Popen(['pdflatex', sys.argv[1]], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as pdflatex, open(sys.argv[1], 'r') as texfile:
        pdflatex.stdin.write(b'q\n')
        pdflatex.stdin.close()

        file = texfile.read().split('\n')
        output = pdflatex.stdout.read().decode('utf-8', 'ignore').split('\n')

        formatter = formatters.TerminalFormatter()

        if len(sys.argv) == 3 and sys.argv[2] == 'json':
            formatter = formatters.JSONFormatter()
        else:
            print('This is dLaTeX version 0.1')

        for generator in message_generators.all.all_generators:
            formatter.add_messages(generator.trigger_output(output, file))

        for num, line in enumerate(file):
            for generator in message_generators.all.all_generators:
                    formatter.add_messages(generator.trigger_line(line, num))
        
        print(formatter.format())