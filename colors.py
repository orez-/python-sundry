# -*- coding: utf8 -*-
from __future__ import division
from __future__ import print_function
import random


sep = "■"
af = '\x1b[38;5;{}m'
ab = '\x1b[48;5;{}m'
clear = '\x1b[0m'

def rando():
    print(''.join(
        ''.join([af, ab, sep]).format(random.randint(0, 256), random.randint(0, 256))
        for _ in range(1000)),
        end=''
    )
    print(clear)

def spectrum():
    # print(' '.join(map(ab.format, range(256))))
    for i in range(256):
        print(af.format(i), end=str(i % 10))
    print(clear)

def sample():
    sampler()
    print()

    for num in range(226, 0, -42):
        print(ab.format(num), end=str(num) + " ")
    print(clear)

    for num in range(231, 0, -43):
        print(ab.format(num), end=str(num) + " ")
    print(clear)

    for num in range(231 + 226, 0, -int(42.5 * 2)):
        print(ab.format(num // 2), end=str(num // 2) + " ")
    print(clear)

    # blue
    for num in [18, 19, 20, 21, 27, 33, 39]:
        print(ab.format(num), end=str(num) + " ")
    print(clear)

    # purple
    for num in range(56, 255, 42):
        print(ab.format(num), end=str(num) + " ")
    print(clear)

    # sunrise
    for num in range(91, 232, 41):
        print(ab.format(num), end=str(num) + " ")
    print(clear)

    # orange
    for num in color_range('804400', 'ff8800', 4):
        print(ab.format(num), end=str(num) + " ")
    print(clear)

    # green
    for num in color_range('008800', '00ff88', 4):
        print(ab.format(num), end=str(num) + " ")
    print(clear)

    # blue
    for num in color_range('000088', '0088ff', 4):
        print(ab.format(num), end=str(num) + " ")
    print(clear)

    # gray
    for num in color_range('666666', 'cccccc', 4):
        print(ab.format(num), end=str(num) + " ")
    print(clear)


def sampler(filter_fn=lambda x: True):
    start = 0
    for end in [16, 52, 88, 124, 160, 196, 232, 256]:
        for i in range(start, end):
            color = clear
            if filter_fn(i):
                color = ab.format(i)
            print(color, end=str(i % 10 or i % 100 // 10))
        start = end
        print(clear)


def closest(color):
    """
    Given a rgb tuple, get the most similar terminal color value.
    """
    d = {
        0: hex_to_tuple('000000'),
        1: hex_to_tuple('800000'),
        2: hex_to_tuple('008000'),
        3: hex_to_tuple('808000'),
        4: hex_to_tuple('000080'),
        5: hex_to_tuple('800080'),
        6: hex_to_tuple('008080'),
        7: hex_to_tuple('c0c0c0'),

        8: hex_to_tuple('808080'),
        9: hex_to_tuple('ff0000'),
        10: hex_to_tuple('00ff00'),
        11: hex_to_tuple('ffff00'),
        12: hex_to_tuple('0000ff'),
        13: hex_to_tuple('ff00ff'),
        14: hex_to_tuple('00ffff'),
        15: hex_to_tuple('ffffff'),

        16: hex_to_tuple('000000'),
        17: hex_to_tuple('00005f'),
        18: hex_to_tuple('000087'),
        19: hex_to_tuple('0000af'),
        20: hex_to_tuple('0000d7'),
        21: hex_to_tuple('0000ff'),

        22: hex_to_tuple('005f00'),
        23: hex_to_tuple('005f5f'),
        24: hex_to_tuple('005f87'),
        25: hex_to_tuple('005faf'),
        26: hex_to_tuple('005fd7'),
        27: hex_to_tuple('005fff'),

        28: hex_to_tuple('008700'),
        29: hex_to_tuple('00875f'),
        30: hex_to_tuple('008787'),
        31: hex_to_tuple('0087af'),
        32: hex_to_tuple('0087d7'),
        33: hex_to_tuple('0087ff'),

        34: hex_to_tuple('00af00'),
        35: hex_to_tuple('00af5f'),
        36: hex_to_tuple('00af87'),
        37: hex_to_tuple('00afaf'),
        38: hex_to_tuple('00afd7'),
        39: hex_to_tuple('00afff'),

        40: hex_to_tuple('00d700'),
        41: hex_to_tuple('00d75f'),
        42: hex_to_tuple('00d787'),
        43: hex_to_tuple('00d7af'),
        44: hex_to_tuple('00d7d7'),
        45: hex_to_tuple('00d7ff'),

        46: hex_to_tuple('00ff00'),
        47: hex_to_tuple('00ff5f'),
        48: hex_to_tuple('00ff87'),
        49: hex_to_tuple('00ffaf'),
        50: hex_to_tuple('00ffd7'),
        51: hex_to_tuple('00ffff'),

        52: hex_to_tuple('5f0000'),
        53: hex_to_tuple('5f005f'),
        54: hex_to_tuple('5f0087'),
        55: hex_to_tuple('5f00af'),
        56: hex_to_tuple('5f00d7'),
        57: hex_to_tuple('5f00ff'),

        58: hex_to_tuple('5f5f00'),
        59: hex_to_tuple('5f5f5f'),
        60: hex_to_tuple('5f5f87'),
        61: hex_to_tuple('5f5faf'),
        62: hex_to_tuple('5f5fd7'),
        63: hex_to_tuple('5f5fff'),

        64: hex_to_tuple('5f8700'),
        65: hex_to_tuple('5f875f'),
        66: hex_to_tuple('5f8787'),
        67: hex_to_tuple('5f87af'),
        68: hex_to_tuple('5f87d7'),
        69: hex_to_tuple('5f87ff'),

        70: hex_to_tuple('5faf00'),
        71: hex_to_tuple('5faf5f'),
        72: hex_to_tuple('5faf87'),
        73: hex_to_tuple('5fafaf'),
        74: hex_to_tuple('5fafd7'),
        75: hex_to_tuple('5fafff'),

        76: hex_to_tuple('5fd700'),
        77: hex_to_tuple('5fd75f'),
        78: hex_to_tuple('5fd787'),
        79: hex_to_tuple('5fd7af'),
        80: hex_to_tuple('5fd7d7'),
        81: hex_to_tuple('5fd7ff'),

        82: hex_to_tuple('5fff00'),
        83: hex_to_tuple('5fff5f'),
        84: hex_to_tuple('5fff87'),
        85: hex_to_tuple('5fffaf'),
        86: hex_to_tuple('5fffd7'),
        87: hex_to_tuple('5fffff'),

        88: hex_to_tuple('870000'),
        89: hex_to_tuple('87005f'),
        90: hex_to_tuple('870087'),
        91: hex_to_tuple('8700af'),
        92: hex_to_tuple('8700d7'),
        93: hex_to_tuple('8700ff'),

        94: hex_to_tuple('875f00'),
        95: hex_to_tuple('875f5f'),
        96: hex_to_tuple('875f87'),
        97: hex_to_tuple('875faf'),
        98: hex_to_tuple('875fd7'),
        99: hex_to_tuple('875fff'),

        100: hex_to_tuple('878700'),
        101: hex_to_tuple('87875f'),
        102: hex_to_tuple('878787'),
        103: hex_to_tuple('8787af'),
        104: hex_to_tuple('8787d7'),
        105: hex_to_tuple('8787ff'),

        106: hex_to_tuple('87af00'),
        107: hex_to_tuple('87af5f'),
        108: hex_to_tuple('87af87'),
        109: hex_to_tuple('87afaf'),
        110: hex_to_tuple('87afd7'),
        111: hex_to_tuple('87afff'),

        112: hex_to_tuple('87d700'),
        113: hex_to_tuple('87d75f'),
        114: hex_to_tuple('87d787'),
        115: hex_to_tuple('87d7af'),
        116: hex_to_tuple('87d7d7'),
        117: hex_to_tuple('87d7ff'),

        118: hex_to_tuple('87ff00'),
        119: hex_to_tuple('87ff5f'),
        120: hex_to_tuple('87ff87'),
        121: hex_to_tuple('87ffaf'),
        122: hex_to_tuple('87ffd7'),
        123: hex_to_tuple('87ffff'),

        124: hex_to_tuple('af0000'),
        125: hex_to_tuple('af005f'),
        126: hex_to_tuple('af0087'),
        127: hex_to_tuple('af00af'),
        128: hex_to_tuple('af00d7'),
        129: hex_to_tuple('af00ff'),

        130: hex_to_tuple('af5f00'),
        131: hex_to_tuple('af5f5f'),
        132: hex_to_tuple('af5f87'),
        133: hex_to_tuple('af5faf'),
        134: hex_to_tuple('af5fd7'),
        135: hex_to_tuple('af5fff'),

        136: hex_to_tuple('af8700'),
        137: hex_to_tuple('af875f'),
        138: hex_to_tuple('af8787'),
        139: hex_to_tuple('af87af'),
        140: hex_to_tuple('af87d7'),
        141: hex_to_tuple('af87ff'),

        142: hex_to_tuple('afaf00'),
        143: hex_to_tuple('afaf5f'),
        144: hex_to_tuple('afaf87'),
        145: hex_to_tuple('afafaf'),
        146: hex_to_tuple('afafd7'),
        147: hex_to_tuple('afafff'),

        148: hex_to_tuple('afd700'),
        149: hex_to_tuple('afd75f'),
        150: hex_to_tuple('afd787'),
        151: hex_to_tuple('afd7af'),
        152: hex_to_tuple('afd7d7'),
        153: hex_to_tuple('afd7ff'),

        154: hex_to_tuple('afff00'),
        155: hex_to_tuple('afff5f'),
        156: hex_to_tuple('afff87'),
        157: hex_to_tuple('afffaf'),
        158: hex_to_tuple('afffd7'),
        159: hex_to_tuple('afffff'),

        160: hex_to_tuple('d70000'),
        161: hex_to_tuple('d7005f'),
        162: hex_to_tuple('d70087'),
        163: hex_to_tuple('d700af'),
        164: hex_to_tuple('d700d7'),
        165: hex_to_tuple('d700ff'),

        166: hex_to_tuple('d75f00'),
        167: hex_to_tuple('d75f5f'),
        168: hex_to_tuple('d75f87'),
        169: hex_to_tuple('d75faf'),
        170: hex_to_tuple('d75fd7'),
        171: hex_to_tuple('d75fff'),

        172: hex_to_tuple('d78700'),
        173: hex_to_tuple('d7875f'),
        174: hex_to_tuple('d78787'),
        175: hex_to_tuple('d787af'),
        176: hex_to_tuple('d787d7'),
        177: hex_to_tuple('d787ff'),

        178: hex_to_tuple('d7af00'),
        179: hex_to_tuple('d7af5f'),
        180: hex_to_tuple('d7af87'),
        181: hex_to_tuple('d7afaf'),
        182: hex_to_tuple('d7afd7'),
        183: hex_to_tuple('d7afff'),

        184: hex_to_tuple('d7d700'),
        185: hex_to_tuple('d7d75f'),
        186: hex_to_tuple('d7d787'),
        187: hex_to_tuple('d7d7af'),
        188: hex_to_tuple('d7d7d7'),
        189: hex_to_tuple('d7d7ff'),

        190: hex_to_tuple('d7ff00'),
        191: hex_to_tuple('d7ff5f'),
        192: hex_to_tuple('d7ff87'),
        193: hex_to_tuple('d7ffaf'),
        194: hex_to_tuple('d7ffd7'),
        195: hex_to_tuple('d7ffff'),

        196: hex_to_tuple('ff0000'),
        197: hex_to_tuple('ff005f'),
        198: hex_to_tuple('ff0087'),
        199: hex_to_tuple('ff00af'),
        200: hex_to_tuple('ff00d7'),
        201: hex_to_tuple('ff00ff'),

        202: hex_to_tuple('ff5f00'),
        203: hex_to_tuple('ff5f5f'),
        204: hex_to_tuple('ff5f87'),
        205: hex_to_tuple('ff5faf'),
        206: hex_to_tuple('ff5fd7'),
        207: hex_to_tuple('ff5fff'),

        208: hex_to_tuple('ff8700'),
        209: hex_to_tuple('ff875f'),
        210: hex_to_tuple('ff8787'),
        211: hex_to_tuple('ff87af'),
        212: hex_to_tuple('ff87d7'),
        213: hex_to_tuple('ff87ff'),

        214: hex_to_tuple('ffaf00'),
        215: hex_to_tuple('ffaf5f'),
        216: hex_to_tuple('ffaf87'),
        217: hex_to_tuple('ffafaf'),
        218: hex_to_tuple('ffafd7'),
        219: hex_to_tuple('ffafff'),

        220: hex_to_tuple('ffd700'),
        221: hex_to_tuple('ffd75f'),
        222: hex_to_tuple('ffd787'),
        223: hex_to_tuple('ffd7af'),
        224: hex_to_tuple('ffd7d7'),
        225: hex_to_tuple('ffd7ff'),

        226: hex_to_tuple('ffff00'),
        227: hex_to_tuple('ffff5f'),
        228: hex_to_tuple('ffff87'),
        229: hex_to_tuple('ffffaf'),
        230: hex_to_tuple('ffffd7'),
        231: hex_to_tuple('ffffff'),

        232: hex_to_tuple('080808'),
        233: hex_to_tuple('121212'),
        234: hex_to_tuple('1c1c1c'),
        235: hex_to_tuple('262626'),
        236: hex_to_tuple('303030'),
        237: hex_to_tuple('3a3a3a'),

        238: hex_to_tuple('444444'),
        239: hex_to_tuple('4e4e4e'),
        240: hex_to_tuple('585858'),
        241: hex_to_tuple('606060'),
        242: hex_to_tuple('666666'),
        243: hex_to_tuple('767676'),

        244: hex_to_tuple('808080'),
        245: hex_to_tuple('8a8a8a'),
        246: hex_to_tuple('949494'),
        247: hex_to_tuple('9e9e9e'),
        248: hex_to_tuple('a8a8a8'),
        249: hex_to_tuple('b2b2b2'),

        250: hex_to_tuple('bcbcbc'),
        251: hex_to_tuple('c6c6c6'),
        252: hex_to_tuple('d0d0d0'),
        253: hex_to_tuple('dadada'),
        254: hex_to_tuple('e4e4e4'),
        255: hex_to_tuple('eeeeee'),
    }

    return min(d.items(), key=lambda kv: sum(
        (coord - color_coord) ** 2
        for coord, color_coord in zip(kv[1], color))
    )[0]

def color_range(start, stop, steps):
    start_hex = hex_to_tuple(start)
    stop_hex = hex_to_tuple(stop)

    colors_hex = zip(*[
        int_tween(start_comp, stop_comp, steps)
        for start_comp, stop_comp in zip(start_hex, stop_hex)
    ])
    return map(closest, colors_hex)


def hex_to_tuple(hex_value):
    return tuple(int(v, 16) for v in (hex_value[:2], hex_value[2:4], hex_value[4:]))


def int_tween(start, stop, steps):
    assert steps > 1
    step = (stop - start) / (steps - 1)

    for i in range(steps):
        yield int(start + round(i * step))


if __name__ == '__main__':
    sample()

    # colors = [
    #     (0, 0, 0),
    #     (1, 0, 103),
    #     (213, 255, 0),
    #     (255, 0, 86),
    #     (158, 0, 142),
    #     (14, 76, 161),
    #     (255, 229, 2),
    #     (0, 95, 57),
    #     (0, 255, 0),
    #     (149, 0, 58),
    #     (255, 147, 126),
    #     (164, 36, 0),
    #     (0, 21, 68),
    #     (145, 208, 203),
    #     (98, 14, 0),
    #     (107, 104, 130),
    #     (0, 0, 255),
    #     (0, 125, 181),
    #     (106, 130, 108),
    #     (0, 174, 126),
    #     (194, 140, 159),
    #     (190, 153, 112),
    #     (0, 143, 156),
    #     (95, 173, 78),
    #     (255, 0, 0),
    #     (255, 0, 246),
    #     (255, 2, 157),
    #     (104, 61, 59),
    #     (255, 116, 163),
    #     (150, 138, 232),
    #     (152, 255, 82),
    #     (167, 87, 64),
    #     (1, 255, 254),
    #     (255, 238, 232),
    #     (254, 137, 0),
    #     (189, 198, 255),
    #     (1, 208, 255),
    #     (187, 136, 0),
    #     (117, 68, 177),
    #     (165, 255, 210),
    #     (255, 166, 254),
    #     (119, 77, 0),
    #     (122, 71, 130),
    #     (38, 52, 0),
    #     (0, 71, 84),
    #     (67, 0, 44),
    #     (181, 0, 255),
    #     (255, 177, 103),
    #     (255, 219, 102),
    #     (144, 251, 146),
    #     (126, 45, 210),
    #     (189, 211, 147),
    #     (229, 111, 254),
    #     (222, 255, 116),
    #     (0, 255, 120),
    #     (0, 155, 255),
    #     (0, 100, 1),
    #     (0, 118, 255),
    #     (133, 169, 0),
    #     (0, 185, 23),
    #     (120, 130, 49),
    #     (0, 255, 198),
    #     (255, 110, 65),
    #     (232, 94, 190),
    # ]

    colors = [
        (0xd9, 0x27, 0x49),
        (0xf2, 0x81, 0x37),
        (0xe7, 0xce, 0x30),
        (0x84, 0xb8, 0x2f),
        (0x3a, 0xa5, 0x90),
        (0x3e, 0x52, 0xcb),
        (0xaf, 0x40, 0x96),

        (0xf7, 0x58, 0x39),
        (0xf3, 0xb7, 0x2f),
        (0x47, 0xad, 0x4b),
        (0x42, 0x8c, 0xb0),
        (0x8c, 0x61, 0xbd),
    ]

    for c in colors:
        close = closest(c)
        print(af.format(close), close, sep='')
