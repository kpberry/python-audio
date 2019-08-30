import pathlib

from amplify import normalize
from audio import Audio
from presets import extra_echo


def run():
    audio = Audio.read(pathlib.Path('/home/kpberry/Downloads/castaway.wav'))
    audio.samples = extra_echo(audio.samples)
    audio.samples = normalize(audio.samples, 30000)
    audio.write(pathlib.Path('out.wav'))


if __name__ == '__main__':
    run()
