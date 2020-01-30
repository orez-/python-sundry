import colorsys


def hue_cycle(r, g, b):
    _, s, v = colorsys.rgb_to_hsv(r, g, b)
    for i in range(256):
        yield colorsys.hsv_to_rgb(i / 256, s, v)


def print_hue_cycle(r, g, b):
    termcolor = "\033[48;2;{:.0f};{:.0f};{:.0f}m \033[0m".format
    cycle = hue_cycle(r, g, b)
    for color in cycle:
        print(end=termcolor(*color))
    print()


if __name__ == '__main__':
    print_hue_cycle(10, 20, 240)
