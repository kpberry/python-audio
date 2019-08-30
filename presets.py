from distortion import clip_distortion, tanh_distortion
from echo import echo, pre_echo

from smoothing import muffle


def echo_distort(samples):
    samples = echo(samples, 0.3, decay=0.4)
    samples = clip_distortion(samples, 30000)
    return samples


def extra_echo(samples):
    return echo(echo(pre_echo(samples, 0.3), 0.4), 0.2)


def extra_extra_echo(samples):
    return pre_echo(echo(echo(pre_echo(samples, 0.3), 0.4), 0.2), 0.1)


def muffle_distortion(samples):
    samples = tanh_distortion(samples, rescaling=0.1)
    for i in range(8):
        samples = muffle(samples)
    return samples
