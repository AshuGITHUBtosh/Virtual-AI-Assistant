import asyncio
import PyTubeStudio.client as pts
import VtsModels.models as models
import random

vts = pts.PyTubeStudio()

async def inject_mouth(value: float):
    """Set the MouthOpen parameter to the given value (0.0 to 1.0)."""
    await vts.request(models.InjectParameterDataRequest(
        data=models.InjectParameterDataRequestData(
            parameter_values=[
                models.ParameterValue(
                    id="MouthOpen",
                    value=value
                )
            ]
        )
    ))

async def talk_simulation(duration: float = 5.0, speed: float = 0.15):
    """Simulate the mouth moving up/down for 'duration' seconds."""
    print("🗣️ Starting fake talking...")
    end_time = asyncio.get_event_loop().time() + duration

    while asyncio.get_event_loop().time() < end_time:
        # Random open value to mimic human variation
        open_val = random.uniform(0.2, 1.0)
        await inject_mouth(open_val)
        await asyncio.sleep(speed / 2)

        await inject_mouth(0.0)
        await asyncio.sleep(speed / 2)

    print("✅ Done talking.")

async def main():
    await vts.connect()
    await vts.authenticate()
    print("✅ Authenticated with VTube Studio")

    await talk_simulation(duration=5)  # Mouth moves for 5 seconds

    await vts.close()

asyncio.run(main())
