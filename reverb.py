import pathlib

from amplify import normalize
from audio import Audio
from presets import muffle_distortion


def run():
    audio = Audio.read(pathlib.Path('/home/kpberry/Downloads/castaway.wav'))
    audio = muffle_distortion(audio)
    audio = normalize(audio, 30000)
    audio.write(pathlib.Path('out.wav'))


if __name__ == '__main__':
    run()
