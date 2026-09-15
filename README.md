# speaker-transcription-api
This converts the conversation to speech along with speaker diarization.

FastAPI was selected as the REST API framework because the application is API-first and requires file upload handling, request validation, JSON responses, and automatically generated OpenAPI/Swagger documentation. FastAPI provides these capabilities directly with relatively little boilerplate. Flask can also implement the same API, but would require more manual setup or additional extensions for some of these features.

The test audio is taken from:
https://huggingface.co/datasets/apptek-com/apptek_callcenter_dialogues
Specifically, the diarization audio has been used since the project is also concerned with distinguishing various speakers from the audio.

