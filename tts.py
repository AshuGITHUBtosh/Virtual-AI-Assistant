from gtts import gTTS
import os
from playsound import playsound

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = "output.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

if __name__ == "__main__":
    while True:
        user_input = input("💬 Type something (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        text_to_speech(user_input)
