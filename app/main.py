import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from app.services.speech_pipeline import transcribe_audio


app = FastAPI(title="ERYX AI Assistant")


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


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

                    # Combine audio chunks
                    complete_audio = b"".join(audio_chunks)

                    # Make sure data folder exists
                    os.makedirs("data", exist_ok=True)

                    # Save recording
                    audio_path = "data/recording.webm"

                    with open(audio_path, "wb") as audio_file:
                        audio_file.write(complete_audio)

                    print(f"Audio saved: {audio_path}")

                    # -------------------------
                    # SPEECH TO TEXT
                    # -------------------------

                    print("Sending audio to Gemini...")

                    transcript = transcribe_audio(audio_path)

                    print("ERYX Transcript:", transcript)

                    # Send transcript to browser
                    await websocket.send_text(
                        f"TRANSCRIPT:{transcript}"
                    )

                    # Clear old audio
                    audio_chunks = []


    except WebSocketDisconnect:

        print("ERYX: Client disconnected")

    except Exception as e:

        print(f"WebSocket error: {e}")