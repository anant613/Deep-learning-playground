import speech_recognition as sr
import threading
import time
from config.settings import settings

class VoiceListener:
    def __init__(self, speaker, ai_handler):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.speaker = speaker
        self.ai_handler = ai_handler
        self.listening = False
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def start_listening(self):
        """Start continuous listening for wake word and commands"""
        self.listening = True
        print(f"🎤 Listening for wake word: '{settings.WAKE_WORD}'")
        
        while self.listening:
            try:
                # Listen for wake word
                if self.listen_for_wake_word():
                    # Wake word detected, listen for command
                    command = self.listen_for_command()
                    if command:
                        # Process command with AI
                        response = self.ai_handler.process_command(command)
                        self.speaker.speak(response)
                        
            except Exception as e:
                print(f"❌ Listening error: {e}")
                time.sleep(1)
    
    def listen_for_wake_word(self):
        """Listen for the wake word"""
        try:
            with self.microphone as source:
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio).lower()
            
            if settings.WAKE_WORD.lower() in text:
                print(f"🔊 Wake word detected: {text}")
                self.speaker.speak("Yes, how can I help you?")
                return True
                
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except Exception as e:
            print(f"❌ Wake word detection error: {e}")
        
        return False
    
    def listen_for_command(self):
        """Listen for user command after wake word"""
        try:
            print("🎤 Listening for command...")
            
            with self.microphone as source:
                # Listen for command with longer timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize command
            command = self.recognizer.recognize_google(audio)
            print(f"🗣️ Command received: {command}")
            return command
            
        except sr.WaitTimeoutError:
            self.speaker.speak("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            self.speaker.speak("Sorry, I didn't understand that. Could you repeat?")
        except Exception as e:
            print(f"❌ Command recognition error: {e}")
            self.speaker.speak("Sorry, there was an error processing your command.")
        
        return None
    
    def stop_listening(self):
        """Stop the voice listener"""
        self.listening = False
        print("🔇 Voice listening stopped")