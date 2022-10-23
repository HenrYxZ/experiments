import math
import numpy as np
import pyglet
from pyglet import gl
from pyglet.image import ColorBufferImage
from pyglet.window import key

# Change color buffer for single frame app
ColorBufferImage.gl_buffer = gl.GL_FRONT
FRAME_SIZE = 300
PADDING = 50
COLS = 2
ROWS = 2
WIDTH = COLS * (2 * PADDING + FRAME_SIZE)
HEIGHT = ROWS * (2 * PADDING + FRAME_SIZE)
MAX_R = 100
SAMPLES = 1500


rng = np.random.default_rng()
window = pyglet.window.Window(WIDTH, HEIGHT, caption="Random Distribution")
batch = pyglet.graphics.Batch()


class Experiment:
    def __init__(self, name, points, position=(0, 0)):
        x, y = position
        n = len(points[0])
        xs, ys = points
        xs = xs + x + PADDING
        ys = ys + y + PADDING
        self.label = pyglet.text.Label(
            name + f" [n = {n}]", x=x+(PADDING+FRAME_SIZE//2), y=y+PADDING//2,
            bold=True, anchor_x='center', batch=batch
        )

        single_list_points = []
        for i in range(n):
            single_list_points.append(xs[i])
            single_list_points.append(ys[i])
        colors = [255] * 3 * n
        self.vertex_list = batch.add(
            n, pyglet.gl.GL_POINTS, None,
            ('v2i', single_list_points), ('c3B', colors)
        )


def random_r():
    radiuses = rng.random(SAMPLES) * MAX_R
    return radiuses


def random_sqrt_r():
    radiuses = np.sqrt(rng.random(SAMPLES)) * MAX_R
    return radiuses


def random_polar_sample(generate_radiuses_func):
    radiuses = generate_radiuses_func()
    thetas = rng.random(SAMPLES) * 2 * np.pi
    xs = radiuses * np.cos(thetas)
    ys = radiuses * np.sin(thetas)
    xs = np.floor(xs + FRAME_SIZE // 2).astype(int)
    ys = np.floor(ys + FRAME_SIZE // 2).astype(int)
    return xs, ys


def random_rejection_box_sample():
    xs = rng.random(SAMPLES) * 2 * MAX_R
    ys = rng.random(SAMPLES) * 2 * MAX_R
    points = []
    for i in range(SAMPLES):
        x = xs[i]
        y = ys[i]
        if (x - MAX_R) ** 2 + (y - MAX_R) ** 2 <= MAX_R ** 2:
            points.append((x, y))

    new_xs = np.zeros(len(points), dtype=int)
    new_ys = np.zeros(len(points), dtype=int)
    for i, p in enumerate(points):
        new_xs[i] = math.floor(p[0])
        new_ys[i] = math.floor(p[1])
    # Correct difference between frame size and maximum radius
    new_xs = new_xs + FRAME_SIZE // 2 - MAX_R
    new_ys = new_ys + FRAME_SIZE // 2 - MAX_R
    return new_xs, new_ys


def random_repeat_box_sample():
    xs = rng.random(SAMPLES) * 2 * MAX_R
    ys = rng.random(SAMPLES) * 2 * MAX_R
    i = 0
    new_xs = np.zeros(SAMPLES, dtype=int)
    new_ys = np.zeros(SAMPLES, dtype=int)
    while i < SAMPLES:
        x = xs[i]
        y = ys[i]
        while (x - MAX_R) ** 2 + (y - MAX_R) ** 2 > MAX_R ** 2:
            x = rng.random() * FRAME_SIZE
            y = rng.random() * FRAME_SIZE
        new_xs[i] = math.floor(x)
        new_ys[i] = math.floor(y)
        i += 1
    # Correct difference between frame size and maximum radius
    new_xs = new_xs + FRAME_SIZE // 2 - MAX_R
    new_ys = new_ys + FRAME_SIZE // 2 - MAX_R
    return new_xs, new_ys


@window.event
def on_draw():
    pyglet.gl.glClearColor(0, 0, 0, 1)
    window.clear()
    batch.draw()


def on_key_press(symbol, _):
    if symbol == key.S:
        pyglet.image.get_buffer_manager().get_color_buffer().save(
            "screenshot.png"
        )


if __name__ == '__main__':
    window.push_handlers(on_key_press)
    r_points = random_polar_sample(random_r)
    r_sq_points = random_polar_sample(random_sqrt_r)
    box_rej_points = random_rejection_box_sample()
    box_rep_points = random_repeat_box_sample()
    # Add offsets
    offset_r = [0, 2 * PADDING + FRAME_SIZE]
    offset_r_sq = [2 * PADDING + FRAME_SIZE, 2 * PADDING + FRAME_SIZE]
    offset_box_rej = [0, 0]
    offset_box_rep = [2 * PADDING + FRAME_SIZE, 0]
    # Create each experiments
    experiment_r = Experiment(
        "r = random()", r_points, position=offset_r
    )
    experiment_r_sq = Experiment(
        "r = sqrt(random())", r_sq_points, position=offset_r_sq
    )
    experiment_box_rej = Experiment(
        "box reject", box_rej_points, position=offset_box_rej
    )
    experiment_box_rep = Experiment(
        "box repeat", box_rep_points, position=offset_box_rep
    )
    pyglet.app.run()
