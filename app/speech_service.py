import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.transcription import TranscriptionClient
from azure.ai.transcription.models import (
    TranscriptionContent,
    TranscriptionOptions,
    TranscriptionDiarizationOptions,
)

load_dotenv()

class TranscriptionServiceError(Exception):
    pass

endpoint = os.getenv("AZURE_SPEECH_ENDPOINT")
api_key = os.getenv("AZURE_SPEECH_API_KEY")

client = TranscriptionClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key)
)


def transcribe_audio(audio_file):

    diarization_options = TranscriptionDiarizationOptions(
        enabled=True,
        max_speakers=5
    )

    options = TranscriptionOptions(
        diarization_options=diarization_options
    )

    try:
        result = client.transcribe(
                TranscriptionContent(
                    definition=options,
                    audio=audio_file
                )
            )

    except Exception as e:
        raise TranscriptionServiceError(
            "Transcription service failed"
        ) from e

    transcript_lines = []

    for phrase in result.phrases:
        speaker = phrase.speaker or "Unknown"

        transcript_lines.append(
            f"speaker_{speaker}: {phrase.text}"
        )

    return "\n\n".join(transcript_lines)