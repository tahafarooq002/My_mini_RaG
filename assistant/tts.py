# tts.py
import gtts
from gtts import gTTS
import playsound
import tempfile
import os

def speak(text, lang="en"):
    """
    Convert text to speech safely without 'run loop already started' errors.
    Works in loops and async environments.
    
    :param text: String to speak
    :param lang: Language code (default: 'en')
    """
    try:
        # Use a temporary file to save audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_file = fp.name
        tts = gTTS(text=text, lang=lang)
        tts.save(temp_file)

        # Play the audio
        playsound.playsound(temp_file, True)
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
