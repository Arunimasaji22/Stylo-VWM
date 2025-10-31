from gtts import gTTS
import os
from playsound import playsound

text = "Hello, this is a sample text to speech conversion using Google Text-to-Speech in Python."


language = 'en'
tts = gTTS(text=text, lang=language, slow=False)
tts.save("output.mp3")
playsound("output.mp3")
os.remove("output.mp3")
