import wave
from pydub import AudioSegment
import pyaudio
from amplitude import Amplitude
from vu_constants import RATE, INPUT_FRAMES_PER_BLOCK
import os

def main():
    audio = pyaudio.PyAudio()
    try:
        chunk = 1024

        os.system("echo gpio | sudo tee /sys/class/leds/ACT/trigger >/dev/null 2>&1")

        sound = AudioSegment.from_mp3("testsound.mp3")
        wav_form = sound.export(format="wav")
        wf = wave.open(wav_form, 'rb')

        stream = audio.open(format =
            audio.get_format_from_width(sound.sample_width),
            channels = sound.channels,
            rate = sound.frame_rate,
            output = True)

        data = wf.readframes(chunk)
        maximal = Amplitude()
        while data:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(chunk)
            amp = Amplitude.from_data(data)
            if amp > maximal:
                maximal = amp
            if type(amp) is int:
                pass
            else:
                amp.display(scale=500, mark=maximal)
#                print(str(amp.to_int(700)))
#                if amp.to_int(700) > 30:
#                    os.system("echo 1 | sudo tee /sys/class/leds/ACT/brightness >/dev/null 2>&1")
#                else:
#                    os.system("echo 0 | sudo tee /sys/class/leds/ACT/brightness >/dev/null 2>&1")

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    main()
