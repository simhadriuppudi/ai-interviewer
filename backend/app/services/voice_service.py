from gtts import gTTS
import base64
import io
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class VoiceService:
    """Service for Text-to-Speech conversion"""
    
    def __init__(self):
        self.language = 'en'
        self.slow = False
    
    def text_to_speech_base64(self, text: str) -> str:
        """
        Convert text to speech and return as base64 encoded audio
        
        Args:
            text: Text to convert to speech
        
        Returns:
            Base64 encoded MP3 audio string
        """
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=self.language, slow=self.slow)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Encode to base64
            audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
            
            return audio_base64
            
        except Exception as e:
            logger.error(f"TTS conversion error: {e}")
            return ""
    
    def text_to_speech_file(self, text: str, output_path: str) -> bool:
        """
        Convert text to speech and save as MP3 file
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the audio file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            tts = gTTS(text=text, lang=self.language, slow=self.slow)
            tts.save(output_path)
            logger.info(f"TTS audio saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"TTS file save error: {e}")
            return False

# Global instance
voice_service = VoiceService()
