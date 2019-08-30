from math import ceil

import numpy as np

from smoothing import lerp


def reverse(samples):
    return samples[::-1]


def change_speed(samples, factor=2.):
    # Do inverse transform sampling and interpolate from left endpoint to
    # right endpoint by the amount that the "ideal" inverse point is greater
    # than the nearest real point
    result = np.zeros(ceil(len(samples) / factor))
    quotients = np.arange(0, len(result)) * factor
    indices = np.floor(quotients).astype(np.int)

    return lerp(samples[indices[:-1]], samples[indices[1:]], np.mod(quotients[:-1], 1))
