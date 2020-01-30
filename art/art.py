import collections
import functools
import math
import random

import imageio
import numpy
# import PIL.Image

SEED = random.random()
det_random = random.Random()


def clamp(low, value, high):
    return sorted((low, value, high))[1]


def bounce_clamp(low, position, velocity, high):
    next_pos = position + velocity
    if next_pos < low:
        return 2 * low - next_pos, -velocity
    if next_pos > high:
        return 2 * high - next_pos, -velocity
    return next_pos, velocity


class Board:
    def __init__(self, width, height, noise, colors=None):
        self.width = width
        self.height = height
        self.colors = colors or {}
        self.noise = noise

    def adjacent(self, x, y):
        yield x, (y - 1) % self.height
        yield (x + 1) % self.width, y
        yield x, (y + 1) % self.height
        yield (x - 1) % self.width, y

    def color_at(self, x, y):
        if (x, y) not in self.colors:
            return (0, 0, 0)
        return self.colors[x, y]
        # if self.noise is None:

        # r, g, b = self.colors[x, y]
        # return (
        #     clamp(0, r + self.noise[y, x, 0], 255),
        #     clamp(0, g + self.noise[y, x, 1], 255),
        #     clamp(0, b + self.noise[y, x, 2], 255),
        # )

    def set_color(self, x, y, color):
        self.colors[x, y] = color
        if self.noise is not None:
            self._apply_noise(x, y)

    def _apply_noise(self, x, y):
        self.colors[x, y] = tuple(
            clamp(0, c + n, 255)
            for c, n in zip(self.colors[x, y], self.noise[y, x])
        )

    def ratio_complete(self):
        return len(self.colors) / (self.width * self.height)

    def percent_complete(self):
        return f"{self.ratio_complete():8.3%}"

    def apply_noise(self, noise):
        if self.noise is not None:
            raise Exception("can't override noise")
        self.noise = noise
        for (x, y) in self.colors:
            self._apply_noise(x, y)

    def clone(self):
        return Board(
            width=self.width,
            height=self.height,
            noise=self.noise,  # !!
            colors=dict(self.colors),
        )


# def bfs_steps(board, start, value):
#     next_queue = collections.deque([start])
#     queue = collections.deque()

#     while next_queue:
#         # Avoid reallocating queues. `queue` is guaranteed empty, so swap em!
#         queue, next_queue = next_queue, queue
#         while queue:
#             x, y = queue.popleft()
#             if (x, y) in board.colors:
#                 continue
#             board.set_color(x, y, value)

#             for coord in board.adjacent(x, y):
#                 if coord not in board.colors:
#                     next_queue.append(coord)
#         yield len(next_queue)

def bfs_steps(board, start, value):
    SPEND = 3
    x, y = start
    next_queue = collections.deque([(x, y, SPEND)])
    queue = collections.deque()

    while next_queue:
        # Avoid reallocating queues. `queue` is guaranteed empty, so swap em!
        queue, next_queue = next_queue, queue
        while queue:
            x, y, spend = queue.popleft()
            if (x, y) in board.colors:
                continue
            board.set_color(x, y, value)

            for x, y in board.adjacent(x, y):
                if (x, y) in board.colors:
                    continue

                next_spend = spend - random.randint(1, 3)
                if next_spend < 0:
                    next_queue.append((x, y, SPEND))
                else:
                    queue.append((x, y, next_spend))
        yield len(next_queue)


# def board_walker(board):
#     MAX_VELOCITY = 5
#     x = random.randrange(board.width)
#     y = random.randrange(board.height)
#     vx = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
#     vy = random.randint(-MAX_VELOCITY, MAX_VELOCITY)

#     while True:
#         vx = clamp(-MAX_VELOCITY, vx + random.randint(-1, 1), MAX_VELOCITY)
#         vy = clamp(-MAX_VELOCITY, vy + random.randint(-1, 1), MAX_VELOCITY)
#         x += vx
#         y += vy
#         x %= board.width
#         y %= board.height
#         yield x, y


def board_walker(board):
    MAX_ACCELERATION = 2
    MAX_VELOCITY = 5
    MAX_VELOCITY2 = MAX_VELOCITY * MAX_VELOCITY
    x = random.randrange(board.width)
    y = random.randrange(board.height)
    vx = 0
    vy = 0

    while True:
        angle = math.tau * random.random()
        radius = MAX_ACCELERATION * math.sqrt(random.random())
        ax = radius * math.cos(angle)
        ay = radius * math.sin(angle)

        vx += ax
        vy += ay
        magnitude2 = vx * vx + vy * vy
        if magnitude2 > MAX_VELOCITY2:
            modifier = MAX_VELOCITY / math.sqrt(magnitude2)
            vx *= modifier
            vy *= modifier

        x = (x + vx) % board.width
        y = (y + vy) % board.height
        yield round(x) % board.width, round(y) % board.height


# def color_walker():
#     while True:
#         for c in range(31, 255, 7):
#             yield (c, 31, 31)
#         for c in range(255, 31, -7):
#             yield (c, 31, 31)


# def color_walker():
#     MAX_VELOCITY = 2
#     r, g, b = (random.randint(31, 255) for _ in range(3))
#     vr, vg, vb = (random.randint(-MAX_VELOCITY, MAX_VELOCITY) for _ in range(3))
#     while True:
#         vr = clamp(-MAX_VELOCITY, vr + random.randint(-1, 1), MAX_VELOCITY)
#         vg = clamp(-MAX_VELOCITY, vg + random.randint(-1, 1), MAX_VELOCITY)
#         vb = clamp(-MAX_VELOCITY, vb + random.randint(-1, 1), MAX_VELOCITY)
#         r = clamp(31, r + vr, 255)
#         g = clamp(31, g + vg, 255)
#         b = clamp(31, b + vb, 255)
#         yield r, g, b


def color_walker():
    ACCELERATION = 1
    tr, tg, tb = (random.randint(31, 255) for _ in range(3))
    r, g, b = (random.randint(31, 255) for _ in range(3))
    vr, vg, vb = (random.randint(-3, 3) for _ in range(3))

    repeats = range(100)

    while True:
        for _ in repeats:
            vr += 0 if tr == r else -ACCELERATION if tr < r else ACCELERATION
            vg += 0 if tg == g else -ACCELERATION if tg < g else ACCELERATION
            vb += 0 if tb == b else -ACCELERATION if tb < b else ACCELERATION

            r, vr = bounce_clamp(31, r, vr, 255)
            g, vg = bounce_clamp(31, g, vg, 255)
            b, vb = bounce_clamp(31, b, vb, 255)

        repeats = range(1)
        for _ in range(5):
            yield round(r), round(g), round(b)

# def paint():
#     WIDTH = 800
#     HEIGHT = 600
#     board = Board(WIDTH, HEIGHT)

#     colors = color_walker()
#     walker = board_walker(board)
#     pens = [iter([])]

#     while pens:
#         pens.append(bfs_steps(board, next(walker), next(colors)))
#         pens = [pen for pen in pens if next(pen, 0)]

#     return board

def paint_by_step(width, height, noise=None):
    board = Board(width, height, noise=noise)

    colors = color_walker()
    walker = board_walker(board)
    pens = [iter([])]
    # pens = [bfs_steps(board, next(walker), next(colors)) for _ in range(10)]

    while pens:
        for _ in range(64):
            pens.append(bfs_steps(board, next(walker), next(colors)))
        pens = [pen for pen in pens if next(pen, 0)]
        yield board


def render_image(board):
    image = PIL.Image.new('RGB', (board.width, board.height))
    image.putdata(
        [
            board.colors.get((x, y), (0, 0, 0))
            for y in range(board.height)
            for x in range(board.width)
        ]
    )

    return image


def render_numpy(board):
    return numpy.fromiter(
        (
            c
            for y in range(board.height)
            for x in range(board.width)
            for c in board.color_at(x, y)
        ),
        dtype=numpy.uint8,
        count=board.height * board.width * 3,
    ).reshape(board.height, board.width, 3)


def lerp(a, b, perc):
    return (1 - perc) * a + perc * b


@functools.lru_cache()
def deterministic_random(*seed):
    det_random.seed((SEED, *seed))
    return det_random.random()


# @functools.lru_cache()
def perlin_noise_value(x, y, *meta):
    POWER_MIN = 2
    POWER_MAX = 5
    total = 0
    for power in range(POWER_MIN, POWER_MAX):
        amplitude = 2 ** power

        int_x, frac_x = divmod(x / amplitude, 1)
        int_y, frac_y = divmod(y / amplitude, 1)

        n0 = deterministic_random(int_x, int_y, power, *meta)
        n1 = deterministic_random(int_x + 1, int_y, power, *meta)
        ix0 = lerp(n0, n1, frac_x)

        n0 = deterministic_random(int_x, int_y + 1, power, *meta)
        n1 = deterministic_random(int_x + 1, int_y + 1, power, *meta)
        ix1 = lerp(n0, n1, frac_x)

        total += lerp(ix0, ix1, frac_y) * amplitude

    return total / ((2 ** POWER_MAX) - (2 ** POWER_MIN))


def generate_gif():
    width = 800
    height = 600
    print("loading noise, this is slow i think because i implemented it bad")
    noise = get_perlin1(width, height, 16)
    print("aight got noise")
    # noise = get_static(width, height, 8)
    images = []
    with imageio.get_writer('display.gif', mode='I') as writer:
        try:
            for i, board in enumerate(paint_by_step(width, height, noise=noise)):
                # if i % 4 == 0:
                writer.append_data(render_numpy(board))
                print(board.percent_complete())
        except KeyboardInterrupt:
            pass
        # writer.append_data(render_numpy(board), meta={'duration': 10000})

    imageio.imwrite("final.png", render_numpy(board))


def compare_noise():
    width = 800
    height = 600

    print("loading noise, this is slow i think because i implemented it bad")
    print("noise1")
    perlin1 = get_perlin1(width, height, 8)
    print("noise3")
    perlin3 = get_perlin3(width, height, 8)
    print("static")
    static = get_static(width, height, 2)
    print("combos")
    p1stat = perlin1 + static
    p3stat = perlin3 + static
    print("aight got noise. painting the board")

    for board in paint_by_step(width, height):
        ...

    print("painted. time for filters")
    imageio.imwrite(f"original.png", render_numpy(board))
    print("did original")
    for filename, noise in [("perlin1", perlin1), ("perlin3", perlin3), ("static", static), ("p1stat", p1stat), ("p3stat", p3stat)]:
        noise_board = board.clone()
        noise_board.apply_noise(noise)
        imageio.imwrite(f"{filename}.png", render_numpy(noise_board))
        print(f"did {filename}")


def get_perlin1(width, height, variance):
    variance2 = variance * 2
    return numpy.fromiter(
        (
            c
            for y in range(height)
            for x in range(width)
            for c in [int(perlin_noise_value(x, y, 0) * variance2) - variance] * 3
        ),
        dtype=numpy.int8,
        count=height * width * 3,
    ).reshape(height, width, 3)


def get_perlin3(width, height, variance):
    variance2 = variance * 2
    return numpy.fromiter(
        (
            int(perlin_noise_value(x, y, c) * variance2) - variance
            for y in range(height)
            for x in range(width)
            for c in range(3)
        ),
        dtype=numpy.int8,
        count=height * width * 3,
    ).reshape(height, width, 3)


def get_static(width, height, variance):
    return numpy.fromiter(
        (
            random.randint(-variance, variance)
            for y in range(height)
            for x in range(width)
            for c in range(3)
        ),
        dtype=numpy.int8,
        count=height * width * 3,
    ).reshape(height, width, 3)


if __name__ == '__main__':
    # board = paint()
    # render(board).show()

    # generate_gif()

    compare_noise()
