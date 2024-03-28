import wave
import sounddevice
from pydub import AudioSegment
import pyaudio
from amplitude import Amplitude
import os
from vu_display.vu_display import setup_vu_meter
from vu_display.vu_display import disp_amp
SHORT_NORMALIZE = 1.0 / 32768.0

def play_and_vu(mp3_file):
    audio = pyaudio.PyAudio()
    setup_vu_meter()

    try:
        chunk = 256

        sound = AudioSegment.from_mp3(mp3_file)
        wav_form = sound.export(format="wav")
        wf = wave.open(wav_form, 'rb')

        stream = audio.open(format =
            audio.get_format_from_width(sound.sample_width),
            channels = sound.channels,
            rate = sound.frame_rate,
            output = True
        )

        data = wf.readframes(chunk)
        max_amp = Amplitude()
        while data:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(chunk)
            amp = Amplitude.from_data(data)
            if amp > max_amp:
                max_amp = amp
#            amp.display(scale=500, mark=max_amp)
#            print(int(10.0 / max_amp.to_int(1000) * amp.to_int(1000)))
            if max_amp.to_int(1000) > 0:
                disp_amp(int(10.0 / max_amp.to_int(1000) * amp.to_int(1000)))

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


while True:
    play_and_vu("testsound.mp3")