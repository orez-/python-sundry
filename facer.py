import colorsys
import random

import PIL.Image
import PIL.ImageDraw

bg_fill = (0xF0, 0xF0, 0xF0)
SIZE = 5
UPSCALE = 70


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
    return rgb_to_bytes(colorsys.hsv_to_rgb(
        random.randint(0, 359),
        random.randint(30, 65) / 100,
        random.randint(75, 90) / 100,
    ))


def rgb_to_bytes(rgb):
    r, g, b = rgb
    return int(r * 255), int(g * 255), int(b * 255)


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
    img = img.resize((SIZE * UPSCALE, SIZE * UPSCALE), resample=PIL.Image.NEAREST)

    # Add padding
    canvas = PIL.Image.new('RGB', ((SIZE + 1) * UPSCALE, (SIZE + 1) * UPSCALE))
    draw = PIL.ImageDraw.Draw(canvas)
    draw.rectangle(((0, 0), canvas.size), fill=bg_fill)
    canvas.paste(img, (UPSCALE // 2, UPSCALE // 2))
    canvas.show()


if __name__ == '__main__':
    main()
