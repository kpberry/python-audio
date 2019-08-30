import pathlib

from amplify import normalize
from audio import Audio
from presets import extra_echo
from smoothing import muffle
from timing import change_speed


def run():
    audio = Audio.read(pathlib.Path('/home/kpberry/Downloads/castaway.wav'))
    audio.samples = extra_echo(audio.samples)
    audio.samples = muffle(audio.samples)
    audio.samples = change_speed(audio.samples, 0.5)
    audio.samples = normalize(audio.samples, 30000)
    audio.write(pathlib.Path('out.wav'))


if __name__ == '__main__':
    run()
    # data = np.sin(np.linspace(0, 6, 100))
    # plt.plot(data)
    # data = change_speed(data, 0.5)
    # plt.plot(data)
    # plt.show()
