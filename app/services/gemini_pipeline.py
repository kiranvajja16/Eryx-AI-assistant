import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def ask_gemini(user_text: str) -> str:

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_text
    )

    return response.text