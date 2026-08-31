import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def ask_gemini(user_text: str) -> str:

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            f"""
    you are ERYX, a helpful real-time AI VOICE assistant.
    Answer the user's question clearly and naturally.
    User question:{user_text}
"""
        ]
    )

    return response.text