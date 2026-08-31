import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from app.services.speech_pipeline import transcribe_audio
from app.services.gemini_pipeline import ask_gemini
from app.services.tts_pipeline import generate_speech, save_wav


app = FastAPI(title="ERYX AI Assistant")


# -------------------------
# HOME PAGE
# -------------------------

@app.get("/")
def home():
    return FileResponse("static/index.html")


# -------------------------
# HEALTH CHECK
# -------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# -------------------------
# AUDIO ENDPOINT
# -------------------------

@app.get("/audio")
def get_audio():

    return FileResponse(
        "data/eryx_response.wav",
        media_type="audio/wav"
    )


# -------------------------
# WEBSOCKET
# -------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    try:

        await websocket.accept()

        print("ERYX: Client connected")

        audio_chunks = []

        while True:

            message = await websocket.receive()

            # -------------------------
            # AUDIO MESSAGE
            # -------------------------

            if message.get("bytes") is not None:

                audio_data = message["bytes"]

                print(
                    f"Received audio chunk: {len(audio_data)} bytes"
                )

                audio_chunks.append(audio_data)

            # -------------------------
            # TEXT MESSAGE
            # -------------------------

            elif message.get("text") is not None:

                command = message["text"]

                print(f"Received command: {command}")

                # -------------------------
                # STOP RECORDING
                # -------------------------

                if command.lower() == "stop":

                    print("ERYX: Recording stopped")

                    # Combine all audio chunks
                    complete_audio = b"".join(audio_chunks)

                    # Make sure data folder exists
                    os.makedirs("data", exist_ok=True)

                    # -------------------------
                    # SAVE USER AUDIO
                    # -------------------------

                    audio_path = "data/recording.webm"

                    with open(audio_path, "wb") as audio_file:

                        audio_file.write(complete_audio)

                    print(
                        f"Audio saved: {audio_path}"
                    )

                    # -------------------------
                    # SPEECH TO TEXT
                    # -------------------------

                    print(
                        "Sending audio to Gemini..."
                    )

                    transcript = transcribe_audio(
                        audio_path
                    )

                    print(
                        "ERYX Transcript:",
                        transcript
                    )

                    # -------------------------
                    # ASK GEMINI
                    # -------------------------

                    answer = ask_gemini(
                        transcript
                    )

                    print(
                        "ERYX Answer:",
                        answer
                    )

                    # -------------------------
                    # SEND TEXT TO FRONTEND
                    # -------------------------

                    await websocket.send_text(
                        f"TRANSCRIPT:{transcript}"
                    )

                    await websocket.send_text(
                        f"ANSWER:{answer}"
                    )

                    # -------------------------
                    # TEXT TO SPEECH
                    # -------------------------

                    print(
                        "ERYX: Generating speech..."
                    )

                    audio_response = generate_speech(
                        answer
                    )

                    # -------------------------
                    # SAVE WAV FILE
                    # -------------------------

                    output_path = (
                        "data/eryx_response.wav"
                    )

                    save_wav(
                        audio_response,
                        output_path
                    )

                    print(
                        f"ERYX voice saved: {output_path}"
                    )

                    # -------------------------
                    # TELL FRONTEND
                    # -------------------------

                    await websocket.send_text(
                        "AUDIO_READY"
                    )

                    # -------------------------
                    # CLEAR OLD AUDIO CHUNKS
                    # -------------------------

                    audio_chunks = []


    except WebSocketDisconnect:

        print(
            "ERYX: Client disconnected"
        )


    except Exception as e:

        print(
            f"WebSocket error: {e}"
        )