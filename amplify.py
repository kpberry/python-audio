import numpy as np


def amplify(samples, scale=1):
    return samples * scale


def normalize(samples, new_peak=1):
    return samples * new_peak / np.max(np.abs(samples))
