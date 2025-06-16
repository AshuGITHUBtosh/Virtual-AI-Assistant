import openai
from gtts import gTTS
import pygame
import subprocess
import time
import os
from multiprocessing import Process

# === CONFIG ===
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "lm-studio"  # dummy key
MODEL_NAME = "codellama-7b-instruct"
AUDIO_FILE = "response.mp3"
VIDEO_FILE = "/home/ashutosh/Desktop/VIGF/intro_casual.mp4"

# === SPEECH UTILITY ===
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save(AUDIO_FILE)

    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()

# === LOOPING VIDEO PLAYER ===
def loop_video(video_path):
    while True:
        proc = subprocess.Popen(
            ["ffplay", "-autoexit", "-loglevel", "quiet", video_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        proc.wait()  # Wait for this run to finish, then loop

# === MAIN LOOP ===
def chat_with_model():
    print("Welcome to your AI Girlfriend 💖! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        try:
            # Step 1: Get response from LLM
            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": user_input}],
                temperature=0.7
            )
            answer = response['choices'][0]['message']['content'].strip()
            print("AI:", answer)

            # Step 2: Convert text to speech
            speak_text(answer)

            # Step 3: Start looping video in background
            video_process = Process(target=loop_video, args=(VIDEO_FILE,))
            video_process.start()

            # Step 4: Wait for audio to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)

            # Step 5: Stop video process when audio ends
            video_process.terminate()
            video_process.join()

        except Exception as e:
            print("Error:", e)

    # Clean up
    pygame.mixer.quit()
    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)

if __name__ == "__main__":
    chat_with_model()
