from random import random

import numpy as np

from amplify import normalize


def clip_distortion(audio, cutoff=5000):
    return audio.set_samples(np.clip(audio.samples, -abs(cutoff), abs(cutoff)))


def tanh_distortion(audio, rescaling=1):
    peak = np.max(np.abs(audio.samples))
    return audio.set_samples(np.tanh(audio.samples / rescaling) * peak * rescaling)


def square_distortion(audio):
    peak = np.max(np.abs(audio.samples))
    result = audio.set_samples(((normalize(audio, 1).samples > 0) - 0.5) * peak * 2)
    return result


def polynomial_distortion(audio, exponent=0.5):
    signs = np.sign(audio.samples)
    abs_samples = np.abs(audio.samples)
    peak = np.max(abs_samples)
    samples = normalize(audio.set_samples(abs_samples), 1).samples ** exponent * signs * peak
    return audio.set_samples(samples)


def soft_clip_polynomial_distortion(audio, proportion=0.33, exponent=3):
    samples = audio.samples - polynomial_distortion(audio, exponent).samples * proportion
    return audio.set_samples(samples)


def strange_differential_distortion(audio, spacing=1, activation=lambda x: x * 20):
    samples = audio.samples.copy()
    signs = np.sign(samples[spacing:])
    activation = np.vectorize(activation)
    differential = np.abs(samples[spacing:] - samples[:-spacing])
    samples[spacing:] = (np.abs(samples[spacing:]) - activation(differential)) * signs
    return audio.set_samples(samples)


def differential_distortion(audio, spacing=1, activation=lambda x: x * 20):
    # Tends to actually make signals much clearer
    samples = audio.samples.copy()
    activation = np.vectorize(activation)
    differential = samples[spacing:] - samples[:-spacing]
    samples[spacing:] = samples[spacing:] - activation(differential)
    return audio.set_samples(samples)


def fuzz(audio, scale=1):
    return differential_distortion(audio, spacing=1, activation=lambda x: random() * x * scale)
