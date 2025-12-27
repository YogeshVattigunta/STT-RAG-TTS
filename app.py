# backend/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import voice_core

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/record/start")
def record_start():
    voice_core.start_recording()
    return {"ok": True}

@app.post("/record/stop")
def record_stop():
    voice_core.stop_recording_and_process()
    return {"ok": True}

@app.get("/status")
def status():
    return voice_core.get_state()
