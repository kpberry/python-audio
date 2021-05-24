import numpy as np

from amplify import normalize
from distortion import clip_distortion, tanh_distortion
from echo import echo, pre_echo
from raytracing import make_box, Point, Sphere, profile_room
from reverb import kernel_reverb

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


def cathedral_reverb(samples):
    room = make_box(100, 100, 100, Point(0, 0, 0), True)
    speaker = Point(50, 95, 5)
    microphone = Sphere(Point(50, 95, 95), 5)
    _kernel = np.array(profile_room(room, speaker, microphone, samples=100000, bounces=100, decay=0.05, max_delay=10))
    return normalize(kernel_reverb(samples, _kernel))
