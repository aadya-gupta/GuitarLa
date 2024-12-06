from dataclasses import dataclass
from typing import Iterator, Sequence
from itertools import cycle
from functools import cache

from burst import BurstGenerator, WhiteNoise
from temporal import Hertz, Time
from processing import normalize, remove_dc
from instrument import PluckedStringInstrument
from chord import Chord
from stroke import Direction, Velocity

import numpy as np

AUDIO_CD_SAMPLING_RATE = 44100

@dataclass(frozen = True)
class synthesizer:
    instrument : PluckedStringInstrument
    burst_generator: BurstGenerator = WhiteNoise()
    sampling_rate = AUDIO_CD_SAMPLING_RATE

    @cache
    def strum_strings(self, chord : Chord, velocity : Velocity, vibration : Time | None = None) -> np.ndarray:
        if vibration is None:
            vibration = self.instrument.vibration

        if velocity.direction is Direction.Up:
            stroke = self.instrument.upstroke
        else:
            stroke = self.instrument.downstroke

        sounds = tuple(self._vibrate(pitch.frequency, vibration, self.instrument.damping)
                       for pitch in stroke(chord))
        
        return self._overlay(sounds, velocity.delay)

    @cache
    def _vibrate(self, frequency: Hertz, duration: Time, damping: float = 0.5) -> np.ndarray:
        assert 0 < damping <= 0.5

        def feedback_loop() -> Iterator[float]:
            buffer = self.burst_generator(num_samples= round(self.sampling_rate/frequency), sampling_rate= self.sampling_rate)

            for i in cycle(range(buffer.size)):
                yield (current_sample := buffer[i])
                next_sample = buffer[(i+1) % buffer.size]
                buffer[i] = (current_sample + next_sample) * damping

        return normalize(remove_dc(np.fromiter(feedback_loop(), np.float64, duration.get_num_samples(self.sampling_rate),)))

    '''       
    def overlay(self, sounds: Sequence[np.ndarray]) -> np.ndarray:
        return np.sum(sounds, axis = 0)    
    '''
    def _overlay(self, sounds: Sequence[np.ndarray], delay: Time) -> np.ndarray:
        num_delay_samples = delay.get_num_samples(self.sampling_rate)
        num_samples = max(i * num_delay_samples + sound.size for i, sound in enumerate(sounds))

        samples = np.zeros(num_samples, dtype = np.float64)
        for i, sound in enumerate(sounds):
            offset = i * num_delay_samples
            samples[offset : offset + sound.size] += sound
        return samples
    
