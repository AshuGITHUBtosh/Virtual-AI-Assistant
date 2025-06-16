import asyncio
import websockets
import json

async def request_and_save_token():
    uri = "ws://localhost:8001"

    async with websockets.connect(uri) as ws:
        # Step 1: Send AuthenticationTokenRequest
        token_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "getToken",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": "MouthOpenerScript",
                "pluginDeveloper": "YourNameHere"
            }
        }

        await ws.send(json.dumps(token_request))
        response = await ws.recv()
        print("📥 Token response received:\n", response)

        # Step 2: Extract and save token
        data = json.loads(response)
        token = data.get("data", {}).get("authenticationToken")
        
        if token:
            with open("auth_token.json", "w") as f:
                json.dump({"token": token}, f)
            print("✅ Token saved to auth_token.json")
        else:
            print("❌ Failed to get token. Make sure you approved the popup in VTube Studio.")

# Run the async function
asyncio.run(request_and_save_token())
