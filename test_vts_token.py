import asyncio
import websockets
import json

async def get_token():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "authTokenRequest",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": "VIGF-TTS",
                "pluginDeveloper": "OpenAI GPT"
            }
        }))
        response = await websocket.recv()
        print("✅ Response from VTube Studio:\n", response)

asyncio.run(get_token())
