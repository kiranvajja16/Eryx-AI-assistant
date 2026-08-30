from app.services.speech_pipeline import transcribe_audio


audio_file = "data/3.mp3"

transcript = transcribe_audio(audio_file)

print("\n--- ERYX TRANSCRIPT ---")
print(transcript)