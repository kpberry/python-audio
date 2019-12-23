import numpy as np

from audio import Audio
from smoothing import lerp


def tone(frequency, duration, amplitude=255, rate=44100) -> Audio:
    times = np.linspace(0, duration, rate * duration)
    return Audio(np.sin(2 * np.pi * frequency * times) * amplitude, rate)


def sinusoid(frequencies, amplitude=255, rate=44100) -> Audio:
    times = np.linspace(0, len(frequencies) / rate, len(frequencies))
    return Audio(np.sin(2 * np.pi * frequencies * times) * amplitude, rate)


def linear_pitch_sweep(start, end, duration, amplitude=255, rate=44100) -> Audio:
    times = np.linspace(0, 1, duration * rate)
    # Linear interpolation of frequencies (instantaneous frequency = df/dt):
    # S(t) = ∫df/dt = ∫f1 + (f2 - f1)t dt = t(f1 + (f2 - f1)t/2) + C
    frequencies = lerp(np.ones_like(times) * start, np.ones_like(times) * end, times / 2)
    return sinusoid(frequencies, amplitude, rate)
