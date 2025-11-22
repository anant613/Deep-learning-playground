import pyttsx3
import threading
from config.settings import settings

class VoiceSpeaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.speaking_lock = threading.Lock()
    
    def setup_voice(self):
        """Configure voice settings"""
        # Set speech rate
        self.engine.setProperty('rate', settings.VOICE_RATE)
        
        # Set volume
        self.engine.setProperty('volume', settings.VOICE_VOLUME)
        
        # Get available voices
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to use a female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            else:
                # Use first available voice
                self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text):
        """Convert text to speech"""
        if not text:
            return
            
        with self.speaking_lock:
            try:
                print(f"🗣️ Jarvis: {text}")
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"❌ Speech error: {e}")
    
    def speak_async(self, text):
        """Speak text asynchronously"""
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """Stop the speech engine"""
        try:
            self.engine.stop()
        except Exception as e:
            print(f"❌ Error stopping speech engine: {e}")