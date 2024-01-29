import pygame
import pygame.sndarray
from pydub import AudioSegment
import numpy as np
import time
from time import sleep

def play_and_vu(file_path):
    pygame.init()

    try:
        vu_interval = 0.02
        norm = 50
        song = AudioSegment.from_mp3(file_path)
        sampling_rate = song.frame_rate

        pygame.mixer.init()

        sound = pygame.mixer.Sound(file_path)

        sound_array = pygame.sndarray.array(sound)
        amplitudes = np.abs(sound_array[:, 0])

        chunk_size = int(sampling_rate * vu_interval)

        num_chunks = len(amplitudes) // chunk_size

        mean_amps = np.zeros(num_chunks, dtype=amplitudes.dtype)

        for i in range(num_chunks):
            start_index = i * chunk_size
            end_index = (i + 1) * chunk_size
            chunk_mean = np.mean(amplitudes[start_index:end_index])
            mean_amps[i] = chunk_mean

        max_amp = np.max(mean_amps[:])
        norm_amps = (mean_amps / max_amp * norm).astype(np.int32)

        pygame.mixer.Sound(sound).play()
        play_start = time.time()

        while pygame.mixer.get_busy():
            value = int((time.time() - play_start) / vu_interval)
            if value > len(norm_amps) - 1:
                value = len(norm_amps) - 1
            print(f"|{'=' * norm_amps[value]}", end='\n')
            sleep(vu_interval)

    finally:
        pygame.quit()

play_and_vu('testsound.mp3')
