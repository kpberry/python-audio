from math import ceil

import numpy as np

from timing import reverse


def echo(samples, offset=1, decay=0.5, rate=44100):
    offset = int(offset * rate)
    buffer = np.zeros(offset)
    level = 1 - decay

    for i in range(ceil(len(samples) / offset)):
        start, end = i * offset, min((i + 1) * offset, len(samples))
        buffer = samples[start:end] + buffer[:end - start] * level
        samples[start:end] = buffer

    return samples


def pre_echo(audio, *echo_args, **echo_kwargs):
    return reverse(echo(reverse(audio), *echo_args, **echo_kwargs))
