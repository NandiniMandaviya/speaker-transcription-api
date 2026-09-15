from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone

from app.speech_service import transcribe_audio

MAX_FILE_SIZE = 50 * 1024 * 1024

class TranscriptionResponse(BaseModel):
    filename: str
    timestamp: datetime
    transcript: str


app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Call Transcription API is running"
    }


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):

    if len(await file.read()) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size exceeds the 50 MB limit"
            )

    if not file.filename.lower().endswith(".wav"):
        raise HTTPException(
            status_code=400,
            detail="Only .wav files are supported"
        )

    audio_data = await file.read()

    await file.seek(0)

    timestamp = datetime.now(timezone.utc)

    transcript = transcribe_audio(file.file)

    return TranscriptionResponse(
        filename=file.filename,
        timestamp=timestamp,
        transcript=transcript
    )