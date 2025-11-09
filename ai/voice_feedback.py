"""
Voice Feedback System using Text-to-Speech
Converts text coaching feedback to audio
"""

import os
import logging
import threading
import queue
from pathlib import Path

logger = logging.getLogger(__name__)

# Try multiple TTS engines for cross-platform compatibility
TTS_ENGINE = None

try:
    import pyttsx3
    TTS_ENGINE = "pyttsx3"
    logger.info("Using pyttsx3 for offline TTS")
except ImportError:
    logger.warning("pyttsx3 not available")

if not TTS_ENGINE:
    try:
        from gtts import gTTS
        import pygame
        pygame.mixer.init()
        TTS_ENGINE = "gtts"
        logger.info("Using gTTS + pygame for TTS")
    except ImportError:
        logger.warning("gTTS/pygame not available")

class VoiceFeedbackSystem:
    def __init__(self, use_async=True):
        """
        Initialize voice feedback system
        
        Args:
            use_async: If True, speaks in background thread (non-blocking)
        """
        self.use_async = use_async
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.temp_dir = Path("temp_audio")
        self.temp_dir.mkdir(exist_ok=True)
        
        if not TTS_ENGINE:
            logger.error("No TTS engine available. Install pyttsx3 or gtts+pygame")
            raise RuntimeError("No TTS engine available")
        
        # Initialize TTS engine
        if TTS_ENGINE == "pyttsx3":
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 165)  # Speed
            self.engine.setProperty('volume', 0.9)  # Volume
            
            # Try to set a clear voice
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        
        # Start async speech worker if enabled
        if self.use_async:
            self.worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
            self.worker_thread.start()
            logger.info("Started async voice feedback worker")
    
    def speak(self, text, priority=False):
        """
        Speak text aloud
        
        Args:
            text: Text to speak
            priority: If True, clear queue and speak immediately
        """
        if not text or text.strip() == "":
            return
        
        # Clean text for better speech
        text = self._clean_text(text)
        
        if self.use_async:
            if priority:
                # Clear queue for priority messages
                while not self.speech_queue.empty():
                    try:
                        self.speech_queue.get_nowait()
                    except queue.Empty:
                        break
            
            self.speech_queue.put(text)
        else:
            self._do_speak(text)
    
    def _speech_worker(self):
        """Background worker for async speech"""
        while True:
            try:
                text = self.speech_queue.get()
                if text is None:  # Shutdown signal
                    break
                self._do_speak(text)
                self.speech_queue.task_done()
            except Exception as e:
                logger.error(f"Error in speech worker: {e}")
    
    def _do_speak(self, text):
        """Actually perform TTS"""
        try:
            self.is_speaking = True
            
            if TTS_ENGINE == "pyttsx3":
                self.engine.say(text)
                self.engine.runAndWait()
            
            elif TTS_ENGINE == "gtts":
                # Generate audio file
                import hashlib
                import time
                
                # Create unique filename
                text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
                audio_file = self.temp_dir / f"tts_{text_hash}_{int(time.time())}.mp3"
                
                # Generate speech
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(str(audio_file))
                
                # Play audio
                pygame.mixer.music.load(str(audio_file))
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                # Clean up
                try:
                    audio_file.unlink()
                except:
                    pass
            
            logger.info(f"Spoke: {text[:50]}...")
            
        except Exception as e:
            logger.error(f"Error speaking text: {e}")
        finally:
            self.is_speaking = False
    
    def _clean_text(self, text):
        """Clean text for better TTS output"""
        # Remove markdown
        text = text.replace('**', '')
        text = text.replace('*', '')
        text = text.replace('_', '')
        
        # Remove special characters that sound weird
        text = text.replace('⚠️', 'Warning:')
        text = text.replace('✅', '')
        text = text.replace('❌', '')
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def is_busy(self):
        """Check if currently speaking"""
        return self.is_speaking
    
    def clear_queue(self):
        """Clear pending speech"""
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
            except queue.Empty:
                break
    
    def shutdown(self):
        """Clean shutdown"""
        if self.use_async:
            self.speech_queue.put(None)  # Signal shutdown
            self.worker_thread.join(timeout=2)
        
        # Clean up temp files
        try:
            for file in self.temp_dir.glob("tts_*.mp3"):
                file.unlink()
        except:
            pass
    
    def test(self):
        """Test voice feedback"""
        self.speak("Voice feedback system initialized. Ready for training!", priority=True)

# Global instance (lazy initialization)
_voice_system = None

def get_voice_system():
    """Get or create global voice feedback system"""
    global _voice_system
    if _voice_system is None:
        try:
            _voice_system = VoiceFeedbackSystem(use_async=True)
        except RuntimeError as e:
            logger.error(f"Failed to initialize voice system: {e}")
            return None
    return _voice_system

def speak_feedback(text, priority=False):
    """Convenience function to speak feedback"""
    voice_system = get_voice_system()
    if voice_system:
        voice_system.speak(text, priority=priority)

