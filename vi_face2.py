import asyncio
import websockets
import json
import os

TOKEN_FILE = "auth_token.json"

async def open_mouth():
    uri = "ws://localhost:8001"

    # Check if token file exists
    if not os.path.exists(TOKEN_FILE):
        print(f"Token file '{TOKEN_FILE}' not found. Please run the token request script first.")
        return

    # Load token
    with open(TOKEN_FILE, "r") as f:
        token_data = json.load(f)
        token = token_data.get("token")

    async with websockets.connect(uri) as ws:
        # Authenticate with token
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
        print("Authentication response:", auth_response)

        # Send command to open mouth
        mouth_open_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "openMouth",
            "messageType": "InjectParameterDataRequest",
            "data": {
                "faceFound": True,
                "mode": "set",
                "parameterValues": [
                    {
                        "id": "MouthOpen",
                        "value": 1.0  # Fully open
                    }
                ]
            }
        }
        await ws.send(json.dumps(mouth_open_request))
        mouth_response = await ws.recv()
        print("Mouth open command response:", mouth_response)

asyncio.run(open_mouth())
