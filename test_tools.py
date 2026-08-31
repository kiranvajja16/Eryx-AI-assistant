from app.services.gemini_pipeline import ask_gemini

question = "Save a note saying I need to finish my ERYX project."

print("YOU:", question)

answer = ask_gemini(question)

print("ERYX:", answer)