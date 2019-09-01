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

    stride = ceil(1 / factor)
    interpolation = np.mod(quotients[:-stride], 1)

    lefts = indices[:-stride]
    rights = lefts + 1
    return lerp(samples[lefts], samples[rights], interpolation)


def change_speed2(samples, factor=2.):
    result = np.zeros(ceil(len(samples) / factor))
    quotients = np.linspace(0, len(samples) - 1, len(result))
    indices = np.floor(quotients).astype(np.int)
    interpolations = np.mod(quotients, 1)
    for i, (left, interp) in enumerate(zip(indices[:-1], interpolations)):
        result[i] = lerp(samples[left], samples[left + 1], interp)
    return result


def change_speed_square(samples, factor=2.):
    result = np.zeros(ceil(len(samples) / factor))
    quotients = np.arange(0, len(result)) * factor
    indices = np.floor(quotients).astype(np.int)

    return samples[indices]
