from random import random

import numpy as np

from amplify import normalize
from audio import Audio


def clip_distortion(samples, cutoff=5000):
    return np.clip(samples, -abs(cutoff), abs(cutoff))


def tanh_distortion(samples, rescaling=1):
    peak = np.max(np.abs(samples))
    return np.tanh(samples / rescaling) * peak * rescaling


def square_distortion(samples):
    peak = np.max(np.abs(samples))
    return ((normalize(samples, 1) > 0) - 0.5) * peak * 2


def polynomial_distortion(samples, exponent=0.5):
    signs = np.sign(samples)
    abs_samples = np.abs(samples)
    peak = np.max(abs_samples)
    samples = normalize(abs_samples, 1) ** exponent * signs * peak
    return samples


def soft_clip_polynomial_distortion(samples, proportion=0.33, exponent=3):
    return samples - polynomial_distortion(samples, exponent) * proportion


def strange_differential_distortion(samples, spacing=1, activation=lambda x: x * 20):
    samples = samples.copy()
    signs = np.sign(samples[spacing:])
    activation = np.vectorize(activation)
    differential = np.abs(samples[spacing:] - samples[:-spacing])
    samples[spacing:] = (np.abs(samples[spacing:]) - activation(differential)) * signs
    return samples


def differential_distortion(samples, spacing=1, activation=lambda x: x * 20):
    # Tends to actually make signals much clearer
    samples = samples.copy()
    activation = np.vectorize(activation)
    differential = samples[spacing:] - samples[:-spacing]
    samples[spacing:] = samples[spacing:] - activation(differential)
    return samples


def fuzz(samples, scale=1):
    return differential_distortion(samples, spacing=1, activation=lambda x: random() * x * scale)

