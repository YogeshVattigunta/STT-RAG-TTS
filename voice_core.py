# backend/voice_core.py

import threading
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import whisper
import faiss
import requests
import pyttsx3
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ----------------
SAMPLE_RATE = 16000
AUDIO_FILE = "input.wav"
OLLAMA_MODEL = "phi"

# ---------------- GLOBAL STATE ----------------
state = {
    "status": "idle",        # idle | listening | transcribing | thinking | speaking
    "you_said": "",
    "assistant": ""
}

recording = False
frames = []
stream = None
lock = threading.Lock()

# ---------------- LOAD MODELS ----------------
stt_model = whisper.load_model("base")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- RECORDING ----------------
def start_recording():
    global recording, frames, stream

    with lock:
        frames = []
        recording = True
        state["status"] = "listening"
        state["you_said"] = ""
        state["assistant"] = ""

    def callback(indata, frames_count, time_info, status):
        if recording:
            frames.append(indata.copy())

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=callback
    )
    stream.start()

# ---------------- SAFE OLLAMA CALL ----------------
def call_ollama(prompt: str) -> str:
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60  # ⬅️ CRITICAL
        )
        res.raise_for_status()
        return res.json().get("response", "").strip()
    except Exception as e:
        return f"Sorry, I ran into an LLM error: {e}"

# ---------------- BACKGROUND PIPELINE ----------------
def stop_recording_and_process():
    def background_job():
        global recording, stream

        # Stop recording safely
        with lock:
            recording = False
            state["status"] = "transcribing"

        try:
            stream.stop()
            stream.close()
        except Exception:
            pass

        if not frames:
            state["assistant"] = "No audio was recorded."
            state["status"] = "idle"
            return

        audio = np.concatenate(frames, axis=0)
        write(AUDIO_FILE, SAMPLE_RATE, audio)

        # ---------- STT ----------
        try:
            text = stt_model.transcribe(AUDIO_FILE)["text"].strip()
        except Exception as e:
            state["assistant"] = f"Speech recognition failed: {e}"
            state["status"] = "idle"
            return

        state["you_said"] = text
        state["status"] = "thinking"

        # ---------- RAG ----------
        try:
            with open("docs.txt", "r", encoding="utf-8") as f:
                docs = f.readlines()

            embeddings = embedder.encode(docs)
            index = faiss.IndexFlatL2(embeddings.shape[1])
            index.add(np.array(embeddings))

            q_emb = embedder.encode([text])
            _, idx = index.search(q_emb, 2)
            context = "\n".join([docs[i] for i in idx[0]])
        except Exception:
            context = ""

        # ---------- LLM ----------
        prompt = f"""
Context:
{context}

Question:
{text}

Answer clearly:
"""
        reply = call_ollama(prompt)

        if not reply:
            reply = "Sorry, I couldn't generate a response."

        state["assistant"] = reply
        state["status"] = "speaking"

        # ---------- TTS ----------
        try:
            engine = pyttsx3.init()
            engine.say(reply)
            engine.runAndWait()
            engine.stop()
        except Exception:
            pass

        state["status"] = "idle"

    threading.Thread(target=background_job, daemon=True).start()

# ---------------- STATUS ----------------
def get_state():
    return state
