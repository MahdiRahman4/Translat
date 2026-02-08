import os
from fastapi import FastAPI, UploadFile, File 
from fastapi.middleware.cors import CORSMiddleware
import subprocess
from openai import OpenAI
# from dotenv import load_dotenv
# load_dotenv()
app = FastAPI()
import whisper
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
async def handleFile(file : UploadFile = File(...)):
  print("=== FILE RECEIVED ===")  
  print(f"Filename: {file.filename}")  
  print(f"Content-Type: {file.content_type}")  
  contents = await file.read()
  print(f"Size: {len(contents)} bytes")  

  upload_dir = 'uploads'
  os.makedirs(upload_dir, exist_ok=True)
  file_path = os.path.join(upload_dir,file.filename)
  with open(file_path, 'wb') as f:
    f.write(contents)
  output_path = file_path.rsplit(".", 1)[0] + ".mp3"
  convertToAudio(file_path, output_path)
  # transcribeAudio(output_path)
  model = whisper.load_model("base")
  result = model.transcribe(output_path, language="ar") 
  print(result["text"])
  return {"message": "File uploaded successfully", "file_path": output_path, "success":True}


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
      os.remove(inputFile)

    except subprocess.CalledProcessError as e:
      print("Failure to convert")
#TODO GET OPENAI TRANSCRIPTION API KEY BILL WORKING
# def transcribeAudio(filePath):
#   audio_file= open(filePath, "rb")
#   transcription = client.audio.transcriptions.create(
#     model="gpt-4o-transcribe", 
#     file=audio_file,
#     response_format="text"
  
# )
#   print(transcription.text) 
