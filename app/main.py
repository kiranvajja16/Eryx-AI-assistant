import asyncio
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from google.genai import types

from app.services.live_pipeline import create_live_session


app = FastAPI(title="ERYX AI Assistant")


# ==========================================
# HOME
# ==========================================

@app.get("/")
async def home():

    return FileResponse(
        "static/index.html"
    )


# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


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
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    print("ERYX: Client connected")

    try:

        async with create_live_session() as session:

            print(
                "ERYX: Gemini Live session connected"
            )


            # ======================================
            # BROWSER → GEMINI
            # ======================================

            async def browser_to_gemini():

                try:

                    while True:

                        message = (
                            await websocket.receive()
                        )


                        # ==================================
                        # AUDIO
                        # ==================================

                        if message.get("bytes") is not None:

                            audio_data = message["bytes"]

                            print(
                                f"PCM audio received: "
                                f"{len(audio_data)} bytes"
                            )

                            await session.send_realtime_input(
                                audio=types.Blob(
                                    data=audio_data,
                                    mime_type="audio/pcm;rate=16000"
                                )
                            )


                        # ==================================
                        # TEXT COMMAND
                        # ==================================

                        elif message.get("text") is not None:

                            command = message["text"]

                            print(
                                f"Browser message: {command}"
                            )


                            # ------------------------------
                            # START NEW TURN
                            # ------------------------------

                            if command.upper() == "START":

                                print(
                                    "ERYX: Starting new turn"
                                )

                                await session.send_realtime_input(
                                    activity_start=(
                                        types.ActivityStart()
                                    )
                                )


                            # ------------------------------
                            # END CURRENT TURN
                            # ------------------------------

                            elif command.upper() == "STOP":

                                print(
                                    "ERYX: Ending turn"
                                )

                                await session.send_realtime_input(
                                    activity_end=(
                                        types.ActivityEnd()
                                    )
                                )


                            # ------------------------------
                            # TEXT INPUT
                            # ------------------------------

                            else:

                                await session.send_realtime_input(
                                    text=command
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

                    async for response in session.receive():

                        server_content = (
                            response.server_content
                        )


                        if not server_content:
                            continue


                        # ==================================
                        # MODEL AUDIO
                        # ==================================

                        if server_content.model_turn:

                            for part in (
                                server_content
                                .model_turn
                                .parts
                            ):

                                if part.inline_data:

                                    audio_data = (
                                        part.inline_data.data
                                    )

                                    print(
                                        "ERYX audio received:",
                                        len(audio_data),
                                        "bytes"
                                    )

                                    await websocket.send_bytes(
                                        audio_data
                                    )


                        # ==================================
                        # USER TRANSCRIPT
                        # ==================================

                        if (
                            server_content
                            .input_transcription
                        ):

                            transcript = (
                                server_content
                                .input_transcription
                                .text
                            )

                            if transcript:

                                print(
                                    "YOU:",
                                    transcript
                                )

                                await websocket.send_text(
                                    json.dumps({
                                        "type": "transcript",
                                        "text": transcript
                                    })
                                )


                        # ==================================
                        # ERYX TRANSCRIPT
                        # ==================================

                        if (
                            server_content
                            .output_transcription
                        ):

                            transcript = (
                                server_content
                                .output_transcription
                                .text
                            )

                            if transcript:

                                print(
                                    "ERYX:",
                                    transcript
                                )

                                await websocket.send_text(
                                    json.dumps({
                                        "type": "answer",
                                        "text": transcript
                                    })
                                )


                        # ==================================
                        # TURN COMPLETE
                        # ==================================

                        if (
                            server_content
                            .turn_complete
                        ):

                            print(
                                "ERYX: Turn complete"
                            )

                            await websocket.send_text(
                                json.dumps({
                                    "type": "turn_complete"
                                })
                            )


                except Exception as e:

                    print(
                        f"Gemini → Browser error: {e}"
                    )


            # ======================================
            # RUN BOTH TASKS
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