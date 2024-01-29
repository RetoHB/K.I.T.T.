#!/usr/bin/env python3

import pygame
import time
from time import sleep

output_file = "KITTScannerSound.mp3"
amplitude = 32767
#pygame.init()
pygame.mixer.init()

#pygame.mixer.music.load(output_file)
#pygame.mixer.music.play()

sound = pygame.mixer.Sound(output_file)
a1 = pygame.sndarray.array(sound)

sound.play()

#pygame.mixer.music.play()

#pygame.mixer.music.load(output_file)
#pygame.mixer.music.set_volume(1.0) # uncomment to control the the playback volume (from 0.0 to 1.0)
#pygame.mixer.music.play()

while pygame.mixer.get_busy():
    #current_volume = pygame.mixer.Sound.get_volume(0)
    print(str(a1[5][1]))
    #pass
    pygame.time.wait(200)

sleep(0.2)
