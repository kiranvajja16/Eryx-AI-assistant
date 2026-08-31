import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


LIVE_MODEL = "gemini-3.1-flash-live-preview"


LIVE_CONFIG = types.LiveConnectConfig(

    # ERYX speaks using audio
    response_modalities=["AUDIO"],

    system_instruction=types.Content(
        role="system",
        parts=[
            types.Part(
                text=(
                    "You are ERYX, a helpful real-time voice assistant. "
                    "Speak naturally and concisely. "
                    "You can answer questions and use available tools "
                    "for reminders and notes. "
                    "Do not mention internal tools unless necessary."
                )
            )
        ]
    ),

    # User speech transcription
    input_audio_transcription=(
        types.AudioTranscriptionConfig()
    ),

    # ERYX speech transcription
    output_audio_transcription=(
        types.AudioTranscriptionConfig()
    ),

    # IMPORTANT
    # We control speech start/end manually
    realtime_input_config=types.RealtimeInputConfig(
        automatic_activity_detection=(
            types.AutomaticActivityDetection(
                disabled=True
            )
        )
    )
)


def create_live_session():

    return client.aio.live.connect(
        model=LIVE_MODEL,
        config=LIVE_CONFIG
    )