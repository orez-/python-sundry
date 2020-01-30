import math

import numpy
import pygame.sndarray as sound
import pygame.mixer as mixer

mixer.init()

print(mixer.get_init())

SAMPLERATE = 44100


# ar = numpy.array([[0.5, 0.5], [2, 2], [3, 3]], dtype='int8')

def tone(freq=1000, volume=127, length=1):
    num_steps = length*SAMPLERATE
    s = []
    for n in range(num_steps):
        value = int(math.sin(n * freq * (6.28318/SAMPLERATE) * length)*volume)
        print(value)
        s.append( [value,value] )
    x_arr = numpy.array(s, dtype='int8')
    return x_arr

sound.make_sound(tone())
