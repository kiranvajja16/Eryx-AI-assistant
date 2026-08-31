import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.tools.weather_tool import get_weather
from app.tools.reminder_tool import create_reminder
from app.tools.notes_tool import save_note


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(text: str) -> str:

    response = client.models.generate_content(
        model="gemini-3.6-flash",

        contents=text,

        config=types.GenerateContentConfig(
            tools=[
                get_weather,
                create_reminder,
                save_note
            ]
        )
    )

    return response.text