import numpy as np


def amplify(samples, scale=1):
    return samples * scale


def normalize(samples, new_peak=1):
    return amplify(samples, new_peak / np.max(np.abs(samples)))


def blend(samples_a, samples_b, ratio=0.5):
    return samples_a * ratio + samples_b * (1 - ratio)
