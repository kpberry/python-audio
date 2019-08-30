def delay(samples, offset=1, rate=44100):
    samples = samples.copy()
    offset = int(offset * rate)
    samples[offset:] += samples[:-offset]
    return samples
