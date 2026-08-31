import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.tools.weather_tool import get_weather
from app.tools.reminder_tool import create_reminder, get_reminders
from app.tools.notes_tool import save_note, get_notes
from app.services.memory import (
    add_message,
    get_history
)


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)




def ask_gemini(text: str) -> str:

    add_message("user", text)

    history = get_history()

    conversation = []

    for message in history:
        conversation.append(
            f"{message['role']}: {message['content']}"
        )

    conversation_text = "\n".join(conversation)

    response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=conversation_text,

        config=types.GenerateContentConfig(

            system_instruction="""
You are ERYX, a helpful real-time AI voice assistant.

Remember the conversation and use previous messages
when answering follow-up questions.

Keep responses concise and natural because your
responses will be converted into speech.

Use available tools whenever necessary.
"""
            ,
            tools=[
                get_weather,
                create_reminder,
                get_reminders,
                save_note,
                get_notes
            ]
        )
    )

    answer = response.text

    add_message("assistant", answer)

    return answer