import openai
from gtts import gTTS
import pygame
import subprocess
import time
import os

# === CONFIG ===
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "lm-studio"  # dummy key
MODEL_NAME = "codellama-7b-instruct"
AUDIO_FILE = "response.mp3"
VIDEO_FILE = "anime_response.mp4"  # Replace with your Animon video path

# === SPEECH UTILITY ===
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save(AUDIO_FILE)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()

# === VIDEO PLAYER ===
def play_anime_video(video_path):
    # Run video in parallel so we can sync with audio
    subprocess.Popen(["ffplay", "-autoexit", "-loglevel", "quiet", "/home/ashutosh/Desktop/VIGF/intro_casual.mp4"])

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

            # Step 2: Convert to speech and play
            speak_text(answer)

            # Step 3: Play video
            play_anime_video(VIDEO_FILE)

            # Step 4: Wait for audio to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)

        except Exception as e:
            print("Error:", e)

    # Clean up
    pygame.mixer.quit()
    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)

if __name__ == "__main__":
    chat_with_model()
