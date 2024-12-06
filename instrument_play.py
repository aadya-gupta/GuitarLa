from pedalboard.io import AudioFile
from chord import Chord
from instrument import PluckedStringInstrument, StringTuning
from stroke import Direction, Velocity
from synthesis import synthesizer
from temporal import Time

instruments = {
    'acoustic guitar' : PluckedStringInstrument(
        tuning = StringTuning.from_notes('E2', 'A2', 'D3', 'G3', 'B3', 'E4'),
        vibration = Time(seconds = 15),
        damping = 0.49,
    ),
    'Ukele' : PluckedStringInstrument(
        tuning = StringTuning.from_notes('A4', 'E4', 'C4', 'G4'),
        vibration = Time(seconds=5.0),
        damping = 0.49,
    ),
}

for name, instrument in instruments.items():
    synth = synthesizer(instrument)
    amplitudes = synth.strum_strings(
        Chord([0] * instrument.num_strings),
        Velocity(Direction.Down, Time.from_millisecond(1))
    )
    with AudioFile(f"{name}.mp3", "w", synth.sampling_rate) as file:
        file.write(amplitudes)
        