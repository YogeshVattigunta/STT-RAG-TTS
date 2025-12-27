# Local Voice Agent with 3D Avatar (Offline-Capable)

A fully local **voice-based AI assistant** featuring real-time speech interaction, retrieval-augmented generation (RAG), text-to-speech (TTS), and an animated 3D avatar UI.

Built to be **offline-first**, **demo-ready**, and **interview-ready**.

---

## Features

-  **Speech-to-Text (STT)**  
  Converts live microphone input into text.

- **Retrieval-Augmented Generation (RAG)**  
  Answers are grounded in your own knowledge base (`docs.txt`).

-  **Local LLM**  
  Uses a locally running language model (via Ollama or equivalent).

-  **Text-to-Speech (TTS)**  
  Speaks responses aloud using a local TTS engine.

-  **Animated 3D Avatar**  
  GLB model with embedded animation (Idle Animation).

- 🎞 **State-Synced Animation**  
  Avatar animation speed reflects system state:
  - Listening
  - Thinking
  - Speaking

-  **Modern UI**
  - Space-themed background
  - Two-panel layout (controls on left, avatar on right)
  - Clean, readable conversation panel

-  **Offline Ready**
  - Works without internet after models are downloaded.

---

##  High-Level Architecture

User Voice
↓
Speech-to-Text (STT)
↓
User Query
↓
RAG (FAISS + Sentence Embeddings)
↓
Local LLM
↓
Response Text
↓
Text-to-Speech (TTS)
↓
Audio Output


The frontend **polls backend status** to:
- update UI text
- trigger avatar animation changes
- reflect current system state

---

##  Folder Structure

project-root/
│
├── backend/
│   ├── app.py                # FastAPI backend server
│   ├── voice_core.py         # Voice pipeline (STT → RAG → LLM → TTS)
│   ├── docs.txt              # Knowledge base for RAG
│   ├── requirements.txt      # Python dependencies
│   └── audio/
│       ├── input.wav         # Recorded user audio
│       └── output.wav        # Generated speech audio
│
├── frontend/
│   ├── index.html            # Main UI layout
│   ├── style.css             # Styling + space background
│   ├── app.js                # UI logic + backend polling
│   ├── robot.glb             # Animated 3D avatar (GLB)
│   └── space_bg.png          # Space background image
│
└── README.md                 # Project documentation


---

##  Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** – API server
- **Whisper / faster-whisper** – Speech-to-text
- **FAISS** – Vector search for RAG
- **Sentence-Transformers** – Text embeddings
- **Local LLM** (e.g., via Ollama)
- **TTS Engine** – Local text-to-speech

### Frontend
- **HTML / CSS / JavaScript**
- **`<model-viewer>`** – 3D avatar rendering
- **GLB model** with embedded animation
- **Polling-based UI updates**

---

##  Knowledge Base (RAG)

The file `backend/docs.txt` acts as the assistant’s **knowledge source**.

Example:
```txt
The user's name is Yogesh.
Yogesh prefers simple explanations.
Transformers use self-attention to process sequences.
RAG improves accuracy by retrieving relevant context.

 How to Run
1️) Start the Local LLM

Make sure your local LLM server is running (example using Ollama):

ollama list


(Optional test)

ollama run phi

2️) Start Backend
cd backend
uvicorn app:app --port 8000


Verify:

http://localhost:8000/status

3️) Start Frontend
cd frontend
python -m http.server 5500


Open in browser:

http://localhost:5500

How to Use

Click 🎤 Start Speaking

Speak clearly into the microphone

Click ⏹ Stop

Observe:

Status transitions (listening → thinking → speaking)

Text appears in the conversation panel

Avatar animation reacts

Voice response is spoken

System States
State	Description
idle	Waiting for user input
listening	Recording microphone input
thinking	Processing STT + RAG + LLM
speaking	Playing TTS response

Avatar animation speed changes based on these states.

 UI Design Notes

Left panel: interaction & conversation

Right panel: animated avatar

Background: 2D space image (visual mood)

Lighting: neutral 3D environment for realism

Glassmorphism: subtle blur for readability

 Interview-Ready Explanation

“This project implements a fully local voice agent using a modular pipeline for STT, RAG, LLM, and TTS. The frontend remains responsive by polling backend state, while the 3D avatar reacts visually to system states for better user feedback.”

 Possible Enhancements

Faster STT with GPU or quantized models

Lip-sync or mouth animation

Streaming LLM responses

Waveform visualization during speech

Mobile-responsive layout

Desktop packaging (Electron)

 License

This project is for educational, demo, and research purposes.
You are free to extend or adapt it as needed.




