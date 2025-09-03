from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from backendRag folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file")
print("✅ GOOGLE_API_KEY loaded:", api_key[:6] + "*****")


from .ragGeneration import get_answer
import re

app = FastAPI()

# Allow requests from your frontend (local or Chrome extension)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev. Later restrict to ["chrome-extension://<EXTENSION_ID>"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class AskRequest(BaseModel):
    videoUrl: str
    question: str

# Function to extract video_id from YouTube URL
def extract_video_id(url: str) -> str:
    """
    Handles normal, shorts, and embed YouTube URLs.
    """
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",   # standard YouTube link
        r"youtu\.be/([a-zA-Z0-9_-]{11})",  # short links
        r"shorts/([a-zA-Z0-9_-]{11})",     # shorts links
        r"embed/([a-zA-Z0-9_-]{11})"       # embed links
    ]
    for p in patterns:
        match = re.search(p, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL")

# API endpoint
@app.post("/ask")
async def ask_question(req: AskRequest):
    try:
        video_id = extract_video_id(req.videoUrl)
        answer = get_answer(video_id, req.question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
