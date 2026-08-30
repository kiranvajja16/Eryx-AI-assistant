import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
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

            # Audio data
            if message["type"] == "websocket.receive":

                if message.get("bytes") is not None:

                    audio_data = message["bytes"]

                    print(
                        f"Received audio chunk: {len(audio_data)} bytes"
                    )

                    audio_chunks.append(audio_data)

                # Text message
                elif message.get("text") is not None:

                    command = message["text"]

                    print(f"Received command: {command}")

                    if command == "stop":

                        print("ERYX: Recording stopped")

                        # Combine all audio chunks
                        complete_audio = b"".join(audio_chunks)

                        os.makedirs("data", exist_ok=True)

                        audio_path = "data/recording.webm"

                        with open(audio_path, "wb") as audio_file:
                            audio_file.write(complete_audio)

                        print(
                            f"Audio saved: {audio_path}"
                        )

                        # Clear chunks for next recording
                        audio_chunks = []

                        await websocket.send_text(
                            "Audio saved successfully"
                        )

    except WebSocketDisconnect:

        print("ERYX: Client disconnected")

    except Exception as e:

        print(f"WebSocket error: {e}")