import asyncio
import edge_tts
import tempfile
import os
import playsound
import threading
import random
import PyTubeStudio.client as pts
import VtsModels.models as models

vts = pts.PyTubeStudio()

async def inject_mouth(value: float):
    """Set the MouthOpen parameter to the given value (0.0 to 1.0)."""
    await vts.request(models.InjectParameterDataRequest(
        data=models.InjectParameterDataRequestData(
            parameter_values=[
                models.ParameterValue(id="MouthOpen", value=value),
                models.ParameterValue(id="MouthSmile", value=-2.0),
                models.ParameterValue(id="BrowRightY", value=-1.0),
                models.ParameterValue(id="BrowLeftY", value=-1.0),
                models.ParameterValue(id="EyeOpenLeft", value=0.3),
                 models.ParameterValue(id="EyeOpenRight", value=0.3)

            ]
        )
    ))

async def inject_sad_expression():
    """Inject parameters to make the model look sad/concerned."""
    await vts.request(models.InjectParameterDataRequest(
        data=models.InjectParameterDataRequestData(
            parameter_values=[
                models.ParameterValue(id="EyeSmile", value=0.0),       # remove smiling eyes
                models.ParameterValue(id="Brows", value=-0.6),         # lower brows (or raise based on model)
                #models.ParameterValue(id="Sad", value=1.0),            # full sad expression (if available)
                models.ParameterValue(id="MouthSmile", value=1.0),
            ]
        )
    ))

async def reset_expression():
    """Reset expression parameters back to neutral."""
    await vts.request(models.InjectParameterDataRequest(
        data=models.InjectParameterDataRequestData(
            parameter_values=[
                models.ParameterValue(id="EyeSmile", value=1.0),
                models.ParameterValue(id="Brows", value=0.0),
                models.ParameterValue(id="Sad", value=0.0),
            ]
        )
    ))

async def talk_simulation_while_audio_playing(audio_thread, speed: float = 0.2):
    """Simulate mouth movement while audio is playing."""
    print("🗣️ Starting mouth movement...")
    await inject_sad_expression()  # Set sad look

    while audio_thread.is_alive():
        open_val = random.uniform(0.3, 0.5)
        await inject_mouth(open_val)
        await asyncio.sleep(speed / 2)

        await inject_mouth(0.0)
        await asyncio.sleep(speed / 2)

    await inject_mouth(0.0)
    await reset_expression()  # Reset expression at the end
    print("✅ Mouth movement and expression stopped.")

async def synthesize_tts(text, voice="en-GB-LibbyNeural"):
    """Generate TTS audio and return path and duration."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name

    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(temp_path)

    try:
        from pydub.utils import mediainfo
        info = mediainfo(temp_path)
        duration = float(info["duration"])
    except Exception:
        duration = max(len(text.split()) * 0.5, 2)

    return temp_path, duration

def play_audio(path):
    playsound.playsound(path)

def run_tts_and_mouth(text):
    loop = asyncio.new_event_loop()

    async def async_task():
        await vts.connect()
        await vts.authenticate()

        audio_path, _ = await synthesize_tts(text)

        audio_thread = threading.Thread(target=play_audio, args=(audio_path,))
        audio_thread.start()

        mouth_task = asyncio.create_task(talk_simulation_while_audio_playing(audio_thread))
        await mouth_task
        audio_thread.join()

        await vts.close()
        os.remove(audio_path)

    loop.run_until_complete(async_task())

def speak_emotional(text: str):
    run_tts_and_mouth(text)

if __name__ == "__main__":
    sample_text = "I'm feeling really down today... I wish I could make you smile."
    speak_emotional(sample_text)
