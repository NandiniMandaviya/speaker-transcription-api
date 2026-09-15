from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone

from app.speech_service import transcribe_audio


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

    if not file.filename.lower().endswith(".wav"):
        raise HTTPException(
            status_code=400,
            detail="Only .wav files are supported"
        )

    timestamp = datetime.now(timezone.utc)

    transcript = transcribe_audio(file.file)

    return TranscriptionResponse(
        filename=file.filename,
        timestamp=timestamp,
        transcript=transcript
    )