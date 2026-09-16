# Speaker Transcription API

A REST API that accepts a `.wav` call recording and returns a text transcript with speaker diarization.

The API uses **FastAPI** for the REST interface and **Azure AI Speech** for speech-to-text transcription and speaker diarization.

## Features

- Accepts `.wav` audio files through a REST API
- Validates the uploaded file
- Validates WAV format
- Enforces a maximum file size of 50 MB
- Converts speech to text
- Identifies different speakers using speaker diarization
- Returns the transcript as a single formatted string
- Returns the uploaded filename and transcription timestamp
- Provides automatically generated Swagger/OpenAPI documentation
- Handles transcription service failures with appropriate HTTP responses

## How It Works

The overall flow of the application is:

```text
Client / Postman
      |
      | POST /transcribe
      | .wav file
      v
   FastAPI
      |
      v
File Validation
      |
      | Valid WAV file
      v
Azure AI Speech
      |
      | Speech-to-text
      | Speaker diarization
      v
Transcript Formatting
      |
      v
JSON Response
```

## Technical Justifications

### Why FastAPI?

FastAPI was selected as the REST API framework because the application is API-first and requires:

- File upload handling
- Request validation
- JSON responses
- HTTP exception handling
- Automatic OpenAPI/Swagger documentation

FastAPI provides these capabilities with relatively little boilerplate.

Flask could also be used to implement the same API, but some of these capabilities would require additional extensions or more manual configuration. FastAPI therefore fits the requirements of this project well.

### Why Azure AI Speech?

Azure AI Speech is used as the transcription backend because the project requires both:

- Speech-to-text transcription
- Speaker diarization

The API is configured for Indian English (`en-IN`) and enables speaker diarization with a maximum of two speakers for the current use case.

The Azure Speech integration is isolated in `speech_service.py`, keeping the API layer separate from the transcription service implementation.

## Test Audio

The test audio used during development was obtained from the following Hugging Face dataset:

**AppTek Call Center Dialogues**

The diarization configuration was used because the project requires speaker identification in addition to speech-to-text transcription.

The dataset contains call-center conversations with speaker-labelled dialogue, making it useful for testing the diarization functionality of the API.

Test audio files are not included in the Git repository.

## Testing

## Testing Specifications

The API was tested using Swagger UI and Postman with the following test cases.

- Valid `.wav` file → `200 OK`
- Invalid file type → `400 Bad Request`
- Invalid/corrupt WAV file → `400 Bad Request`
- File over 50 MB → `413 Request Entity Too Large`
- Invalid Azure credentials → `502 Bad Gateway`
- Speaker diarization → Speakers identified correctly


## How to Test the API

After cloning the repository, creating the virtual environment and installing requirements, follow the below steps to test it:

### Start the API
uvicorn app.main:app --reload

The API will start at- http://127.0.0.1:8000
Open the following URL in browser: http://127.0.0.1:8000/docs

#### From Swagger UI:

1. Open POST /transcribe
2. Click Try it out
3. Upload a .wav file
4. Click Execute
5. View the diarized transcript in the response

#### From Postman:

Alternatively, send a POST request to: http://127.0.0.1:8000/transcribe

Use Body → form-data:
Key	Type	Value
file	File	<your .wav file>