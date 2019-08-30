import numpy as np


def lerp(a, b, t):
    return (1 - t) * a + t * b


def quad_interpolate(a, b, c, t):
    ab = lerp(a, b, t)
    bc = lerp(b, c, t)
    return lerp(ab, bc, t)


def muffle(audio):
    lerped = lerp(audio.samples[:-1], audio.samples[1:], 0.5)
    return audio.set_samples(np.concatenate([audio.samples[0:1], lerped]))
