ERYX --- Real-Time AI Voice Assistant

ERYX is a low-latency, real-time AI voice assistant that accepts spoken
commands, understands them using Gemini Live, performs useful actions
through tools, and speaks the response back to the user.

The project was built as a working end-to-end prototype with streaming
audio, WebSockets, an LLM, persistent notes/reminders, and voice
interaction.

Features

🎙️ Real-time microphone input

🔊 Streaming voice responses from ERYX

🧠 Gemini Live for real-time conversational intelligence

🔌 WebSocket communication between browser and FastAPI backend

🎚️ PCM audio processing using an AudioWorkletProcessor

📝 Save and retrieve notes

⏰ Create and retrieve reminders

🔄 Multi-turn conversation handling

🗣️ Voice interruption / turn lifecycle handling

⚡ Low-latency streaming pipeline

🗣️ Wake-word detection

💾 SQLite database for persistent notes and reminders

❤️ Health-check endpoint for the backend

Project Requirements / Mentor Specification

The project follows the Real-Time Voice Assistant track.

Core requirements

Stream audio to speech-to-text while the user talks.

Use an LLM with function/tool calling to trigger real actions.

Stream the spoken response back with low latency.

Handle user interruptions (barge-in) gracefully.

For the real actions, this implementation focuses on the two requested
tools:

Reminder tool

Notes tool

A weather tool was intentionally not included in the final scope.

How It Works

Microphone
    │
    ▼
Browser AudioWorklet
    │
    │ PCM 16-bit audio
    ▼
WebSocket
    │
    ▼
FastAPI Backend
    │
    ▼
Gemini Live
    │
    ├── Speech understanding
    ├── Conversation
    └── Tool calling
          │
          ├── Reminder Tool ──► SQLite
          │
          └── Notes Tool ─────► SQLite
    │
    ▼
Streaming Gemini Audio
    │
    ▼
WebSocket
    │
    ▼
Browser Audio Playback
    │
    ▼
User hears ERYX

Technology Stack

Frontend

HTML

CSS

JavaScript

Web Audio API

AudioWorklet

WebSocket

Backend

Python

FastAPI

Uvicorn

WebSockets

SQLite

AI / Voice

Google Gemini Live API

Real-time audio input/output

Input audio transcription

Output audio transcription

Project Structure

eryx-AI-assistant/
│
├── app/
│   ├── main.py
│   │
│   ├── services/
│   │   ├── database.py
│   │   ├── gemini_pipeline.py
│   │   ├── live_pipeline.py
│   │   ├── memory.py
│   │   ├── speech_pipeline.py
│   │   └── tts_pipeline.py
│   │
│   └── tools/
│       ├── notes_tool.py
│       ├── reminder_tool.py
│       └── weather_tool.py
│
├── static/
│   ├── index.html
│   └── pcm-processor.js
│
├── data/
│   └── eryx.db
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

The weather tool exists in the development codebase, but it is not
part of the final required feature scope.

Important Components

1. live_pipeline.py

This file creates the Gemini Live session and configures ERYX as a
real-time audio assistant.

It defines:

Live model

Audio response modality

System instructions

Input audio transcription

Output audio transcription

2. main.py

The FastAPI backend handles:

Serving the frontend

Health checks

Serving the PCM processor

WebSocket connections

Browser → Gemini audio streaming

Gemini → Browser audio streaming

User and ERYX transcripts

Turn lifecycle

3. pcm-processor.js

The browser microphone produces floating-point audio samples.

The AudioWorklet converts those samples into 16-bit PCM data and sends
the PCM chunks through the WebSocket.

This is important because the real-time Gemini audio pipeline expects
audio data in a compatible PCM format.

4. reminder_tool.py

The reminder tool can:

Create reminders

Store them in SQLite

Retrieve saved reminders

Example:

User: Remind me to study Python at 7 PM.

ERYX: Reminder created for studying Python at 7 PM.

5. notes_tool.py

The notes tool can:

Save notes

Store them in SQLite

Retrieve saved notes

Example:

User: Save a note saying I need to finish my ERYX project.

ERYX: Note saved successfully.

6. database.py

SQLite is used as the small persistent database for:

Notes

Reminders

This keeps the project simple while still providing real persistence.

Multi-Turn Conversation

A major part of the implementation was handling multiple voice turns in
the same Live session.

The lifecycle is:

Start ERYX
   ↓
Record user speech
   ↓
Send PCM chunks
   ↓
End current audio turn
   ↓
Receive ERYX response
   ↓
Start another turn
   ↓
Send new PCM chunks
   ↓
Receive next response

The implementation was tested with multiple questions in sequence rather
than treating the application as a one-shot voice interaction.

Interruption / Barge-In Handling

ERYX uses a turn-based audio lifecycle so that the microphone can be
stopped and a new interaction can begin without creating a completely
new application session.

The browser sends a stop/end signal when the current recording ends,
allowing the backend to close the current audio turn cleanly.

Wake-Word Detection

Wake-word detection was added as a stretch feature.

The purpose is to allow ERYX to react to a defined activation phrase
before processing a voice command.

This helps make the assistant behave more like a practical voice
assistant rather than a simple push-to-talk application.

Low-Latency Design

The project uses streaming rather than waiting for an entire recording
to finish.

The main latency-sensitive path is:

Microphone
→ AudioWorklet
→ PCM chunks
→ WebSocket
→ Gemini Live
→ Streaming audio
→ Browser playback

This avoids unnecessary file creation and batch processing during normal
interaction.

The project is designed toward the mentor's stretch target of
approximately 1.5 seconds round-trip latency. Exact latency can vary
depending on microphone processing, network conditions, model response
time, and browser performance.

Setup

1. Clone the project

git clone <your-github-repository-url>
cd eryx-AI-assistant

2. Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure the Gemini API key

Create a .env file:

GEMINI_API_KEY=your_api_key_here

Do not commit .env or the API key to GitHub.

5. Run the application

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000

Testing

Basic voice test:

Start ERYX.

Ask: "What is Python?"

Stop speaking / end the turn.

Wait for ERYX to finish responding.

Start the next turn.

Ask: "What is Java?"

Verify that ERYX responds again.

Tool tests:

Save a note saying I need to finish my ERYX project.

and:

Remind me to study Python at 7 PM.

The notes and reminders should be persisted in the SQLite database.

Error Handling and Debugging

During development, the project encountered several issues including:

Gemini API free-tier quota exhaustion

Incorrect async handling of the Gemini Live connection

PCM processor route issues

WebSocket disconnects

Multi-turn session lifecycle problems

Audio playback/recording lifecycle problems

These were resolved by:

Updating the API configuration/key when the quota was exhausted

Correctly treating client.aio.live.connect(...) as an asynchronous
context manager

Adding a FastAPI route for /pcm-processor.js

Separating browser-to-Gemini and Gemini-to-browser tasks

Explicitly managing audio turn start/end

Cleaning up microphone and AudioWorklet resources between turns

Evaluation Criteria

The project was developed with the following evaluation areas in mind.

1. End-to-End Functionality

The complete pipeline should run:

Audio In → LLM → Tool / Response → Audio Out

2. Thoughtful LLM Use

ERYX uses Gemini Live for conversational understanding and real-time
interaction instead of using an LLM as a simple disconnected API call.

3. Speech-Handling Quality

The system uses streaming PCM audio, transcription, streaming model
output, and turn management.

4. Code Quality & Structure

The application is separated into:

Services

Tools

Database logic

Frontend

Audio processing

This makes the project easier to understand and extend.

5. Documentation

This README documents:

Setup

Architecture

Features

Project structure

Testing

Design decisions

Known limitations

6. Creativity / Stretch Goals

The implementation goes beyond the basic requirements with:

Wake-word detection

Multi-turn conversation

Persistent SQLite storage

Real-time streaming audio

Low-latency architecture

Assumptions and Known Limitations

The project depends on access to the Gemini Live API.

API quota and network conditions can affect availability and
latency.

Microphone permissions are required in the browser.

Exact round-trip latency is environment dependent and should be
measured on the target machine if a precise benchmark is required.

Wake-word detection is intended as a lightweight activation
mechanism rather than a production-grade always-listening security
system.

The current tool scope intentionally focuses on reminders and notes.

AI Coding Assistance Disclosure

AI coding assistance was used during development.

I used AI assistance mainly for:

UI styling and frontend presentation ideas

Understanding some functions and APIs

Learning implementation patterns while developing the real-time
pipeline

Debugging and resolving development errors

Getting explanations for unfamiliar code

I did not simply copy the complete project without understanding it. I
worked through the implementation, tested the features, fixed errors,
and can explain the code and architecture used in the project.

The AI assistance was particularly useful for learning unfamiliar
concepts such as:

WebSocket communication

AudioWorklet processing

PCM audio conversion

Gemini Live session handling

Asynchronous Python code

Multi-turn voice-session lifecycle

Development Approach

The project was built incrementally:

Set up the FastAPI backend.

Added the Gemini API pipeline.

Added notes and reminder tools.

Added database persistence.

Built the browser voice interface.

Added PCM audio processing.

Connected browser audio to Gemini through WebSockets.

Added streaming ERYX audio responses.

Fixed multi-turn conversation handling.

Added interruption/turn lifecycle handling.

Added wake-word detection.

Optimized the streaming path for low latency.

Tested the complete end-to-end pipeline.

Future Improvements

Possible future improvements include:

More robust wake-word detection

Better noise suppression

Authentication and per-user data isolation

More tools

Production deployment

More detailed latency measurement

Improved UI animations and visual feedback

Persistent conversation history across sessions

Author

Kiran

Built as a Real-Time Voice Assistant project for the take-home
assessment.