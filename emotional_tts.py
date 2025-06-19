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
                models.ParameterValue(
                    id="MouthOpen",
                    value=value
                )
            ]
        )
    ))

async def talk_simulation_while_audio_playing(audio_thread, speed: float = 0.2):
    """Simulate mouth movement while audio is playing."""
    print("🗣️ Starting mouth movement...")

    while audio_thread.is_alive():
        open_val = random.uniform(0.3, 0.5)  # More natural range
        await inject_mouth(open_val)
        await asyncio.sleep(speed / 2)

        await inject_mouth(0.0)
        await asyncio.sleep(speed / 2)

    # Make sure mouth is closed at the end
    await inject_mouth(0.0)
    print("✅ Mouth movement stopped with audio.")

async def synthesize_tts(text, voice="en-GB-LibbyNeural"):
    """Generate TTS audio with edge_tts and save to temp file, returning path and duration."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name

    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(temp_path)

    # Get duration using pydub if available
    try:
        from pydub.utils import mediainfo
        info = mediainfo(temp_path)
        duration = float(info["duration"])
    except Exception:
        duration = max(len(text.split()) * 0.5, 2)  # fallback estimate

    return temp_path, duration

def play_audio(path):
    """Play audio file (blocking)."""
    playsound.playsound(path)

def run_tts_and_mouth(text):
    loop = asyncio.new_event_loop()

    async def async_task():
        await vts.connect()
        await vts.authenticate()

        # Generate TTS audio
        audio_path, _ = await synthesize_tts(text)

        # Start playing audio in a thread
        audio_thread = threading.Thread(target=play_audio, args=(audio_path,))
        audio_thread.start()

        # Start mouth animation while audio is playing
        mouth_task = asyncio.create_task(talk_simulation_while_audio_playing(audio_thread))
        await mouth_task  # Wait until audio is done and mouth stops

        audio_thread.join()  # Ensure thread is finished

        await vts.close()

        # Clean up temp audio file
        os.remove(audio_path)

    loop.run_until_complete(async_task())

# ✅ Reusable function
def speak(text: str):
    run_tts_and_mouth(text)

if __name__ == "__main__":
    sample_text = "Hello master, I am your virtual anime assistant. How can I help you today?"
    speak(sample_text)