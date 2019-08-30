import numpy as np


def lerp(a, b, t):
    return (1 - t) * a + t * b


def quad_interpolate(a, b, c, t):
    ab = lerp(a, b, t)
    bc = lerp(b, c, t)
    return lerp(ab, bc, t)


def muffle(samples):
    lerped = lerp(samples[:-1], samples[1:], 0.5)
    return np.concatenate([samples[0:1], lerped])
