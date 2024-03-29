from math import sqrt
from numba import njit
import numpy as np
from PIL import Image


import utils

RES_SCALE = 5
SCREEN_WIDTH = 280 * RES_SCALE
SCREEN_HEIGHT = 210 * RES_SCALE
COLOR_CHANNELS = 3
AA_H_SAMPLES = 3
AA_V_SAMPLES = 3
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
MAX_COLOR_VALUE = 255.0
MAT_COL = np.array((128 / MAX_COLOR_VALUE, 0.0, 128 / MAX_COLOR_VALUE))
C0 = MAT_COL * 0.2     # Lowest possible material color
BG_COLOR = np.zeros(COLOR_CHANNELS)
LIGHT_DIR = utils.normalize(np.array([-0.3, 1.0, -0.5]))


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
def intersect(pp, nr, pos, radius):
    diff = pp - pos
    b = np.dot(nr, diff)
    c = np.dot(diff, diff) - radius ** 2
    discriminant = b ** 2 - c
    if b > 0 or discriminant < 0:
        return -1.0
    t = -b - sqrt(discriminant)
    return t


@njit(fastmath=True)
def render(h, w, sx, sy, proj_dist, cam_pos, cam_coords, radius):
    arr = np.zeros(
        (h, w, COLOR_CHANNELS), dtype=np.uint8
    )
    n0, n1, n2 = cam_coords
    p00 = cam_pos + (n0 * (-sx / 2) + n1 * (-sy / 2) + n2 * proj_dist)
    for j in range(h):
        for i in range(w):
            color = np.zeros(COLOR_CHANNELS)
            for n in range(AA_V_SAMPLES):
                for m in range(AA_H_SAMPLES):
                    offsets = np.random.random(2)
                    pixel_coords = (
                        i + (m + offsets[0]) / AA_H_SAMPLES,
                        j + (n + offsets[1]) / AA_V_SAMPLES
                    )
                    # Project pixel to point in 3D coordinates
                    pp = project_pixel(
                        sx, sy, n0, n1, h, w, pixel_coords, p00
                    )
                    # Shoot ray
                    nr = utils.normalize(pp - cam_pos)
                    t = intersect(cam_pos, nr, SPHERE_POS, radius)
                    if t > 0:
                        p_hit = cam_pos + nr * t
                        normal = utils.normalize(p_hit - SPHERE_POS)
                        color += np.maximum(
                            np.dot(normal, LIGHT_DIR) * MAT_COL, C0
                        )
                    else:
                        color += BG_COLOR
            color = (color * MAX_COLOR_VALUE) / AA_SAMPLES
            arr[j, i] = color.astype(np.uint8)
    return arr


def main():
    timer = utils.Timer()
    with timer:
        arr = render(
            SCREEN_HEIGHT, SCREEN_WIDTH, SX, SY,
            PROJ_DIST, CAM_POS, CAM_COORDS, RADIUS
        )
    img = Image.fromarray(arr)
    img_path = "docs/nrt_output.png"
    img.save(img_path)
    print(f"Finished rendering and saved image in {img_path}")


if __name__ == '__main__':
    main()
