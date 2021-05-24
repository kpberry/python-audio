import pathlib
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read as wav_read, write as wav_write


class Audio:
    def __init__(self, data, rate=44100):
        self.samples = data.astype(np.float)
        self.rate = rate

    @classmethod
    def read(cls, path: Union[pathlib.Path, str]) -> 'Audio':
        path = pathlib.Path(path)
        extension = path.suffix
        if extension == '.wav':
            rate, samples = wav_read(str(path))
            # TODO handle stereo reading properly
            try:
                samples = np.mean(samples, axis=1)
            except IndexError:
                pass
            return cls(samples, rate)
        else:
            raise ValueError(f'Unsupported file type: {extension}')

    def write(self, path: Union[pathlib.Path, str]):
        path = pathlib.Path(path)
        extension = path.suffix
        if extension == '.wav':
            wav_write(str(path), self.rate, self.samples)
        else:
            raise ValueError(f'Unsupported file type: {extension}')

    def plot(self):
        plt.plot(self.samples)
        plt.show()

    def __add__(self, other):
        if not isinstance(other, Audio):
            raise TypeError('Audio can only be added to other Audio objects.')

        if self.rate != other.rate:
            raise ValueError(f'Audio samples must have the same rates to be added. '
                             f'Found mismatched rates: {self.rate} and {other.rate}.')

        return Audio(self.samples + other.samples, rate=self.rate)