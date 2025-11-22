from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncio

router = APIRouter()

# Request/Response models
class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    response: str
    success: bool

class StatusResponse(BaseModel):
    status: str
    components: dict

# Global references (will be set from main.py)
voice_speaker = None
ai_handler = None

@router.post("/command", response_model=CommandResponse)
async def process_command(request: CommandRequest):
    """Process a text command through the AI handler"""
    try:
        if not ai_handler:
            raise HTTPException(status_code=503, detail="AI handler not initialized")
        
        # Process command
        response = ai_handler.process_command(request.command)
        
        # Speak response if voice is available
        if voice_speaker:
            voice_speaker.speak_async(response)
        
        return CommandResponse(response=response, success=True)
        
    except Exception as e:
        return CommandResponse(response=f"Error processing command: {str(e)}", success=False)

@router.post("/speak")
async def speak_text(request: dict):
    """Make Jarvis speak the provided text"""
    try:
        text = request.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        if not voice_speaker:
            raise HTTPException(status_code=503, detail="Voice speaker not initialized")
        
        voice_speaker.speak_async(text)
        return {"success": True, "message": "Text spoken successfully"}
        
    except Exception as e:
        return {"success": False, "message": f"Error speaking text: {str(e)}"}

@router.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status"""
    return StatusResponse(
        status="online",
        components={
            "voice_speaker": voice_speaker is not None,
            "ai_handler": ai_handler is not None,
            "voice_listener": True  # Assume running if API is responding
        }
    )

@router.get("/weather/{city}")
async def get_weather(city: str):
    """Get weather for a specific city"""
    try:
        if not ai_handler:
            raise HTTPException(status_code=503, detail="AI handler not initialized")
        
        response = ai_handler.weather_service.get_weather(city)
        return {"weather": response, "city": city}
        
    except Exception as e:
        return {"error": f"Error getting weather: {str(e)}"}

@router.get("/news")
async def get_news():
    """Get latest news headlines"""
    try:
        if not ai_handler:
            raise HTTPException(status_code=503, detail="AI handler not initialized")
        
        response = ai_handler.news_service.get_latest_news()
        return {"news": response}
        
    except Exception as e:
        return {"error": f"Error getting news: {str(e)}"}

@router.get("/search/{query}")
async def web_search(query: str):
    """Perform web search"""
    try:
        if not ai_handler:
            raise HTTPException(status_code=503, detail="AI handler not initialized")
        
        response = ai_handler.web_search.search(query)
        return {"results": response, "query": query}
        
    except Exception as e:
        return {"error": f"Error performing search: {str(e)}"}