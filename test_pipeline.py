from app.services.speech_pipeline import transcribe_audio
from app.services.gemini_pipeline import ask_gemini


audio_file = "data/3.mp3"

print("1. Transcribing audio...")

transcript = transcribe_audio(audio_file)

print("\n--- ERYX TRANSCRIPT ---")
print(transcript)


print("\n2. Sending transcript to Gemini...")

answer = ask_gemini(transcript)

print("\n--- ERYX ANSWER ---")
print(answer)