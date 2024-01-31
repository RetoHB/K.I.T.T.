# the following program is provided by RetoHB - https://github.com/RetoHB

#!/usr/bin/env python3

import boto3
import openai
import os
import pvcobra
import pvleopard
import pvporcupine
import pyaudio
import struct
import sys
import textwrap
import threading
import time

import keys

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from colorama import Fore, Style
from openai import OpenAI
from pvleopard import *
from pvrecorder import PvRecorder
from threading import Thread, Event
from time import sleep

from vu_meter.vu_meter import play_and_vu
from vu_meter.vu_display.vu_display import disp_amp
from vu_meter.vu_display.vu_display import setup_vu_meter

audio_stream = None
cobra = None
pa = None
polly = boto3.client('polly')
porcupine = None
recorder = None
wav_file = None
sleeping = 0

GPT_model = "gpt-4" # most capable GPT model and optimized for chat.  You can substitute with gpt-3.5-turbo for lower cost and latency. gpt-4
openai.api_key = keys.openai
pv_access_key = keys.pv

client = OpenAI(api_key=openai.api_key)

prompt = ["How may I assist you?",
    "How may I help?",
    "What can I do for you?",
    "Yes?",
    "I'm here.",
    "I'm listening."]

chat_log=[
    {"role": "system", "content": "Your name is kitt. If you are asked about yourself, you answer with the following exact phrase: 'I am the voice of the Knight Industries Two Thousand microprocessor. K.I.T.T for easy reference, KITT if you prefer.' Do not repeat this too often."},
    ]

def ChatGPT(query):
    user_query = [
        {"role": "user", "content": query},
        ]
    send_query = (chat_log + user_query)
    response = client.chat.completions.create(
    model=GPT_model,
    messages=send_query
    )
    answer = response.choices[0].message.content
    chat_log.append({"role": "assistant", "content": answer})
    return answer

def responseprinter(chat):
    wrapper = textwrap.TextWrapper(width=70)  # Adjust the width to your preference
    paragraphs = res.split('\n')
    wrapped_chat = "\n".join([wrapper.fill(p) for p in paragraphs])
    for word in wrapped_chat:
       time.sleep(0.06)
       print(word, end="", flush=True)
    print("\n")

#K.I.T.T. will 'remember' earlier queries so that it has greater continuity in its response
#the following will delete that 'memory' five minutes after the start of the conversation
def append_clear_countdown():
    sleep(300)
    global chat_log
    chat_log.clear()
    chat_log=[
        {"role": "system", "content": "Your name is kitt. If you are asked about yourself, you answer with the following exact phrase: 'I am the voice of the Knight Industries Two Thousand microprocessor. K.I.T.T for easy reference, KITT if you prefer' Do not repeat this too often."},
        ]
    global count
    count = 0
    t_count.join

def voice(chat):

    voiceResponse = polly.synthesize_speech(Text=chat, OutputFormat="mp3",
                    VoiceId="Matthew") #other options include Amy, Joey, Nicole, Raveena, Russell and Matthew
    if "AudioStream" in voiceResponse:
        with voiceResponse["AudioStream"] as stream:
            output_file = "speech.mp3"
            try:
                with open(output_file, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)

    else:
        print("did not work")

    play_and_vu("speech.mp3")
    sleep(0.2)

def wake_word():

    porcupine = pvporcupine.create(keyword_paths=["Hey-Kitt_en_raspberry-pi_v3_0_0.ppn"],
                            access_key=pv_access_key,
                            sensitivities=[0.1], #from 0 to 1.0 - a higher number reduces the miss rate at the cost of increased false alarms
                                   )
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)

    wake_pa = pyaudio.PyAudio()

    porcupine_audio_stream = wake_pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

    Detect = True

    pygame.mixer.init()
    pygame.mixer.music.load("KITTScannerSound.mp3")
    pygame.mixer.music.play()

    disp_amp(10)
    sleep(0.2)
    disp_amp(0)

    while Detect:
        porcupine_pcm = porcupine_audio_stream.read(porcupine.frame_length)
        porcupine_pcm = struct.unpack_from("h" * porcupine.frame_length, porcupine_pcm)

        porcupine_keyword_index = porcupine.process(porcupine_pcm)

        if porcupine_keyword_index >= 0:
            keyword = "K.I.T.T."
            print(Fore.GREEN + "\n" + keyword + " detected\n")
            porcupine_audio_stream.stop_stream
            porcupine_audio_stream.close()
            porcupine.delete()
            os.dup2(old_stderr, 2)
            os.close(old_stderr)
            Detect = False
            global sleeping
            sleeping = 0

def listen():

    listen_start = time.time()

    cobra = pvcobra.create(access_key=pv_access_key)

    listen_pa = pyaudio.PyAudio()

    listen_audio_stream = listen_pa.open(
                rate=cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=cobra.frame_length)

    print("Listening...\n")

    while True:
        listen_pcm = listen_audio_stream.read(cobra.frame_length)
        listen_pcm = struct.unpack_from("h" * cobra.frame_length, listen_pcm)

        if cobra.process(listen_pcm) > 0.3:
            print("Voice detected\n")
            listen_audio_stream.stop_stream
            listen_audio_stream.close()
            cobra.delete()
            break

        listening_time = time.time() - listen_start

        if listening_time > 15:
            print("No voice input\n")
            global sleeping
            sleeping = 1
            listen_audio_stream.stop_stream
            listen_audio_stream.close()
            cobra.delete()
            break

def detect_silence():

    voice_start = time.time()

    cobra = pvcobra.create(access_key=pv_access_key)

    silence_pa = pyaudio.PyAudio()

    cobra_audio_stream = silence_pa.open(
                    rate=cobra.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=cobra.frame_length)

    last_voice_time = time.time()

    while True:
        cobra_pcm = cobra_audio_stream.read(cobra.frame_length)
        cobra_pcm = struct.unpack_from("h" * cobra.frame_length, cobra_pcm)

        if cobra.process(cobra_pcm) > 0.2:
            last_voice_time = time.time()
        else:
            silence_duration = time.time() - last_voice_time
            if silence_duration > 1.3:
                print("End of query detected\n")
                cobra_audio_stream.stop_stream
                cobra_audio_stream.close()
                cobra.delete()
                last_voice_time=None
                break
        input_duration = voice_start + 15
        if time.time() > input_duration:
            print("Endless query, aborting\n")
            cobra_audio_stream.stop_stream
            cobra_audio_stream.close()
            cobra.delete()
            last_voice_time=None
            break
        else:
            pass

class Recorder(Thread):
    def __init__(self):
        super().__init__()
        self._pcm = list()
        self._is_recording = False
        self._stop = False

    def is_recording(self):
        return self._is_recording

    def run(self):
        self._is_recording = True

        recorder = PvRecorder(device_index=-1, frame_length=512)
        recorder.start()

        while not self._stop:
            self._pcm.extend(recorder.read())
        recorder.stop()

        self._is_recording = False

    def stop(self):
        self._stop = True
        while self._is_recording:
            pass

        return self._pcm

try:

    o = create(
        access_key=pv_access_key,
        enable_automatic_punctuation = True,
        )

    event = threading.Event()
    setup_vu_meter()

    count = 0

    sleep(2)

    wake_word()

    while True:

        try:

            if count == 0:
                t_count = threading.Thread(target=append_clear_countdown)
                t_count.start()
            else:
                pass
            count += 1

            if sleeping == 1:
                print("Sleeping...\n")
                wake_word()
                sleeping = 0
            else:
                pass

            pygame.mixer.init()
            pygame.mixer.music.load("tick.mp3")
            pygame.mixer.music.play()

            disp_amp(1)
            sleep(0.2)
            disp_amp(0)

# comment out the next line if you do not want K.I.T.T. to respond to his name
#            voice(random.choice(prompt))
            recorder = Recorder()
            recorder.start()
            listen()

            if sleeping == 1:
                recorder.stop()
                o.delete
                recorder = None
                continue

            detect_silence()
            transcript, words = o.process(recorder.stop())
            recorder.stop()
            print(transcript)
#                voice(transcript) # uncomment to have K.I.T.T. repeat what it heard
            (res) = ChatGPT(transcript)
            print("\nChatGPT's response is:\n")
            t1 = threading.Thread(target=voice, args=(res,))
            t2 = threading.Thread(target=responseprinter, args=(res,))
            t2.start()
            sleep(1)
            t1.start()
            t1.join()
            t2.join()
            event.set()
            recorder.stop()
            o.delete
            recorder = None

        except openai.APIError as e:
            print("\nThere was an API error.  Please try again in a few minutes.")
            voice("\nThere was an A P I error.  Please try again in a few minutes.")
            event.set()
            recorder.stop()
            o.delete
            recorder = None
            sleep(1)

        except openai.RateLimitError as e:
            print("\nYou have hit your assigned rate limit.")
            voice("\nYou have hit your assigned rate limit.")
            event.set()
            recorder.stop()
            o.delete
            recorder = None
            break

        except openai.APIConnectionError as e:
            print("\nI am having trouble connecting to the API.  Please check your network connection and then try again.")
            voice("\nI am having trouble connecting to the A P I.  Please check your network connection and try again.")
            event.set()
            recorder.stop()
            o.delete
            recorder = None
            sleep(1)

        except openai.AuthenticationError as e:
            print("\nYour OpenAI API key or token is invalid, expired, or revoked.  Please fix this issue and then restart my program.")
            voice("\nYour Open A I A P I key or token is invalid, expired, or revoked.  Please fix this issue and then restart my program.")
            event.set()
            recorder.stop()
            o.delete
            recorder = None
            break

except KeyboardInterrupt:
    print("\n\nExiting ChatGPT Virtual Assistant\n")
    o.delete
