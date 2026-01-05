"""
Speech Recognition Module
Handles voice input capture and conversion to text
Uses sounddevice as alternative to PyAudio for Python 3.14 compatibility
"""

import speech_recognition as sr
import numpy as np
import sounddevice as sd
import wave
import tempfile
import os


class SpeechRecognizer:
    """Handles speech-to-text conversion using various recognition engines"""
    
    def __init__(self, sample_rate=16000):
        self.recognizer = sr.Recognizer()
        self.sample_rate = sample_rate
        self.channels = 1
        self.microphone_available = False
        
        # Test if microphone is available
        try:
            devices = sd.query_devices()
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            if input_devices:
                self.microphone_available = True
                print("🎤 Microphone detected and ready!")
                print(f"   Using: {sd.query_devices(kind='input')['name']}")
            else:
                print("⚠️ No microphone found. Please use text input.")
        except Exception as e:
            print(f"⚠️ Audio device error: {e}")
            print("📝 Please use text input mode.")
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen to microphone and capture audio using sounddevice
        
        Args:
            timeout: Maximum time to wait for speech to start
            phrase_time_limit: Maximum time for the phrase
            
        Returns:
            AudioData object or None if failed
        """
        if not self.microphone_available:
            print("⚠️ Microphone not available. Please use text input.")
            return None
            
        try:
            print("\n🎤 Listening... Speak now!")
            
            # Record audio using sounddevice
            duration = phrase_time_limit
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=np.int16
            )
            sd.wait()  # Wait until recording is finished
            
            # Save to temporary WAV file
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_filename = temp_file.name
            temp_file.close()
            
            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(self.sample_rate)
                wf.writeframes(recording.tobytes())
            
            # Load the audio file for recognition
            with sr.AudioFile(temp_filename) as source:
                audio = self.recognizer.record(source)
            
            # Clean up temp file
            os.unlink(temp_filename)
            
            return audio
            
        except Exception as e:
            print(f"❌ Error capturing audio: {e}")
            return None
    
    def recognize_google(self, audio, language="en-IN"):
        """
        Convert audio to text using Google Speech Recognition API
        
        Args:
            audio: AudioData object from listen()
            language: Language code (default: en-IN for Indian English)
            
        Returns:
            Recognized text string or None if failed
        """
        if audio is None:
            return None
            
        try:
            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio, language=language)
            print(f"📝 You said: \"{text}\"")
            return text
        except sr.UnknownValueError:
            print("❓ Sorry, I couldn't understand that. Please speak clearly.")
            return None
        except sr.RequestError as e:
            print(f"❌ Could not request results from Google Speech Recognition service: {e}")
            return None
    
    def recognize_sphinx(self, audio):
        """
        Convert audio to text using offline Sphinx recognizer
        (Requires pocketsphinx to be installed)
        
        Args:
            audio: AudioData object from listen()
            
        Returns:
            Recognized text string or None if failed
        """
        if audio is None:
            return None
            
        try:
            print("🔄 Processing speech (offline mode)...")
            text = self.recognizer.recognize_sphinx(audio)
            print(f"📝 You said: \"{text}\"")
            return text
        except sr.UnknownValueError:
            print("❓ Sorry, I couldn't understand that. Please speak clearly.")
            return None
        except sr.RequestError as e:
            print(f"❌ Sphinx error: {e}")
            return None
    
    def get_text_from_speech(self, use_google=True, language="en-IN"):
        """
        Main method to capture and convert speech to text
        
        Args:
            use_google: If True, use Google API; else use offline Sphinx
            language: Language code for recognition
            
        Returns:
            Recognized text string or None if failed
        """
        audio = self.listen()
        
        if audio is None:
            return None
        
        if use_google:
            return self.recognize_google(audio, language)
        else:
            return self.recognize_sphinx(audio)


# Test the module
if __name__ == "__main__":
    print("=" * 50)
    print("  Speech Recognition Module Test")
    print("=" * 50)
    
    recognizer = SpeechRecognizer()
    
    print("\nSay something to test the speech recognition...")
    text = recognizer.get_text_from_speech()
    
    if text:
        print(f"\n✅ Successfully recognized: {text}")
    else:
        print("\n❌ Failed to recognize speech")
