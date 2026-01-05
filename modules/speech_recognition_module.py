"""
Speech Recognition Module
Handles voice input capture and conversion to text
"""

import speech_recognition as sr


class SpeechRecognizer:
    """Handles speech-to-text conversion using various recognition engines"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise on initialization
        with self.microphone as source:
            print("🎤 Calibrating microphone for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone calibrated!")
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen to microphone and capture audio
        
        Args:
            timeout: Maximum time to wait for speech to start
            phrase_time_limit: Maximum time for the phrase
            
        Returns:
            AudioData object or None if failed
        """
        try:
            with self.microphone as source:
                print("\n🎤 Listening... Speak now!")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                return audio
        except sr.WaitTimeoutError:
            print("⏰ No speech detected. Please try again.")
            return None
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
