def delay(audio, offset=1):
    samples = audio.samples.copy()
    offset = int(offset * audio.rate)
    samples[offset:] += samples[:-offset]
    return audio.set_samples(samples)
