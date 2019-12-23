import pathlib

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read as wav_read, write as wav_write


class Audio:
    def __init__(self, data, rate=44100):
        self.samples = data.astype(np.float)
        self.rate = rate

    @classmethod
    def read(cls, path: pathlib.Path) -> 'Audio':
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

    def write(self, path: pathlib.Path):
        extension = path.suffix
        if extension == '.wav':
            wav_write(str(path), self.rate, self.samples.astype(np.short))
        else:
            raise ValueError(f'Unsupported file type: {extension}')

    def plot(self):
        plt.plot(self.samples)
        plt.show()
