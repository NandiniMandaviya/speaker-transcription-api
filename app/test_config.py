import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_SPEECH_ENDPOINT")
api_key = os.getenv("AZURE_SPEECH_API_KEY")

print("Endpoint:", endpoint)
print("API key loaded:", api_key is not None)