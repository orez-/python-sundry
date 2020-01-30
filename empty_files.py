import os
import os.path
import sys
import token
import tokenize


NONCODE_TOKENS = {tokenize.COMMENT, tokenize.NL, token.ENDMARKER, token.STRING, token.NEWLINE}

def is_empty(filename):
    with open(filename, 'r') as file:
        for type_, str_, (srow, scol), (erow, ecol), line in tokenize.generate_tokens(file.readline):
            if type_ not in NONCODE_TOKENS:
                return False
        return True


def find_empty_files(top):
    for directory, subdirs, files in os.walk(top):
        if 'node_modules' in subdirs:
            subdirs.remove('node_modules')
        for filename in files:
            # __init__s serve a purpose besides their contents
            if filename == '__init__.py':
                continue
            path = os.path.join(directory, filename)
            if path.endswith('.py') and is_empty(path):
                yield path


if __name__ == '__main__':
    print(is_empty(sys.argv[1]))
