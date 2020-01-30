import random

import PIL.Image
import PIL.ImageDraw

bg_fill = (0xF0, 0xF0, 0xF0)
SIZE = 5
UPSCALE = 70


def hsv_to_rgb(hue, saturation, value):
    # https://www.rapidtables.com/convert/color/hsv-to-rgb.html
    C = value * saturation
    X = C * (1 - abs((hue / 60) % 2 - 1))
    m = value - C

    if 0 <= hue < 60:
        r, g, b = C, X, 0
    elif 60 <= hue < 120:
        r, g, b = X, C, 0
    elif 120 <= hue < 180:
        r, g, b = 0, C, X
    elif 180 <= hue < 240:
        r, g, b = 0, X, C
    elif 240 <= hue < 300:
        r, g, b = X, 0, C
    elif 300 <= hue < 360:
        r, g, b = C, 0, X
    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)


# saturation, value
# 39, 88
# 56, 84
# 35, 89
# 41, 83
# 59, 84
# 61, 85
# 44, 88
# 32, 86
# 48, 87
# 55, 77
# 48, 82
# 53, 77
# 41, 83
# 45, 83
# 65, 85
# 32, 85
# 34, 89
def pick_color():
    return hsv_to_rgb(
        hue=random.randint(0, 359),
        saturation=random.randint(30, 65) / 100,
        value=random.randint(75, 90) / 100,
    )


def main():
    fg_fill = pick_color()
    img = PIL.Image.new('RGB', (SIZE, SIZE))
    draw = PIL.ImageDraw.Draw(img)
    draw.rectangle(((0, 0), img.size), fill=bg_fill)

    for x in range(SIZE // 2 + 1):
        for y in range(SIZE):
            if random.randint(0, 1):
                img.putpixel((x, y), fg_fill)
                img.putpixel((SIZE - x - 1, y), fg_fill)
    img = img.resize((SIZE * UPSCALE, SIZE * UPSCALE))
    canvas = PIL.Image.new('RGB', ((SIZE + 1) * UPSCALE, (SIZE + 1) * UPSCALE))
    draw = PIL.ImageDraw.Draw(canvas)
    draw.rectangle(((0, 0), canvas.size), fill=bg_fill)
    canvas.paste(img, (UPSCALE // 2, UPSCALE // 2))
    canvas.show()


if __name__ == '__main__':
    main()
