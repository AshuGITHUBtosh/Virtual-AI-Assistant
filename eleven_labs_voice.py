# eleven_labs_voice.py
import asyncio
import os
import tempfile
import threading
import random
import playsound
from elevenlabs import generate, save, set_api_key

# Optional: VTube Studio animation
try:
    import PyTubeStudio.client as pts
    import VtsModels.models as models
    ENABLE_VTS = True
except ImportError:
    ENABLE_VTS = False

# === CONFIG ===
set_api_key(os.getenv("ELEVEN_API_KEY", "ap2_6499a600-d564-463f-b107-8c3ab1b1c56d"))
DEFAULT_VOICE = "Rachel"

# === VTube Studio setup ===
if ENABLE_VTS:
    vts = pts.PyTubeStudio()

    async def inject_mouth(value: float):
        await vts.request(models.InjectParameterDataRequest(
            data=models.InjectParameterDataRequestData(
                parameter_values=[
                    models.ParameterValue(id="MouthOpen", value=value)
                ]
            )
        ))

    async def talk_simulation_while_audio_playing(audio_thread, speed=0.2):
        while audio_thread.is_alive():
            open_val = random.uniform(0.3, 0.5)
            await inject_mouth(open_val)
            await asyncio.sleep(speed / 2)
            await inject_mouth(0.0)
            await asyncio.sleep(speed / 2)
        await inject_mouth(0.0)

# === TTS Generation ===
async def synthesize_tts(text, voice=DEFAULT_VOICE):
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_monolingual_v1",
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
        save(audio, temp_path)

    try:
        from pydub.utils import mediainfo
        info = mediainfo(temp_path)
        duration = float(info["duration"])
    except Exception:
        duration = max(len(text.split()) * 0.5, 2)

    return temp_path, duration

# === Audio Player ===
def play_audio(path):
    playsound.playsound(path)

# === Main speak() function ===
def speak(text):
    import asyncio

    async def async_task():
        audio_path, _ = await synthesize_tts(text)

        # Connect to VTS if enabled
        if ENABLE_VTS:
            await vts.connect()
            await vts.authenticate()

        # Start audio thread
        audio_thread = threading.Thread(target=play_audio, args=(audio_path,))
        audio_thread.start()

        # Animate mouth if VTS enabled
        if ENABLE_VTS:
            await talk_simulation_while_audio_playing(audio_thread)

        audio_thread.join()

        if ENABLE_VTS:
            await vts.close()

        os.remove(audio_path)

    asyncio.run(async_task())
