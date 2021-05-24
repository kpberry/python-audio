import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import convolve


def seek(clip, query):
    clip = clip.copy()
    clip[clip > 0] = 1
    clip[clip < 0] = -1

    query = query.copy()
    query[query > 0] = 1
    query[query < 0] = -1

    return np.argmax(convolve(clip, query[::-1], mode='valid'))


def seek2(clip, query):
    return np.argmax(ifft(convolve(fft(clip), fft(query[::-1]), mode='valid')))


def seek3(clip, query):
    query = query / np.std(query)
    return np.argmax(
        [np.dot(query, clip[i:i + len(query)]) / np.std(clip[i:i + len(query)]) for i in range(len(clip) - len(query))])
