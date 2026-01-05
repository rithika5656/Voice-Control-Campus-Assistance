"""
Voice-Controlled Campus Assistant
GUI Application using Tkinter

This provides a graphical interface for the campus voice assistant
with buttons for voice input and visual feedback.

Author: Campus Assistant Team
Version: 1.0.0
"""

import sys
import os
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.speech_recognition_module import SpeechRecognizer
from modules.text_to_speech_module import TextToSpeech
from modules.nlp_processor import IntentProcessor
from modules.response_generator import ResponseGenerator


class CampusAssistantGUI:
    """GUI Application for Campus Voice Assistant"""
    
    def __init__(self):
        """Initialize the GUI application"""
        self.root = tk.Tk()
        self.root.title("🎓 Campus Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        # Set minimum size
        self.root.minsize(700, 500)
        
        # Initialize components
        self.speech_recognizer = None
        self.tts = None
        self.nlp_processor = IntentProcessor()
        self.response_generator = ResponseGenerator()
        
        # Flags
        self.is_listening = False
        self.voice_output_enabled = tk.BooleanVar(value=True)
        
        # Create GUI elements
        self._create_styles()
        self._create_widgets()
        self._initialize_components()
        
        # Show welcome message
        self._show_welcome()
    
    def _create_styles(self):
        """Create custom styles for ttk widgets"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('Title.TLabel',
                           font=('Helvetica', 24, 'bold'),
                           foreground='#00d9ff',
                           background='#1a1a2e')
        
        self.style.configure('Subtitle.TLabel',
                           font=('Helvetica', 12),
                           foreground='#a0a0a0',
                           background='#1a1a2e')
        
        self.style.configure('Status.TLabel',
                           font=('Helvetica', 11),
                           foreground='#00ff88',
                           background='#1a1a2e')
        
        self.style.configure('Voice.TButton',
                           font=('Helvetica', 14, 'bold'),
                           padding=15)
        
        self.style.configure('Action.TButton',
                           font=('Helvetica', 10),
                           padding=8)
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#1a1a2e')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, 
                               text="🎓 Campus Voice Assistant",
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame,
                                  text="Your intelligent campus information guide",
                                  style='Subtitle.TLabel')
        subtitle_label.pack()
        
        # Chat display area
        chat_frame = tk.Frame(main_frame, bg='#16213e', relief=tk.RIDGE, bd=2)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg='#16213e',
            fg='#ffffff',
            insertbackground='white',
            state=tk.DISABLED,
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for formatting
        self.chat_display.tag_configure('user', foreground='#00d9ff', font=('Consolas', 11, 'bold'))
        self.chat_display.tag_configure('assistant', foreground='#00ff88', font=('Consolas', 11, 'bold'))
        self.chat_display.tag_configure('system', foreground='#ffcc00', font=('Consolas', 10, 'italic'))
        self.chat_display.tag_configure('error', foreground='#ff6b6b', font=('Consolas', 10))
        
        # Input area
        input_frame = tk.Frame(main_frame, bg='#1a1a2e')
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.input_entry = tk.Entry(
            input_frame,
            font=('Helvetica', 12),
            bg='#16213e',
            fg='white',
            insertbackground='white',
            relief=tk.FLAT,
            bd=10
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind('<Return>', self._on_text_submit)
        
        send_btn = ttk.Button(input_frame, text="Send 📤",
                             style='Action.TButton',
                             command=self._on_text_submit)
        send_btn.pack(side=tk.LEFT)
        
        # Button area
        button_frame = tk.Frame(main_frame, bg='#1a1a2e')
        button_frame.pack(fill=tk.X)
        
        # Voice input button
        self.voice_btn = tk.Button(
            button_frame,
            text="🎤 Press to Speak",
            font=('Helvetica', 14, 'bold'),
            bg='#0066cc',
            fg='white',
            activebackground='#0052a3',
            activeforeground='white',
            relief=tk.FLAT,
            padx=30,
            pady=15,
            cursor='hand2',
            command=self._on_voice_button
        )
        self.voice_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Voice output toggle
        voice_check = ttk.Checkbutton(
            button_frame,
            text="🔊 Voice Output",
            variable=self.voice_output_enabled,
            style='Action.TButton'
        )
        voice_check.pack(side=tk.LEFT, padx=10)
        
        # Help button
        help_btn = ttk.Button(button_frame, text="❓ Help",
                             style='Action.TButton',
                             command=self._show_help)
        help_btn.pack(side=tk.LEFT, padx=10)
        
        # Clear button
        clear_btn = ttk.Button(button_frame, text="🗑️ Clear",
                              style='Action.TButton',
                              command=self._clear_chat)
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(button_frame,
                                textvariable=self.status_var,
                                style='Status.TLabel')
        status_label.pack(side=tk.RIGHT)
    
    def _initialize_components(self):
        """Initialize speech components in background"""
        def init():
            try:
                self._update_status("Initializing speech recognition...")
                self.speech_recognizer = SpeechRecognizer()
                
                self._update_status("Initializing text-to-speech...")
                self.tts = TextToSpeech(rate=150, volume=0.9)
                
                self._update_status("Ready - Click 🎤 or type your question")
                self._add_message("system", "✅ All components initialized successfully!")
                
            except Exception as e:
                self._add_message("error", f"⚠️ Error initializing: {e}")
                self._update_status("Running in text-only mode")
        
        threading.Thread(target=init, daemon=True).start()
    
    def _show_welcome(self):
        """Display welcome message"""
        welcome = """
╔══════════════════════════════════════════════════════════════╗
║          🎓 CAMPUS VOICE ASSISTANT                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  I can help you with:                                        ║
║                                                              ║
║  📅 Class timetables and schedules                          ║
║  📝 Exam schedules and dates                                ║
║  🏛️ Department information                                   ║
║  🏫 Campus facilities (library, canteen, hostel)            ║
║  🎉 Upcoming events                                          ║
║  ❓ General FAQs                                             ║
║                                                              ║
║  Click the 🎤 button to speak or type your question below.  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        self._add_message("system", welcome)
    
    def _add_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        if sender == "user":
            self.chat_display.insert(tk.END, "\n👤 You: ", 'user')
            self.chat_display.insert(tk.END, f"{message}\n")
        elif sender == "assistant":
            self.chat_display.insert(tk.END, "\n🤖 Assistant:\n", 'assistant')
            self.chat_display.insert(tk.END, f"{message}\n")
        elif sender == "system":
            self.chat_display.insert(tk.END, f"{message}\n", 'system')
        elif sender == "error":
            self.chat_display.insert(tk.END, f"{message}\n", 'error')
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def _update_status(self, status):
        """Update the status bar"""
        self.status_var.set(status)
        self.root.update_idletasks()
    
    def _on_voice_button(self):
        """Handle voice button click"""
        if self.is_listening:
            return
        
        if not self.speech_recognizer:
            self._add_message("error", "⚠️ Speech recognition not available. Please type your question.")
            return
        
        # Start listening in a separate thread
        threading.Thread(target=self._listen_and_process, daemon=True).start()
    
    def _listen_and_process(self):
        """Listen for voice input and process"""
        self.is_listening = True
        self.voice_btn.config(text="🎤 Listening...", bg='#cc0000')
        self._update_status("🎤 Listening... Speak now!")
        
        try:
            # Get voice input
            text = self.speech_recognizer.get_text_from_speech()
            
            if text:
                self._add_message("user", text)
                self._process_and_respond(text)
            else:
                self._add_message("error", "❓ Couldn't understand. Please try again or type your question.")
        
        except Exception as e:
            self._add_message("error", f"⚠️ Error: {e}")
        
        finally:
            self.is_listening = False
            self.voice_btn.config(text="🎤 Press to Speak", bg='#0066cc')
            self._update_status("Ready")
    
    def _on_text_submit(self, event=None):
        """Handle text input submission"""
        text = self.input_entry.get().strip()
        if not text:
            return
        
        self.input_entry.delete(0, tk.END)
        self._add_message("user", text)
        
        # Process in background
        threading.Thread(target=self._process_and_respond, args=(text,), daemon=True).start()
    
    def _process_and_respond(self, query):
        """Process query and generate response"""
        self._update_status("Processing...")
        
        try:
            # Check for exit
            if any(word in query.lower() for word in ['exit', 'quit', 'bye']):
                response = "Goodbye! Have a great day! 👋"
                self._add_message("assistant", response)
                if self.voice_output_enabled.get() and self.tts:
                    self.tts.speak(response)
                self.root.after(2000, self.root.quit)
                return
            
            # Process query
            query_result = self.nlp_processor.process_query(query)
            response = self.response_generator.generate_response(query_result)
            
            self._add_message("assistant", response)
            
            # Speak response if enabled
            if self.voice_output_enabled.get() and self.tts:
                # Speak a shorter version for long responses
                speak_text = response[:500] if len(response) > 500 else response
                self.tts.speak(speak_text)
        
        except Exception as e:
            self._add_message("error", f"⚠️ Error processing query: {e}")
        
        finally:
            self._update_status("Ready")
    
    def _show_help(self):
        """Show help dialog"""
        help_text = self.response_generator.get_help_message()
        self._add_message("assistant", help_text)
    
    def _clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self._show_welcome()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = CampusAssistantGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")


if __name__ == "__main__":
    main()
