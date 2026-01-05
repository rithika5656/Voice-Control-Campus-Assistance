"""
Text-to-Speech Module
Handles conversion of text responses to speech output
"""

import pyttsx3


class TextToSpeech:
    """Handles text-to-speech conversion using pyttsx3 (offline)"""
    
    def __init__(self, rate=150, volume=1.0, voice_index=0):
        """
        Initialize the TTS engine
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
            voice_index: Index of voice to use (0 = default)
        """
        self.engine = pyttsx3.init()
        
        # Set speech rate
        self.engine.setProperty('rate', rate)
        
        # Set volume
        self.engine.setProperty('volume', volume)
        
        # Get available voices and set the preferred one
        self.voices = self.engine.getProperty('voices')
        if voice_index < len(self.voices):
            self.engine.setProperty('voice', self.voices[voice_index].id)
        
        print("🔊 Text-to-Speech engine initialized!")
    
    def get_available_voices(self):
        """
        Get list of available voices
        
        Returns:
            List of voice objects with id and name
        """
        voices_info = []
        for idx, voice in enumerate(self.voices):
            voices_info.append({
                'index': idx,
                'id': voice.id,
                'name': voice.name,
                'languages': voice.languages,
                'gender': voice.gender
            })
        return voices_info
    
    def set_voice(self, voice_index):
        """
        Set the voice by index
        
        Args:
            voice_index: Index of the voice to use
        """
        if 0 <= voice_index < len(self.voices):
            self.engine.setProperty('voice', self.voices[voice_index].id)
            print(f"✅ Voice set to: {self.voices[voice_index].name}")
        else:
            print(f"❌ Invalid voice index. Available: 0-{len(self.voices)-1}")
    
    def set_rate(self, rate):
        """
        Set the speech rate
        
        Args:
            rate: Words per minute (100-200 recommended)
        """
        self.engine.setProperty('rate', rate)
        print(f"✅ Speech rate set to: {rate}")
    
    def set_volume(self, volume):
        """
        Set the volume level
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if 0.0 <= volume <= 1.0:
            self.engine.setProperty('volume', volume)
            print(f"✅ Volume set to: {volume}")
        else:
            print("❌ Volume must be between 0.0 and 1.0")
    
    def speak(self, text):
        """
        Convert text to speech and play it
        
        Args:
            text: Text string to speak
        """
        if text:
            print(f"🔊 Speaking: \"{text[:50]}...\"" if len(text) > 50 else f"🔊 Speaking: \"{text}\"")
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            print("⚠️ No text to speak")
    
    def speak_with_pause(self, text, pause_duration=0.5):
        """
        Speak text with a pause after sentences
        
        Args:
            text: Text string to speak
            pause_duration: Duration of pause in seconds (approximate)
        """
        if text:
            sentences = text.replace('!', '.').replace('?', '.').split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence:
                    self.engine.say(sentence)
                    self.engine.runAndWait()
    
    def save_to_file(self, text, filename):
        """
        Save speech to an audio file
        
        Args:
            text: Text string to convert
            filename: Output filename (mp3/wav)
        """
        try:
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            print(f"✅ Audio saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving audio: {e}")


# Test the module
if __name__ == "__main__":
    print("=" * 50)
    print("  Text-to-Speech Module Test")
    print("=" * 50)
    
    tts = TextToSpeech()
    
    # Show available voices
    print("\n📋 Available voices:")
    for voice in tts.get_available_voices():
        print(f"  [{voice['index']}] {voice['name']}")
    
    # Test speech
    print("\n🎤 Testing speech output...")
    tts.speak("Hello! I am your Campus Voice Assistant. How can I help you today?")
    
    print("\n✅ Text-to-Speech module test complete!")
