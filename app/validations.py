from fastapi import HTTPException
import wave

MAX_FILE_SIZE = 50 * 1024 * 1024


async def validate_file_size(file):
    audio_data = await file.read()

    if len(audio_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 50 MB limit"
        )

    await file.seek(0)


async def validate_file_extension(file):
    if not file.filename.lower().endswith(".wav"):
        raise HTTPException(
            status_code=400,
            detail="Only .wav files are supported"
        )


async def validate_wav_format(file):
    try:
        with wave.open(file.file, "rb") as wav_file:
            channels = wav_file.getnchannels()
            sample_rate = wav_file.getframerate()

    except wave.Error:
        raise HTTPException(
            status_code=400,
            detail="Invalid WAV file"
        )

    await file.seek(0)


async def validate_file(file):
    await validate_file_size(file)
    await validate_file_extension(file)
    await validate_wav_format(file)