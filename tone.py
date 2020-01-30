from __future__ import division

import math

import pyaudio


#See http://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 16000 #number of frames per second/frameset.


SCALE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
fixed_note, fixed_octave, fixed_freq = SCALE.index('A'), 4, 440
A = 2 ** (1 / 12)


def get_freq(note, octave=4):
    _note_delta = SCALE.index(note) - fixed_note
    half_step_delta = (octave - fixed_octave) * len(SCALE) + _note_delta
    return fixed_freq * (A ** half_step_delta)


class AudioStream(object):
    def __init__(self):
        self._p = pyaudio.PyAudio()
        self.stream = self._p.open(
            format=self._p.get_format_from_width(1),
            channels=1,
            rate=BITRATE,
            output=True,
        )

    def _play_tone(self, freq, length):
        #See http://www.phy.mtu.edu/~suits/notefreqs.html
        # FREQUENCY = 261.63 #Hz, waves per second, 261.63=C4-note.

        NUMBEROFFRAMES = int(BITRATE * length)
        # RESTFRAMES = NUMBEROFFRAMES % BITRATE
        wavedata = ''.join(
            chr(int(math.sin(x/((BITRATE/freq)/math.pi))*127+128))
            for x in range(NUMBEROFFRAMES)
        )
        self.stream.write(wavedata)


    def play_tone(self, note, octave, duration=0.33):
        freq = get_freq(note, octave)
        self._play_tone(freq, duration)

    def __enter__(self):
        return self

    def __exit__(self, _, __, ___):
        self.stream.stop_stream()
        self.stream.close()
        self._p.terminate()


# with AudioStream() as stream:
#     for note in SCALE:
#         if len(note) == 1:
#             stream.play_tone(note, 4)
#     stream.play_tone(SCALE[0], 5)

with AudioStream() as stream:
    for note in [('A', 3), ('E', 3), ('A', 3), ('E', 4, 0.66), ('D', 4, 0.66), ('C#', 4), ('B', 3), ('G#', 3, 0.33 * 3)]:
        octave = 4
        duration = 0.33
        if isinstance(note, tuple):
            if len(note) == 2:
                note, octave = note
            else:
                note, octave, duration = note
        stream.play_tone(note, octave, duration)
