import asyncio
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from app.services.live_pipeline import create_live_session


app = FastAPI(title="ERYX AI Assistant")


# ==========================================
# HOME
# ==========================================

@app.get("/")
async def home():
    return FileResponse("static/index.html")


# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
async def health():
    return {"status": "healthy"}


# ==========================================
# PCM PROCESSOR
# ==========================================

@app.get("/pcm-processor.js")
async def pcm_processor():
    return FileResponse(
        "static/pcm-processor.js",
        media_type="application/javascript"
    )


# ==========================================
# WEBSOCKET
# ==========================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    print("ERYX: Client connected")

    try:

        # ONE Gemini Live session
        # stays alive for multiple turns.

        async with create_live_session() as session:

            print("ERYX: Gemini Live session connected")

            # ======================================
            # BROWSER → GEMINI
            # ======================================

            async def browser_to_gemini():

                try:

                    while True:

                        message = await websocket.receive()

                        # ==================================
                        # PCM AUDIO
                        # ==================================

                        if message.get("bytes") is not None:

                            audio_data = message["bytes"]

                            print(
                                f"PCM audio received: "
                                f"{len(audio_data)} bytes"
                            )

                            await session.send_realtime_input(
                                audio={
                                    "data": audio_data,
                                    "mime_type": "audio/pcm;rate=16000"
                                }
                            )

                        # ==================================
                        # TEXT COMMAND
                        # ==================================

                        elif message.get("text") is not None:

                            text = message["text"]

                            print(
                                f"Browser message: {text}"
                            )

                            # ------------------------------
                            # END CURRENT TURN
                            # ------------------------------

                            if text.upper() == "STOP":

                                print(
                                    "ERYX: Ending turn"
                                )

                                await session.send_realtime_input(
                                    audio_stream_end=True
                                )

                except WebSocketDisconnect:

                    print(
                        "ERYX: Browser disconnected"
                    )

                except Exception as e:

                    print(
                        f"Browser → Gemini error: {e}"
                    )


            # ======================================
            # GEMINI → BROWSER
            # ======================================

            async def gemini_to_browser():

                try:

                    while True:

                        # Create a new receive iterator for each turn
                        receive_stream = session.receive()

                        async for response in receive_stream:

                            if not response.server_content:
                                continue

                            content = response.server_content

                            # ==================================
                            # ERYX AUDIO
                            # ==================================

                            if content.model_turn:

                                for part in content.model_turn.parts:

                                    if part.inline_data:

                                        audio_data = part.inline_data.data

                                        print(
                                            f"ERYX audio received: "
                                            f"{len(audio_data)} bytes"
                                        )

                                        await websocket.send_bytes(
                                            audio_data
                                        )

                            # ==================================
                            # USER TRANSCRIPT
                            # ==================================

                            if content.input_transcription:

                                text = (
                                    content
                                    .input_transcription
                                    .text
                                )

                                if text:

                                    print(
                                        "YOU:",
                                        text
                                    )

                                    await websocket.send_text(
                                        json.dumps({
                                            "type": "transcript",
                                            "text": text
                                        })
                                    )

                            # ==================================
                            # ERYX TRANSCRIPT
                            # ==================================

                            if content.output_transcription:

                                text = (
                                    content
                                    .output_transcription
                                    .text
                                )

                                if text:

                                    print(
                                        "ERYX:",
                                        text
                                    )

                                    await websocket.send_text(
                                        json.dumps({
                                            "type": "answer",
                                            "text": text
                                        })
                                    )

                            # ==================================
                            # TURN COMPLETE
                            # ==================================

                            if content.turn_complete:

                                print(
                                    "ERYX: Turn complete"
                                )

                                await websocket.send_text(
                                    json.dumps({
                                        "type": "turn_complete"
                                    })
                                )

                                # IMPORTANT:
                                # Break this receive iterator.
                                # The outer while loop will create
                                # a fresh receive iterator for the
                                # next turn.

                                break

                except WebSocketDisconnect:

                    print(
                        "ERYX: Browser disconnected"
                    )

                except Exception as e:

                    print(
                        f"Gemini receive error: {e}"
                    )
            # ======================================
            # KEEP BOTH TASKS RUNNING
            # ======================================

            await asyncio.gather(
                browser_to_gemini(),
                gemini_to_browser()
            )


    except WebSocketDisconnect:

        print(
            "ERYX: Client disconnected"
        )

    except Exception as e:

        print(
            f"WebSocket error: {e}"
        )