from __future__ import print_function

import sys
import time

af = '\x1b[38;5;{}m'
ab = '\x1b[48;5;{}m'
clear = '\x1b[0m'
up = "\033[1A"


message = "Oh man\nIt's a party."
if len(sys.argv) > 1:
    message = sys.argv[1]

lines = message.split('\n')

print(message)

try:
    while True:
        for i in xrange(14):
            print(up * len(lines), end="")
            for line in lines:
                print("\r", af.format(i), line, clear, sep='')
            time.sleep(0.0625)
except (KeyboardInterrupt, EOFError):
    pass
