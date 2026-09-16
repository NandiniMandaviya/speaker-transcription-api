from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, timezone

from app.validations import validate_file

from app.speech_service import transcribe_audio, TranscriptionServiceError

class TranscriptionResponse(BaseModel):
    filename: str
    timestamp: datetime
    transcript: str


app = FastAPI()

@app.exception_handler(TranscriptionServiceError)
async def transcription_service_error_handler(request: Request, exc: TranscriptionServiceError):
    return JSONResponse(
        status_code=502,
        content={
            "detail": str(exc)
        }
    )

@app.get("/")
def root():
    return {
        "message": "Call Transcription API is running"
    }


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):

    await validate_file(file)

    timestamp = datetime.now(timezone.utc)

    transcript = transcribe_audio(file.file)

    # Console output
    print("\n" + "=" * 70)
    print(f"File: {file.filename}")
    print(f"Timestamp: {timestamp}")
    print("=" * 70)
    print(transcript)
    print("=" * 70 + "\n")

    # Save transcript to file
    with open("transcript.txt", "a", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write(f"File: {file.filename}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("=" * 70 + "\n")
        f.write(transcript)
        f.write("\n\n")

    return TranscriptionResponse(
        filename=file.filename,
        timestamp=timestamp,
        transcript=transcript
    )