"""
Voice-Controlled Campus Assistant
Main Application - Console Version

This application provides voice-controlled access to campus information
including timetables, exam schedules, department info, and facilities.

Author: Campus Assistant Team
Version: 1.0.0
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.speech_recognition_module import SpeechRecognizer
from modules.text_to_speech_module import TextToSpeech
from modules.nlp_processor import IntentProcessor
from modules.response_generator import ResponseGenerator


class CampusVoiceAssistant:
    """Main class for the Voice-Controlled Campus Assistant"""
    
    def __init__(self, use_voice_input=True, use_voice_output=True):
        """
        Initialize the campus assistant
        
        Args:
            use_voice_input: If True, use microphone; else use text input
            use_voice_output: If True, speak responses; else just print
        """
        print("\n" + "=" * 60)
        print("  🎓 VOICE-CONTROLLED CAMPUS ASSISTANT")
        print("=" * 60)
        print("\n⏳ Initializing components...\n")
        
        self.use_voice_input = use_voice_input
        self.use_voice_output = use_voice_output
        
        # Initialize components
        try:
            if use_voice_input:
                self.speech_recognizer = SpeechRecognizer()
            else:
                self.speech_recognizer = None
                print("🎤 Voice input disabled - using text input mode")
            
            if use_voice_output:
                self.tts = TextToSpeech(rate=150, volume=0.9)
            else:
                self.tts = None
                print("🔊 Voice output disabled - using text output mode")
            
            self.nlp_processor = IntentProcessor()
            self.response_generator = ResponseGenerator()
            
            print("\n✅ All components initialized successfully!")
            
        except Exception as e:
            print(f"\n❌ Error initializing components: {e}")
            print("Please check if all required libraries are installed.")
            print("Run: pip install -r requirements.txt")
            sys.exit(1)
    
    def speak(self, text):
        """Output text as speech or print to console"""
        print(f"\n🤖 Assistant: {text}")
        if self.use_voice_output and self.tts:
            self.tts.speak(text)
    
    def listen(self):
        """Get input from user (voice or text)"""
        if self.use_voice_input and self.speech_recognizer:
            return self.speech_recognizer.get_text_from_speech()
        else:
            try:
                return input("\n👤 You: ").strip()
            except EOFError:
                return "quit"
    
    def process_query(self, query):
        """
        Process user query and generate response
        
        Args:
            query: User's query string
            
        Returns:
            Response string
        """
        if not query:
            return "I didn't catch that. Could you please repeat?"
        
        # Process query through NLP
        query_result = self.nlp_processor.process_query(query)
        
        # Generate response
        response = self.response_generator.generate_response(query_result)
        
        return response
    
    def is_exit_command(self, query):
        """Check if user wants to exit"""
        if not query:
            return False
        exit_words = ['exit', 'quit', 'bye', 'goodbye', 'stop', 'end']
        return any(word in query.lower() for word in exit_words)
    
    def show_welcome_message(self):
        """Display welcome message"""
        welcome = """
🎓 Welcome to the Voice-Controlled Campus Assistant!

I can help you with:
  📅 Class timetables and schedules
  📝 Exam schedules and dates
  🏛️ Department information
  🏫 Campus facilities (library, canteen, hostel, etc.)
  🎉 Upcoming events
  ❓ General FAQs

Say 'help' for more options or 'quit' to exit.
        """
        print(welcome)
        if self.use_voice_output:
            self.speak("Welcome to the Voice-Controlled Campus Assistant! How can I help you today?")
    
    def run(self):
        """Main loop to run the assistant"""
        self.show_welcome_message()
        
        while True:
            try:
                # Get user input
                query = self.listen()
                
                if query is None:
                    continue
                
                # Check for exit
                if self.is_exit_command(query):
                    self.speak("Goodbye! Have a great day!")
                    break
                
                # Check for help
                if query.lower() in ['help', 'commands', 'what can you do']:
                    print(self.response_generator.get_help_message())
                    continue
                
                # Process and respond
                response = self.process_query(query)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                self.speak("Sorry, something went wrong. Please try again.")
        
        print("\n" + "=" * 60)
        print("  Thank you for using Campus Voice Assistant!")
        print("=" * 60 + "\n")


def main():
    """Main entry point"""
    print("\n🎓 Campus Voice Assistant - Starting...")
    
    # Check for command line arguments
    use_voice_input = True
    use_voice_output = True
    
    if len(sys.argv) > 1:
        if '--text-only' in sys.argv:
            use_voice_input = False
            use_voice_output = False
        if '--no-voice-input' in sys.argv:
            use_voice_input = False
        if '--no-voice-output' in sys.argv:
            use_voice_output = False
    
    # Create and run assistant
    assistant = CampusVoiceAssistant(
        use_voice_input=use_voice_input,
        use_voice_output=use_voice_output
    )
    assistant.run()


if __name__ == "__main__":
    main()
