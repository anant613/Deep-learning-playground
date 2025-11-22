import asyncio
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config.settings import settings
from voice.listener import VoiceListener
from voice.speaker import VoiceSpeaker
from brain.ai_handler import AIHandler
from web.api import router

app = FastAPI(title="Jarvis AI Assistant", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Global components
voice_listener = None
voice_speaker = None
ai_handler = None

@app.on_event("startup")
async def startup_event():
    global voice_listener, voice_speaker, ai_handler
    
    # Initialize components
    voice_speaker = VoiceSpeaker()
    ai_handler = AIHandler()
    voice_listener = VoiceListener(voice_speaker, ai_handler)
    
    # Start voice listening in background thread
    voice_thread = threading.Thread(target=voice_listener.start_listening, daemon=True)
    voice_thread.start()
    
    print("🤖 Jarvis is now online!")
    voice_speaker.speak("Jarvis is now online and ready to assist you.")

@app.get("/")
async def root():
    return {"message": "Jarvis AI Assistant is running", "status": "online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "components": {
        "voice": voice_listener is not None,
        "ai": ai_handler is not None,
        "speaker": voice_speaker is not None
    }}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )