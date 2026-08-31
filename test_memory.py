from app.services.gemini_pipeline import ask_gemini

print("YOU: My name is Kiran")

answer = ask_gemini(
    "My name is Kiran"
)

print("ERYX:", answer)


print("\nYOU: What is my name?")

answer = ask_gemini(
    "What is my name?"
)

print("ERYX:", answer)