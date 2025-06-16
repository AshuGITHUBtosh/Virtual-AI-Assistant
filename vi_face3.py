import asyncio
import websockets
import json
import os

TOKEN_FILE = "auth_token.json"
WS_URI = "ws://localhost:8001"

async def open_mouth():
    # Check if token file exists
    if not os.path.exists(TOKEN_FILE):
        print(f"Token file '{TOKEN_FILE}' not found. Please run the token request script first.")
        return

    # Load token
    with open(TOKEN_FILE, "r") as f:
        token_data = json.load(f)
        token = token_data.get("token")

    async with websockets.connect(WS_URI) as ws:
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
        print("Sending authentication request...")
        await ws.send(json.dumps(auth_request))

        auth_response = await ws.recv()
        print("Authentication response:", auth_response)
        auth_data = json.loads(auth_response)
        if not auth_data.get("data", {}).get("authenticated", False):
            print("Authentication failed:", auth_data.get("data", {}).get("reason", "Unknown reason"))
            return

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
        print("Sending mouth open command...")
        await ws.send(json.dumps(mouth_open_request))
        mouth_response = await ws.recv()
        print("Mouth open command response:", mouth_response)

        # You can add a delay here if you want mouth open for some seconds
        await asyncio.sleep(3)

        # Send command to close mouth
        mouth_close_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "closeMouth",
            "messageType": "InjectParameterDataRequest",
            "data": {
                "faceFound": True,
                "mode": "set",
                "parameterValues": [
                    {
                        "id": "MouthOpen",
                        "value": 0.0  # Fully closed
                    }
                ]
            }
        }
        print("Sending mouth close command...")
        await ws.send(json.dumps(mouth_close_request))
        close_response = await ws.recv()
        print("Mouth close command response:", close_response)

async def main():
    print("Script started")
    try:
        await open_mouth()
    except Exception as e:
        print("Error:", e)
    print("Script ended")

if __name__ == "__main__":
    asyncio.run(main())
