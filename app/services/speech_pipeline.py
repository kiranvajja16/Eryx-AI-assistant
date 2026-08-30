import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def transcribe_audio(audio_path: str)->str:
    audio_file= client.files.upload(
        file=audio_path,
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            "Transcribe the audio exactly.Return only the spoken words.",
            audio_file
        ]
    )

    return response.text