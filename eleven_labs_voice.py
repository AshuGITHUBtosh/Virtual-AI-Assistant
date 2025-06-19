import requests
import tempfile
import subprocess
from murf import Murf

# Step 1: Authenticate with your Murf API key
client = Murf(api_key="ap2_6499a600-d564-463f-b107-8c3ab1b1c56d")

# Step 2: Generate speech from text using a voice
response = client.text_to_speech.generate(
    text="Hello master, I am your virtual anime assistant. How can I help you today?",
    voice_id="Heidi"
)

# Step 3: Download the audio file from the URL
audio_url = response.audio_file

# Step 4: Save audio to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
    audio_data = requests.get(audio_url).content
    temp_audio.write(audio_data)
    temp_audio_path = temp_audio.name

# Step 5: Use subprocess to play the audio with default media player (Windows)
subprocess.run(f'start /wait wmplayer "{temp_audio_path}"', shell=True)
