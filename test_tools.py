from app.services.gemini_pipeline import ask_gemini


questions = [
    "What is the weather in Hyderabad?",
    "Remind me to study Python at 7 PM.",
    "Save a note saying I need to finish my ERYX project."
]


for question in questions:

    print("\nYOU:", question)

    answer = ask_gemini(question)

    print("ERYX:", answer)