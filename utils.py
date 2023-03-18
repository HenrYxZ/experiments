from numba import njit
import numpy as np
import time


@njit
def normalize(arr):
    """
    Normalize a vector using numpy.
    Args:
        arr (ndarray): Input vector
    Returns:
        ndarray: Normalized input vector
    """
    norm = np.linalg.norm(arr)
    if norm == 0.0:
        return arr
    return arr / norm


def humanize_time(secs):
    minutes, secs = divmod(secs, 60)
    hours, minutes = divmod(minutes, 60)
    return '%02d:%02d:%02d' % (hours, minutes, secs)


class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        print(self)

    def __str__(self):
        return f"Finished in {self.elapsed_time:,} seconds"
