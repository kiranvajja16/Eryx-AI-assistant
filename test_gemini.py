from app.services.gemini_pipeline import ask_gemini


question = "Who is S. S. Rajamouli?"

answer = ask_gemini(question)

print("\n--- ERYX ---")
print(answer)