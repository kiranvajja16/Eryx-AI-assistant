from app.services.tts_pipeline import generate_speech


text = "Hello. I am ERYX, your AI assistant."

audio = generate_speech(text)

with open("data/eryx_test.wav", "wb") as file:
    file.write(audio)

print("ERYX voice generated successfully!")