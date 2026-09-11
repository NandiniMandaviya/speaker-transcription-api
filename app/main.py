from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Call Transcription API is running"
    }