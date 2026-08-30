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

    print(" ERYX: Client connected")

    try:

        while True:

            audio_data = await websocket.receive_bytes()

            print(
                f" Received audio chunk: {len(audio_data)} bytes"
            )

            await websocket.send_text(
                "Audio received by ERYX" 
            )

    except Exception as e:

        print(f" WebSocket closed: {e}")