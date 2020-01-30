#!/usr/bin/env python
"""Play a fixed frequency sound."""
from __future__ import division
import math
import contextlib

from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio


def sine_tone(stream, frequency, duration, volume=1, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

    s = lambda t: volume * math.sin(2 * math.pi * frequency * 2 * t / sample_rate)
    samples = (int(s(t) * 0x7f + 0x80) for t in range(n_samples))
    b = bytes(bytearray(samples))
    print(b[0], b[-1])
    stream.write(b)

    # fill remainder of frameset with silence
    # stream.write(b'\x80' * restframes)



@contextlib.contextmanager
def pyaudio_stream(sample_rate=22050):
    p = PyAudio()
    stream = p.open(
        format=p.get_format_from_width(1), # 8bit
        channels=1, # mono
        rate=sample_rate,
        output=True,
    )

    yield stream

    stream.stop_stream()
    stream.close()
    p.terminate()



with pyaudio_stream() as stream:
    sine_tone(stream, 73, 0.220)
    sine_tone(stream, 110, 0.220)
    sine_tone(stream, 165, 0.220)
    sine_tone(stream, 98, 0.220)
    sine_tone(stream, 110, 0.220)
    sine_tone(stream, 147, 0.440)
