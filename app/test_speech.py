import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.transcription import TranscriptionClient
from azure.ai.transcription.models import (
    TranscriptionContent,
    TranscriptionOptions,
    TranscriptionDiarizationOptions,
)

# Load environment variables
load_dotenv()

endpoint = os.getenv("AZURE_SPEECH_ENDPOINT")
api_key = os.getenv("AZURE_SPEECH_API_KEY")

# Create Azure Speech client
client = TranscriptionClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key)
)

# Path to the audio file
audio_path = r"C:\Users\Admin\Desktop\Speaker Transcription API\test_audio\call.wav"

# Get only the filename
file_name = os.path.basename(audio_path)

# Send audio to Azure Speech
with open(audio_path, "rb") as audio_file:

    diarization_options = TranscriptionDiarizationOptions(
        enabled=True,
        max_speakers=2
    )

    options = TranscriptionOptions(
        locales=["en-IN"],
        diarization_options=diarization_options
    )

    result = client.transcribe(
        TranscriptionContent(
            definition=options,
            audio=audio_file
        )
    )

# Build transcript
# Build transcript
transcript_lines = []

for phrase in result.phrases:
    speaker = phrase.speaker or "Unknown"

    transcript_lines.append(
        f"speaker_{speaker}: {phrase.text}"
    )

transcript = "\n\n".join(transcript_lines)

# Append transcript to transcript.txt
with open("transcript.txt", "a", encoding="utf-8") as file:
    file.write(f"Filename: {file_name}\n")
    file.write("=" * 60 + "\n")
    file.write(transcript)
    file.write("\n\n" + "=" * 60 + "\n\n")

print("Transcript saved to transcript.txt")