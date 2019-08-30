import numpy as np


def amplify(audio, scale=1):
    return audio.set_samples(audio.samples * scale)


def normalize(audio, peak=1):
    unit_normalized = audio.samples / np.max(np.abs(audio.samples))
    return audio.set_samples((unit_normalized * peak))
