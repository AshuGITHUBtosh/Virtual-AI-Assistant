import zipfile
import os
from PIL import Image, ImageDraw

# Create a working directory
project_dir = "/mnt/data/simple_talking_avatar"
os.makedirs(project_dir, exist_ok=True)

# Create avatar face image (placeholder anime face)
avatar_path = os.path.join(project_dir, "avatar.png")
img = Image.new("RGB", (512, 512), color=(255, 228, 235))  # light pink
draw = ImageDraw.Draw(img)
draw.ellipse((180, 150, 240, 210), fill="black")  # left eye
draw.ellipse((270, 150, 330, 210), fill="black")  # right eye
draw.arc((220, 300, 300, 340), start=0, end=180, fill="red", width=3)  # smiling mouth
img.save(avatar_path)

# Create simple index.html
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Simple Anime Avatar</title>
  <style>
    body { background: #000; display: flex; justify-content: center; align-items: center; height: 100vh; }
    canvas { border: 2px solid #ccc; }
  </style>
</head>
<body>
  <canvas id="canvas" width="512" height="512"></canvas>
  <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    const avatarImg = new Image();
    avatarImg.src = 'avatar.png';

    const mouthY = 400;
    const mouthWidth = 80;
    const mouthHeight = 10;

    let mouthOpen = 0;

    avatarImg.onload = () => {
      drawFrame();
      startLipSync();
    };

    function drawFrame() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(avatarImg, 0, 0, canvas.width, canvas.height);

      if (mouthOpen > 0.05) {
        ctx.fillStyle = 'red';
        ctx.fillRect((canvas.width - mouthWidth) / 2, mouthY, mouthWidth, mouthHeight * mouthOpen);
      }

      requestAnimationFrame(drawFrame);
    }

    function startLipSync() {
      const audio = new Audio('voice.mp3');
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const src = audioCtx.createMediaElementSource(audio);
      const analyser = audioCtx.createAnalyser();
      src.connect(analyser);
      analyser.connect(audioCtx.destination);
      analyser.fftSize = 512;

      const dataArray = new Uint8Array(analyser.frequencyBinCount);

      function updateMouth() {
        analyser.getByteFrequencyData(dataArray);
        const volume = dataArray.reduce((a, b) => a + b, 0) / dataArray.length;
        mouthOpen = Math.min(volume / 100, 1.0);
        requestAnimationFrame(updateMouth);
      }

      audio.play().then(() => {
        audioCtx.resume();
        updateMouth();
      });
    }
  </script>
</body>
</html>
"""

with open(os.path.join(project_dir, "index.html"), "w") as f:
    f.write(html_content)

# Create a zip file of the project
zip_path = "/mnt/data/simple_talking_avatar.zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, project_dir))

zip_path
