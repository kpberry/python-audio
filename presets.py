from distortion import clip_distortion, tanh_distortion
from echo import echo, pre_echo

from smoothing import muffle


def echo_distort(audio):
    audio = echo(audio, 0.3, decay=0.4)
    audio = clip_distortion(audio, 30000)
    return audio


def extra_echo(audio):
    return echo(echo(pre_echo(audio, 0.3), 0.4), 0.2)


def extra_extra_echo(audio):
    return pre_echo(echo(echo(pre_echo(audio, 0.3), 0.4), 0.2), 0.1)


def muffle_distortion(audio):
    audio = tanh_distortion(audio, rescaling=0.1)
    for i in range(8):
        audio = muffle(audio)
    return audio
