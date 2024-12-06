from pedalboard.io import AudioFile
from synthesis import synthesizer
from temporal import Time
from processing import normalize

frequencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]
duration = Time(seconds = 0.35)
delay = Time.from_millisecond(40)
damping = 0.499

synthesizer = synthesizer()
#sounds = [synthesizer.vibrate(frequency, duration, damping) for frequency in frequencies]
sounds = [synthesizer._vibrate(frequency, Time(3.5 + 0.25 * i), damping) for i, frequency in enumerate(frequencies)]

with AudioFile("arpeggio.mp3", "w", synthesizer.sampling_rate) as file:
    file.write(normalize(synthesizer._overlay(sounds, delay)))
    '''
    for frequency in frequencies:
        file.write(synthsizer.vibrate(frequency, duration, damping))
    '''