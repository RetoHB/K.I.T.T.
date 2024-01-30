# Interactive AI based K.I.T.T. with Voicebox

Attribution and Acknowledgment: many thanks to DevMiser for his awesome DaVinci project! He laid the foundation for this K.I.T.T project and made it possible in the first place! https://github.com/DevMiser/DaVinci

This interactive AI based K.I.T.T is a python program that utilizes Picovoice Porcupine (and PyAudio) to detect a wake word; Picovoice Cobra voice activity detection to determine when the user begins and finishes speaking their query; Picovoice Leopard to convert the spoken query to text; OpenAI ChatGPT as the artificial intelligence that responds to the query; Amazon Polly text to speech to convert the response into a natural-sounding human voice; and Pygame to play the audio. At the same time the voice output is displayed on the voicebox VU meter. The voicebox is attached to the Pi 4 via I2C bus.

Parts required:
- Raspberry Pi 4 – This needs to be a Raspberry Pi 4, so that you can run the 64-bit operating system. Earlier versions of Raspberry Pis are likely to throw memory errors while running this program. Raspberry Pi’s newest OS (Bookworm) released on December 5, 2023, does not work well with this installation. For best results, use a Raspberry Pi 4 (not a Raspberry Pi 5) and use the legacy 64-bit OS. The 2 GB RAM model is sufficient: https://www.adafruit.com/product/4292
- Power Supply – 5V power supply. I recommend the official Raspberry Pi power supply: https://www.adafruit.com/product/4298
- USB Microphone – for talking to K.I.T.T. Any USB mic should work, and this inexpensive one is sufficient: https://www.adafruit.com/product/3367
- USB speaker – for K.I.T.T. to talk back to you. I used this one: https://www.adafruit.com/product/3369
- my voicebox PCB. I may have some unpoplutaed boards left... contact me
- some nice housing, to be designed...
