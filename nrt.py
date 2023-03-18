from math import sqrt
from numba import njit
import numpy as np
from PIL import Image


import utils


SCREEN_WIDTH = 280
SCREEN_HEIGHT = 210
COLOR_CHANNELS = 3
AA_H_SAMPLES = 1
AA_V_SAMPLES = 1
AA_SAMPLES = AA_V_SAMPLES * AA_H_SAMPLES

RADIUS = 0.5
SPHERE_POS = np.array((0.0, 0.0, 0.0))
SX = 2.0
SY = 1.5
PROJ_DIST = 2.0
CAM_POS = np.array((0.0, 0.0, -2.0))
CAM_COORDS = np.array((
    (1.0, 0.0, 0.0),    # n0
    (0.0, 1.0, 0.0),    # n1
    (0.0, 0.0, 1.0)     # n2
))
MAT_COL = np.array((128 / 255.0, 0.0, 128 / 255.0))
C0 = MAT_COL * 0.2     # Lowest possible material color
BG_COLOR = np.zeros(COLOR_CHANNELS)
LIGHT_DIR = utils.normalize(np.array([-0.3, 1.0, -0.5]))

rng = np.random.default_rng()


@njit
def project_pixel(sx, sy, n0, n1, h, w, pixel_coords, p00):
    """
    Get the projection point for a given screen pixel

    Args:
        sx:
        sy:
        n0:
        n1:
        h:
        w:
        pixel_coords (tuple[float]):
        p00 (ndarray):

    Returns:
        ndarray: The projection point in 3D coordinates
    """
    xp = (pixel_coords[0] / w) * sx
    yp = ((h - pixel_coords[1]) / h) * sy
    pp = p00 + n0 * xp + n1 * yp
    return pp


@njit
def intersect(pp, nr, pos, radius) -> float:
    diff = pp - pos
    b = np.dot(nr, diff)
    c = np.dot(diff, diff) - radius ** 2
    discriminant = b ** 2 - c
    if b > 0 or discriminant < 0:
        return -1.0
    t = -b - sqrt(discriminant)
    return t


@njit(fastmath=True)
def render(arr, sx, sy, proj_dist, cam_pos, cam_coords, radius):
    h, w, _ = arr.shape
    n0, n1, n2 = cam_coords
    p00 = cam_pos + (n0 * (-sx / 2) + n1 * (-sy / 2) + n2 * proj_dist)
    for j in range(h):
        for i in range(w):
            color = np.zeros(COLOR_CHANNELS)
            for n in range(AA_V_SAMPLES):
                for m in range(AA_H_SAMPLES):
                    offsets = rng.random(2)
                    pixel_coords = (
                        i + (m + offsets[0]) / float(AA_H_SAMPLES),
                        j + (n + offsets[1]) / float(AA_V_SAMPLES)
                    )
                    # Project pixel to point in 3D coordinates
                    pp = project_pixel(
                        sx, sy, n0, n1, h, w, pixel_coords, p00
                    )
                    # Shoot ray
                    nr = utils.normalize(pp - cam_pos)
                    t = intersect(cam_pos, nr, SPHERE_POS, radius)
                    # print(t)
                    if t > 0:
                        p_hit = cam_pos + nr * t
                        n = utils.normalize(p_hit - SPHERE_POS)
                        color += np.maximum(np.dot(n, LIGHT_DIR) * MAT_COL, C0)
                    else:
                        color += BG_COLOR
            color /= AA_SAMPLES
            final_color = np.empty_like(color)
            np.round(color * 255, 0, final_color)
            arr[j, i] = final_color


def main():
    arr = np.zeros(
        (SCREEN_HEIGHT, SCREEN_WIDTH, COLOR_CHANNELS), dtype=np.uint8
    )
    timer = utils.Timer()
    with timer:
        render(arr, SX, SY, PROJ_DIST, CAM_POS, CAM_COORDS, RADIUS)
    img = Image.fromarray(arr)
    img.save("docs/nrt_output.png")
    print("Finished rendering")


if __name__ == '__main__':
    main()
