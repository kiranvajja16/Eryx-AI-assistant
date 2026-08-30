from fastapi import FastAPI, WebSocket
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

    await websocket.accept()

    print("ERYX: Client connected")

    audio_chunks = []

    try:

        while True:

            message = await websocket.receive()

            # Audio chunk
            if message.get("bytes") is not None:

                audio_data = message["bytes"]

                print(
                    f"Received audio chunk: {len(audio_data)} bytes"
                )

                audio_chunks.append(audio_data)

            # STOP message
            elif message.get("text") == "STOP":

                print("ERYX: Recording finished")

                break

    except Exception as e:

        print(f"WebSocket closed: {e}")