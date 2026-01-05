"""
Voice-Controlled Campus Assistant
🌟 Premium Modern GUI Application 🌟

Author: Campus Assistant Team
Version: 3.0.0
"""

import sys
import os
import threading
import queue
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.speech_recognition_module import SpeechRecognizer
from modules.text_to_speech_module import TextToSpeech
from modules.nlp_processor import IntentProcessor
from modules.response_generator import ResponseGenerator


class TTSManager:
    """Thread-safe TTS manager to prevent run loop errors"""
    def __init__(self):
        self.queue = queue.Queue()
        self.tts = None
        self.running = True
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()
    
    def _worker(self):
        """Worker thread for TTS"""
        import pyttsx3
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        self.tts.setProperty('volume', 0.9)
        
        while self.running:
            try:
                text = self.queue.get(timeout=0.5)
                if text:
                    self.tts.say(text)
                    self.tts.runAndWait()
            except queue.Empty:
                continue
            except Exception:
                pass
    
    def speak(self, text):
        """Add text to speak queue"""
        if text:
            self.queue.put(text)
    
    def stop(self):
        self.running = False


class AnimatedGradientCanvas(tk.Canvas):
    """Animated gradient background"""
    def __init__(self, parent, colors, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.colors = colors
        self.offset = 0
        self.bind("<Configure>", self._draw_gradient)
    
    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        for i in range(height):
            ratio = i / height
            r = int(self.colors[0][0] + (self.colors[1][0] - self.colors[0][0]) * ratio)
            g = int(self.colors[0][1] + (self.colors[1][1] - self.colors[0][1]) * ratio)
            b = int(self.colors[0][2] + (self.colors[1][2] - self.colors[0][2]) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.create_line(0, i, width, i, fill=color, tags="gradient")


class PulsingButton(tk.Canvas):
    """Animated pulsing microphone button"""
    def __init__(self, parent, command, size=120, **kwargs):
        super().__init__(parent, width=size+40, height=size+40, 
                        highlightthickness=0, bg=parent["bg"], **kwargs)
        self.command = command
        self.size = size
        self.pulse_size = 0
        self.is_listening = False
        self.base_color = "#6366f1"
        self.listening_color = "#ef4444"
        self.current_color = self.base_color
        
        self._draw()
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self._animate()
    
    def _draw(self):
        self.delete("all")
        cx, cy = (self.size + 40) // 2, (self.size + 40) // 2
        
        # Outer glow/pulse
        if self.is_listening:
            for i in range(3):
                alpha = 0.3 - (i * 0.1)
                pulse_r = self.size // 2 + 10 + self.pulse_size + (i * 8)
                glow_color = "#fca5a5" if self.is_listening else "#a5b4fc"
                self.create_oval(cx - pulse_r, cy - pulse_r, cx + pulse_r, cy + pulse_r,
                               fill="", outline=glow_color, width=2, tags="pulse")
        
        # Shadow
        self.create_oval(cx - self.size//2 + 4, cy - self.size//2 + 4,
                        cx + self.size//2 + 4, cy + self.size//2 + 4,
                        fill="#1e1b4b", outline="")
        
        # Main button
        self.create_oval(cx - self.size//2, cy - self.size//2,
                        cx + self.size//2, cy + self.size//2,
                        fill=self.current_color, outline="")
        
        # Inner highlight
        self.create_oval(cx - self.size//2 + 8, cy - self.size//2 + 8,
                        cx + self.size//2 - 8, cy + self.size//2 - 8,
                        fill="", outline="#ffffff", width=2)
        
        # Microphone icon
        icon = "🎤" if not self.is_listening else "🔴"
        self.create_text(cx, cy, text=icon, font=("Segoe UI Emoji", 36),
                        fill="white", tags="icon")
        
        # Status text
        status = "TAP TO SPEAK" if not self.is_listening else "LISTENING..."
        self.create_text(cx, cy + self.size//2 + 25, text=status,
                        font=("Segoe UI", 10, "bold"), fill="#94a3b8")
    
    def _animate(self):
        if self.is_listening:
            self.pulse_size = (self.pulse_size + 2) % 20
            self._draw()
        self.after(50, self._animate)
    
    def _on_click(self, event):
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        self.config(cursor="hand2")
    
    def _on_leave(self, event):
        self.config(cursor="")
    
    def set_listening(self, listening):
        self.is_listening = listening
        self.current_color = self.listening_color if listening else self.base_color
        self.pulse_size = 0
        self._draw()


class GlassCard(tk.Frame):
    """Modern glass-morphism card"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="#1e1b4b")


class CampusAssistantGUI:
    """Premium Modern GUI for Campus Voice Assistant"""
    
    COLORS = {
        'bg_gradient_start': (15, 23, 42),
        'bg_gradient_end': (30, 27, 75),
        'card_bg': '#1e1b4b',
        'card_bg_light': '#312e81',
        'primary': '#6366f1',
        'primary_light': '#818cf8',
        'secondary': '#8b5cf6',
        'accent': '#06b6d4',
        'accent_light': '#22d3ee',
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'text_white': '#ffffff',
        'text_light': '#e2e8f0',
        'text_muted': '#94a3b8',
        'text_dark': '#64748b',
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎓 Campus Voice Assistant")
        self.root.geometry("1100x750")
        self.root.configure(bg='#0f172a')
        self.root.minsize(1000, 650)
        
        self._center_window()
        
        # Initialize components
        self.speech_recognizer = None
        self.tts_manager = None
        self.nlp_processor = IntentProcessor()
        self.response_generator = ResponseGenerator()
        
        self.is_listening = False
        self.voice_enabled = True
        
        self._create_ui()
        self._initialize_components()
        self._show_welcome()
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _center_window(self):
        w, h = 1100, 750
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f'{w}x{h}+{x}+{y}')
    
    def _create_ui(self):
        # Main container
        main = tk.Frame(self.root, bg='#0f172a')
        main.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Quick Actions
        self._create_left_panel(main)
        
        # Center - Chat area
        self._create_center_panel(main)
        
        # Right panel - Voice Control
        self._create_right_panel(main)
    
    def _create_left_panel(self, parent):
        """Create left sidebar with quick actions"""
        left = tk.Frame(parent, bg='#1e1b4b', width=250)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(15, 0), pady=15)
        left.pack_propagate(False)
        
        # App branding
        brand = tk.Frame(left, bg='#1e1b4b')
        brand.pack(fill=tk.X, padx=20, pady=25)
        
        tk.Label(brand, text="🎓", font=("Segoe UI Emoji", 40),
                bg='#1e1b4b', fg='#6366f1').pack()
        tk.Label(brand, text="CAMPUS", font=("Segoe UI", 20, "bold"),
                bg='#1e1b4b', fg='#ffffff').pack()
        tk.Label(brand, text="ASSISTANT", font=("Segoe UI", 12),
                bg='#1e1b4b', fg='#6366f1').pack()
        
        # Divider
        tk.Frame(left, bg='#312e81', height=2).pack(fill=tk.X, padx=20, pady=15)
        
        # Quick actions header
        tk.Label(left, text="⚡ QUICK ACCESS", font=("Segoe UI", 9, "bold"),
                bg='#1e1b4b', fg='#64748b').pack(anchor=tk.W, padx=20, pady=(5, 15))
        
        # Quick action buttons
        actions = [
            ("📅", "Today's Classes", "What are today's classes?", "#6366f1"),
            ("📝", "Exam Schedule", "What is the exam schedule?", "#8b5cf6"),
            ("🏛️", "Departments", "Tell me about departments", "#06b6d4"),
            ("📚", "Library", "Library timings", "#10b981"),
            ("🏥", "Medical", "Medical center info", "#f59e0b"),
            ("🎉", "Events", "Upcoming events", "#ec4899"),
            ("🍽️", "Canteen", "Canteen information", "#14b8a6"),
            ("🚌", "Transport", "Bus information", "#f97316"),
        ]
        
        for emoji, label, query, color in actions:
            self._create_quick_action(left, emoji, label, query, color)
        
        # Spacer
        tk.Frame(left, bg='#1e1b4b').pack(fill=tk.BOTH, expand=True)
        
        # Status indicator
        status_frame = tk.Frame(left, bg='#312e81')
        status_frame.pack(fill=tk.X, padx=15, pady=15)
        
        status_inner = tk.Frame(status_frame, bg='#312e81')
        status_inner.pack(padx=15, pady=12)
        
        self.status_dot = tk.Label(status_inner, text="●", font=("Segoe UI", 14),
                                   bg='#312e81', fg='#f59e0b')
        self.status_dot.pack(side=tk.LEFT)
        
        self.status_text = tk.Label(status_inner, text="Initializing...",
                                    font=("Segoe UI", 10), bg='#312e81', fg='#94a3b8')
        self.status_text.pack(side=tk.LEFT, padx=(8, 0))
    
    def _create_quick_action(self, parent, emoji, label, query, color):
        """Create a quick action button"""
        btn = tk.Frame(parent, bg='#1e1b4b', cursor='hand2')
        btn.pack(fill=tk.X, padx=15, pady=3)
        
        inner = tk.Frame(btn, bg='#1e1b4b')
        inner.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(inner, text=emoji, font=("Segoe UI Emoji", 16),
                bg='#1e1b4b', fg=color).pack(side=tk.LEFT)
        tk.Label(inner, text=label, font=("Segoe UI", 11),
                bg='#1e1b4b', fg='#e2e8f0').pack(side=tk.LEFT, padx=(10, 0))
        
        for widget in [btn, inner] + list(inner.children.values()):
            widget.bind("<Enter>", lambda e, b=btn: b.configure(bg='#312e81') or 
                       [w.configure(bg='#312e81') for w in [b] + list(b.children.values()) + 
                        list(list(b.children.values())[0].children.values()) if hasattr(w, 'configure')])
            widget.bind("<Leave>", lambda e, b=btn: b.configure(bg='#1e1b4b') or
                       [w.configure(bg='#1e1b4b') for w in [b] + list(b.children.values()) +
                        list(list(b.children.values())[0].children.values()) if hasattr(w, 'configure')])
            widget.bind("<Button-1>", lambda e, q=query: self._quick_query(q))
    
    def _create_center_panel(self, parent):
        """Create center chat panel"""
        center = tk.Frame(parent, bg='#0f172a')
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header with greeting
        header = tk.Frame(center, bg='#0f172a')
        header.pack(fill=tk.X, pady=(0, 15))
        
        greeting = self._get_greeting()
        tk.Label(header, text=greeting, font=("Segoe UI", 28, "bold"),
                bg='#0f172a', fg='#ffffff').pack(side=tk.LEFT)
        
        self.time_label = tk.Label(header, text="", font=("Segoe UI", 11),
                                   bg='#0f172a', fg='#64748b')
        self.time_label.pack(side=tk.RIGHT, pady=10)
        self._update_time()
        
        # Chat container
        chat_container = tk.Frame(center, bg='#1e1b4b')
        chat_container.pack(fill=tk.BOTH, expand=True)
        
        # Chat header
        chat_header = tk.Frame(chat_container, bg='#1e1b4b')
        chat_header.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(chat_header, text="💬", font=("Segoe UI Emoji", 18),
                bg='#1e1b4b', fg='#6366f1').pack(side=tk.LEFT)
        tk.Label(chat_header, text="Conversation", font=("Segoe UI", 14, "bold"),
                bg='#1e1b4b', fg='#ffffff').pack(side=tk.LEFT, padx=(10, 0))
        
        # Clear button
        clear_btn = tk.Label(chat_header, text="🗑️ Clear", font=("Segoe UI", 10),
                            bg='#1e1b4b', fg='#64748b', cursor='hand2')
        clear_btn.pack(side=tk.RIGHT)
        clear_btn.bind("<Button-1>", lambda e: self._clear_chat())
        clear_btn.bind("<Enter>", lambda e: clear_btn.configure(fg='#ef4444'))
        clear_btn.bind("<Leave>", lambda e: clear_btn.configure(fg='#64748b'))
        
        # Chat display
        chat_frame = tk.Frame(chat_container, bg='#312e81')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.chat_display = tk.Text(
            chat_frame, wrap=tk.WORD, font=("Segoe UI", 11),
            bg='#312e81', fg='#e2e8f0', insertbackground='white',
            state=tk.DISABLED, padx=20, pady=15, relief=tk.FLAT,
            spacing1=8, spacing3=8, selectbackground='#6366f1'
        )
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(chat_frame, command=self.chat_display.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.config(yscrollcommand=scrollbar.set)
        
        # Text tags
        self.chat_display.tag_configure('user', foreground='#818cf8', font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_configure('bot', foreground='#22d3ee', font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_configure('msg', foreground='#e2e8f0')
        self.chat_display.tag_configure('time', foreground='#64748b', font=("Segoe UI", 9))
        self.chat_display.tag_configure('system', foreground='#f59e0b', font=("Segoe UI", 10, "italic"))
        self.chat_display.tag_configure('error', foreground='#ef4444')
        
        # Input area
        input_frame = tk.Frame(center, bg='#1e1b4b')
        input_frame.pack(fill=tk.X, pady=(15, 0))
        
        input_inner = tk.Frame(input_frame, bg='#312e81')
        input_inner.pack(fill=tk.X, padx=3, pady=3)
        
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            input_inner, textvariable=self.input_var,
            font=("Segoe UI", 13), bg='#312e81', fg='#e2e8f0',
            insertbackground='#6366f1', relief=tk.FLAT, bd=15
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.insert(0, "Type your question here...")
        self.input_entry.config(fg='#64748b')
        self.input_entry.bind('<FocusIn>', self._on_focus_in)
        self.input_entry.bind('<FocusOut>', self._on_focus_out)
        self.input_entry.bind('<Return>', self._on_submit)
        
        send_btn = tk.Label(input_inner, text=" ➤ ", font=("Segoe UI", 20),
                           bg='#312e81', fg='#6366f1', cursor='hand2', padx=15)
        send_btn.pack(side=tk.RIGHT)
        send_btn.bind("<Button-1>", self._on_submit)
        send_btn.bind("<Enter>", lambda e: send_btn.configure(fg='#22d3ee'))
        send_btn.bind("<Leave>", lambda e: send_btn.configure(fg='#6366f1'))
    
    def _create_right_panel(self, parent):
        """Create right panel with voice controls"""
        right = tk.Frame(parent, bg='#1e1b4b', width=220)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 15), pady=15)
        right.pack_propagate(False)
        
        # Voice control section
        tk.Label(right, text="🎙️ VOICE CONTROL", font=("Segoe UI", 10, "bold"),
                bg='#1e1b4b', fg='#64748b').pack(pady=(25, 20))
        
        # Pulsing microphone button
        self.mic_button = PulsingButton(right, command=self._on_voice_click, size=100)
        self.mic_button.pack(pady=20)
        
        # Voice toggle
        toggle_frame = tk.Frame(right, bg='#1e1b4b')
        toggle_frame.pack(pady=20)
        
        self.voice_icon = tk.Label(toggle_frame, text="🔊", font=("Segoe UI Emoji", 24),
                                   bg='#1e1b4b', fg='#10b981', cursor='hand2')
        self.voice_icon.pack()
        self.voice_icon.bind("<Button-1>", self._toggle_voice)
        
        tk.Label(toggle_frame, text="Voice Output", font=("Segoe UI", 9),
                bg='#1e1b4b', fg='#94a3b8').pack(pady=(5, 0))
        
        self.voice_status = tk.Label(toggle_frame, text="ON", font=("Segoe UI", 9, "bold"),
                                     bg='#1e1b4b', fg='#10b981')
        self.voice_status.pack()
        
        # Divider
        tk.Frame(right, bg='#312e81', height=2).pack(fill=tk.X, padx=20, pady=20)
        
        # Tips section
        tk.Label(right, text="💡 TIPS", font=("Segoe UI", 10, "bold"),
                bg='#1e1b4b', fg='#64748b').pack(pady=(5, 15))
        
        tips = [
            "Click mic to speak",
            "Ask about classes",
            "Check exam dates",
            "Find facilities",
        ]
        
        for tip in tips:
            tk.Label(right, text=f"• {tip}", font=("Segoe UI", 9),
                    bg='#1e1b4b', fg='#94a3b8', anchor='w').pack(fill=tk.X, padx=25, pady=3)
        
        # Spacer
        tk.Frame(right, bg='#1e1b4b').pack(fill=tk.BOTH, expand=True)
        
        # Help button
        help_btn = tk.Label(right, text="❓ Help & Commands", font=("Segoe UI", 10),
                           bg='#312e81', fg='#94a3b8', cursor='hand2', pady=12)
        help_btn.pack(fill=tk.X, padx=15, pady=15)
        help_btn.bind("<Button-1>", lambda e: self._show_help())
        help_btn.bind("<Enter>", lambda e: help_btn.configure(fg='#ffffff', bg='#6366f1'))
        help_btn.bind("<Leave>", lambda e: help_btn.configure(fg='#94a3b8', bg='#312e81'))
    
    def _get_greeting(self):
        hour = datetime.now().hour
        if hour < 12:
            return "Good Morning! ☀️"
        elif hour < 17:
            return "Good Afternoon! 🌤️"
        else:
            return "Good Evening! 🌙"
    
    def _update_time(self):
        self.time_label.config(text=datetime.now().strftime("%I:%M %p  •  %B %d, %Y"))
        self.root.after(1000, self._update_time)
    
    def _on_focus_in(self, event):
        if self.input_var.get() == "Type your question here...":
            self.input_entry.delete(0, tk.END)
            self.input_entry.config(fg='#e2e8f0')
    
    def _on_focus_out(self, event):
        if not self.input_var.get():
            self.input_entry.insert(0, "Type your question here...")
            self.input_entry.config(fg='#64748b')
    
    def _toggle_voice(self, event=None):
        self.voice_enabled = not self.voice_enabled
        if self.voice_enabled:
            self.voice_icon.config(fg='#10b981')
            self.voice_status.config(text="ON", fg='#10b981')
        else:
            self.voice_icon.config(fg='#64748b')
            self.voice_status.config(text="OFF", fg='#64748b')
    
    def _quick_query(self, query):
        self._add_message("user", query)
        threading.Thread(target=self._process, args=(query,), daemon=True).start()
    
    def _initialize_components(self):
        def init():
            try:
                self._set_status("Initializing...", "warning")
                self.speech_recognizer = SpeechRecognizer()
                self.tts_manager = TTSManager()
                self._set_status("Ready", "success")
            except Exception as e:
                self._add_message("error", f"Init error: {e}")
                self._set_status("Text Mode", "warning")
        
        threading.Thread(target=init, daemon=True).start()
    
    def _show_welcome(self):
        welcome = """Welcome to Campus Voice Assistant! 🎓

I'm here to help you with:
  ✨ Class schedules and timetables
  ✨ Exam dates and information
  ✨ Department details and contacts
  ✨ Campus facilities info
  ✨ Events and activities

👉 Click the microphone or type below to get started!"""
        self._add_message("bot", welcome)
    
    def _add_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        time_str = datetime.now().strftime("%I:%M %p")
        
        if sender == "user":
            self.chat_display.insert(tk.END, f"\n👤 You ", 'user')
            self.chat_display.insert(tk.END, f"  {time_str}\n", 'time')
            self.chat_display.insert(tk.END, f"{message}\n", 'msg')
        elif sender == "bot":
            self.chat_display.insert(tk.END, f"\n🤖 Assistant ", 'bot')
            self.chat_display.insert(tk.END, f"  {time_str}\n", 'time')
            self.chat_display.insert(tk.END, f"{message}\n", 'msg')
        elif sender == "error":
            self.chat_display.insert(tk.END, f"\n⚠️ {message}\n", 'error')
        elif sender == "system":
            self.chat_display.insert(tk.END, f"\n{message}\n", 'system')
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def _set_status(self, text, state="normal"):
        self.status_text.config(text=text)
        colors = {"success": "#10b981", "warning": "#f59e0b", "error": "#ef4444", "normal": "#94a3b8"}
        self.status_dot.config(fg=colors.get(state, "#94a3b8"))
    
    def _on_voice_click(self):
        if self.is_listening:
            return
        if not self.speech_recognizer or not self.speech_recognizer.microphone_available:
            self._add_message("error", "Microphone not available. Please type instead.")
            return
        threading.Thread(target=self._listen, daemon=True).start()
    
    def _listen(self):
        self.is_listening = True
        self.mic_button.set_listening(True)
        self._set_status("Listening...", "warning")
        
        try:
            text = self.speech_recognizer.get_text_from_speech()
            if text:
                self._add_message("user", text)
                self._process(text)
            else:
                self._add_message("error", "Couldn't understand. Please try again.")
        except Exception as e:
            self._add_message("error", f"Error: {e}")
        finally:
            self.is_listening = False
            self.mic_button.set_listening(False)
            self._set_status("Ready", "success")
    
    def _on_submit(self, event=None):
        text = self.input_var.get().strip()
        if not text or text == "Type your question here...":
            return
        self.input_entry.delete(0, tk.END)
        self._add_message("user", text)
        threading.Thread(target=self._process, args=(text,), daemon=True).start()
    
    def _process(self, query):
        self._set_status("Processing...", "warning")
        try:
            if any(w in query.lower() for w in ['exit', 'quit', 'bye']):
                response = "Goodbye! Have a great day! 👋"
                self._add_message("bot", response)
                if self.voice_enabled and self.tts_manager:
                    self.tts_manager.speak(response)
                self.root.after(2000, self.root.quit)
                return
            
            result = self.nlp_processor.process_query(query)
            response = self.response_generator.generate_response(result)
            self._add_message("bot", response)
            
            if self.voice_enabled and self.tts_manager:
                self.tts_manager.speak(response[:400] if len(response) > 400 else response)
        except Exception as e:
            self._add_message("error", f"Error: {e}")
        finally:
            self._set_status("Ready", "success")
    
    def _show_help(self):
        self._add_message("bot", self.response_generator.get_help_message())
    
    def _clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self._show_welcome()
    
    def _on_close(self):
        if self.tts_manager:
            self.tts_manager.stop()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()


def main():
    try:
        app = CampusAssistantGUI()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    main()
