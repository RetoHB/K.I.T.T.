# Interactive AI based K.I.T.T. with Voicebox

*Attribution and Acknowledgment:* many thanks to DevMiser for his awesome [DaVinci project](https://github.com/DevMiser/DaVinci)! He laid the foundation for this K.I.T.T project and made it possible in the first place!

This interactive AI based K.I.T.T is a python program that utilizes Picovoice Porcupine (and PyAudio) to detect a wake word; Picovoice Cobra voice activity detection to determine when the user begins and finishes speaking their query; Picovoice Leopard to convert the spoken query to text; OpenAI ChatGPT as the artificial intelligence that responds to the query; Amazon Polly text to speech to convert the response into a natural-sounding human voice; and PyAudio to play the audio. At the same time the voice output is displayed on the voicebox VU meter. The voicebox is attached to the Pi 4 via I2C bus.

Parts required:
- Raspberry Pi 4 – This needs to be a Raspberry Pi 4, so that you can run the 64-bit operating system. Earlier versions of Raspberry Pis are likely to throw memory errors while running this program. Raspberry Pi’s newest OS (Bookworm) released on December 5, 2023, does not work well with this installation. ***For best results, use a Raspberry Pi 4 (not a Raspberry Pi 5) and use the legacy 64-bit OS.*** The 2 GB RAM model is sufficient: https://www.adafruit.com/product/4292
- microSD card, minimum 16GB seems to be a good choice: https://www.adafruit.com/product/2693
- Power Supply – 5V power supply. I recommend the official Raspberry Pi power supply: https://www.adafruit.com/product/4298
- USB Microphone – for talking to K.I.T.T. Any USB mic should work, and this inexpensive one is sufficient: https://www.adafruit.com/product/3367
- USB speaker – for K.I.T.T. to talk back to you. I used this one: https://www.adafruit.com/product/3369
- my [voicebox PCB](voicebox_pcb). I may have some unpoplutaed boards left... contact me
- some nice housing, to be designed...

## Creating required API keys
### Create an OpenAI Account and create a secret key
Create an account on https://openai.com  
Sign in and click on your personal icon in the upper right-corner and then click on "View API keys". Click on "Create new secret key" and copy the key for later use.  
I think you need to make sure to have a positive credit balance in your account. I do not remember if you get a free amount to start with when opening an account.

### Create Picovoice Account and create access key
Create a free account on https://picovoice.ai
Sign in and copy your AccessKey for later use

### Create AWS IAM account and obtain AWS access key and secret access key
This is the trickiest step...  
Create a free AWS account on https://aws.amazon.com/free/  
Go to the IAM dashboard under https://console.aws.amazon.com/iamv2  
Select "User groups" from the menu on the left side, then click "Create group" in the upper right corner.  
As group name enter "Polly".  
Under "Attach permission policies - Optional" search for "Polly" and select "AmazonPollyFullAccess".  
Then select "Users" from the menu on the left side and click "Add users" in the upper right corner.  
Type "Polly_User" and click next.  
Under Permission options select "Add user to group" and check the box next to "Polly" under "User groups". Click next.  
Click "Create User" and then "View User".  
In the tab "Security credentials" click "Create access key". Select "Command Line Interface (CLI), tick the box at the bottom and click "Create access key".  
On the next page copy both "Access key" and "Secret access key" for later use.
