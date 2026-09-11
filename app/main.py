from fastapi import FastAPI, UploadFile, File, HTTPException


app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Call Transcription API is running"
    }

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".wav"):
        raise HTTPException(
            status_code=400,
            detail="Only .wav files are supported"
        )

    audio_data = await file.read()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(audio_data),
        "message": "Audio received successfully"
    }