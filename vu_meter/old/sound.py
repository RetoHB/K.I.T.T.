# the following program is provided by DevMiser - https://github.com/DevMiser

#!/usr/bin/env python3

import boto3
import openai
import os
import pvcobra
import pvleopard
import pvporcupine
import pyaudio
import random
import struct
import sys
import textwrap
import threading
import time

import RPi.GPIO as GPIO

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from colorama import Fore, Style
from openai import OpenAI
from pvleopard import *
from pvrecorder import PvRecorder
from threading import Thread, Event
from time import sleep

output_file = "KITTScannerSound.mp3"
pygame.mixer.init()
pygame.mixer.music.load(output_file)
pygame.mixer.music.set_volume(1.0) # uncomment to control the the playback volume (from 0.0 to 1.0)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pass
sleep(0.2)
