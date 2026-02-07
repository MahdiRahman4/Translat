import os
from fastapi import FastAPI, UploadFile, File as file
from fastapi.middleware.cors import CORSMiddleware
import subprocess
app = FastAPI()

files = []

origins=[
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/uploadFile")
async def handleFile(file : UploadFile = file(...)):
  contents = await file.read()
  upload_dir = 'uploads'
  os.makedirs(upload_dir, exist_ok=True)
  file_path = os.path.join(upload_dir,file.filename)
  with open(file_path, 'wb') as f:
    f.write(contents)
  output_path = file_path.rsplit(".", 1)[0] + ".mp3"
  convertToAudio(file_path, output_path)
  


def convertToAudio(inputFile, outputFile):
    ffmpeg_cmd = [
      "ffmpeg",
      "-i", inputFile,
      "-vn",
      "-acodec", "libmp3lame",
      "-ab", "192k",
      "-ar", "44100",
      "-y",
      outputFile
    ]
    try:
      subprocess.run(ffmpeg_cmd, check=True)
      print("Success!")
    except subprocess.CalledProcessError as e:
      print("Failure to convert")
    finally:
      if os.path.exists(inputFile):
        os.remove(inputFile)
