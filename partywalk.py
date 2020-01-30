import itertools
import sys
import time

af = '\x1b[38;5;{}m'
ab = '\x1b[48;5;{}m'
clear = '\x1b[0m'
up = "\033[1A"


def cycle_from(iterable, index):
    cycle = itertools.cycle(iterable)
    for _ in range(index):
        next(cycle)
    return cycle


def main():
    message = "Oh man\nIt's a party."
    if len(sys.argv) > 1:
        message = sys.argv[1]

    lines = message.split('\n')

    print(message)

    colors = [9, 3, 11, 10, 12, 5]

    try:
        while True:
            # reverse is left to right
            for start in range(len(colors))[::-1]:
                print(up * len(lines), end="")
                for line in lines:
                    color_loop = cycle_from(colors, start)
                    # subtle: color_loop should go second,
                    # so we don't pop an extra when we exhaust `line`
                    line = ''.join(af.format(color) + char for char, color in zip(line, color_loop))
                    print("\r", line, clear, sep='')
                sys.stdout.flush()
                time.sleep(0.1)
    except (KeyboardInterrupt, EOFError):
        pass


if __name__ == '__main__':
    main()
