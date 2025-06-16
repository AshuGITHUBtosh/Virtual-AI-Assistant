import asyncio
import websockets
import json
import os
import tempfile
import edge_tts
import playsound
import time
import threading

TOKEN_FILE = "auth_token.json"
VTUBE_URI = "ws://localhost:8001"

# Function to generate TTS and save to a temp file
async def generate_tts(text, voice="en-GB-LibbyNeural", filename="temp_tts.mp3"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

# Function to animate mouth (open/close while speaking)
async def animate_mouth(ws, speaking_time=3.0):
    start = time.time()
    toggle = True

    while time.time() - start < speaking_time:
        value = 1.0 if toggle else 0.2  # Alternate between open and slightly closed
        toggle = not toggle

        mouth_cmd = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "mouthMove",
            "messageType": "InjectParameterDataRequest",
            "data": {
                "faceFound": True,
                "mode": "set",
                "parameterValues": [
                    {"id": "MouthOpen", "value": value}
                ]
            }
        }
        await ws.send(json.dumps(mouth_cmd))
        await asyncio.sleep(0.12)  # Adjust for speed

# Function to play sound (blocking)
def play_audio(path):
    playsound.playsound(path)

# Main function that does TTS + mouth animation
async def speak_and_move(text):
    # Load token
    if not os.path.exists(TOKEN_FILE):
        print(f"Token file '{TOKEN_FILE}' not found.")
        return

    with open(TOKEN_FILE, "r") as f:
        token = json.load(f).get("token")

    # Generate TTS and save
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        audio_path = temp_audio.name

    await generate_tts(text, filename=audio_path)

    # Estimate duration (approximate: 150 words/min = 2.5 wps)
    duration = max(2.0, len(text.split()) / 2.5)

    # Connect to VTube Studio
    async with websockets.connect(VTUBE_URI) as ws:
        # Authenticate
        auth_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "authRequest",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": "MouthSyncTTS",
                "pluginDeveloper": "YourNameHere",
                "authenticationToken": token
            }
        }
        await ws.send(json.dumps(auth_request))
        auth_response = await ws.recv()
        print("Auth:", auth_response)

        # Play sound in a thread (non-blocking)
        audio_thread = threading.Thread(target=play_audio, args=(audio_path,))
        audio_thread.start()

        # Animate mouth while audio is playing
        await animate_mouth(ws, speaking_time=duration)

        audio_thread.join()
        os.remove(audio_path)

# Example usage
if __name__ == "__main__":
    text = "Hello master, I am happy to see you!"
    asyncio.run(speak_and_move(text))