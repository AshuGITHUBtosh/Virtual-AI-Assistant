import asyncio
import websockets
import json
import os
import time
import threading

TOKEN_FILE = "auth_token.json"
WS_URI = "ws://localhost:8001"

async def send_command(ws, request_id, mouth_value):
    command = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": request_id,
        "messageType": "InjectParameterDataRequest",
        "data": {
            "faceFound": True,
            "mode": "set",
            "parameterValues": [
                {
                    "id": "MouthOpen",
                    "value": mouth_value
                }
            ]
        }
    }
    await ws.send(json.dumps(command))
    response = await ws.recv()
    print(f"Command {request_id} response: {response}")

async def mouth_movement(ws, duration):
    """Simulate mouth opening and closing repeatedly during duration in seconds."""
    start_time = time.time()
    open_close = 1.0
    while time.time() - start_time < duration:
        await send_command(ws, "mouthMove", open_close)
        open_close = 0.0 if open_close == 1.0 else 1.0
        await asyncio.sleep(0.3)  # adjust speed here
    # Ensure mouth is closed at the end
    await send_command(ws, "mouthClose", 0.0)

def play_tts_sync(text):
    # Placeholder: replace with your TTS play code here, which blocks until finished
    # For example, playsound, pydub.play, or synchronous edge-tts wrapper
    import playsound
    # Assuming you generate an mp3 file from text then play it here synchronously:
    mp3_path = "temp_speech.mp3"
    # You should generate mp3 with your TTS beforehand; this is just an example
    playsound.playsound(mp3_path)

async def tts_with_mouth(text):
    # Load token
    if not os.path.exists(TOKEN_FILE):
        print(f"Token file '{TOKEN_FILE}' not found. Please run the token request script first.")
        return

    with open(TOKEN_FILE, "r") as f:
        token_data = json.load(f)
        token = token_data.get("token")

    async with websockets.connect(WS_URI) as ws:
        # Authenticate
        auth_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "authRequest",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": "MouthOpenerScript",
                "pluginDeveloper": "YourNameHere",
                "authenticationToken": token
            }
        }
        await ws.send(json.dumps(auth_request))
        auth_response = await ws.recv()
        auth_data = json.loads(auth_response)
        if not auth_data.get("data", {}).get("authenticated", False):
            print("Authentication failed:", auth_data.get("data", {}).get("reason", "Unknown reason"))
            return
        print("Authenticated successfully")

        # Start mouth movement in background task
        # Assume speech duration ~ 5 seconds here (you should set it based on TTS audio length)
        duration = 5

        # Run mouth movement task
        mouth_task = asyncio.create_task(mouth_movement(ws, duration))

        # Run TTS synchronously in thread to not block asyncio loop
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, play_tts_sync, text)

        # Wait for mouth movement to complete
        await mouth_task

async def main():
    text_to_speak = "Hello master, how can I help you today?"
    await tts_with_mouth(text_to_speak)

if __name__ == "__main__":
    asyncio.run(main())
