# Voice-Controlled Campus Assistant 🎓

A Python-based voice-controlled assistant that helps students and staff access campus information using voice commands. The system uses speech recognition to capture voice input, processes natural language queries, retrieves information from the database, and responds with both text and voice output.

## 📋 Features

- **Voice Input**: Capture voice commands using microphone
- **Speech Recognition**: Convert speech to text using Google Speech API
- **Natural Language Processing**: Identify user intent and extract entities
- **Data Retrieval**: Fetch information from JSON database
- **Voice Output**: Convert text responses to speech using pyttsx3
- **GUI Interface**: User-friendly Tkinter-based graphical interface
- **Console Mode**: Command-line interface for simple interaction

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.8+ |
| Speech Recognition | SpeechRecognition library |
| Text-to-Speech | pyttsx3 (offline) |
| NLP | Custom keyword matching & pattern recognition |
| GUI | Tkinter |
| Database | JSON files |

## 📁 Project Structure

```
Voice-control-campus-assistance/
│
├── main.py                 # Console application
├── gui_app.py              # GUI application (Tkinter)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── modules/
│   ├── __init__.py
│   ├── speech_recognition_module.py    # Voice input handling
│   ├── text_to_speech_module.py        # Voice output handling
│   ├── nlp_processor.py                # Intent identification
│   ├── data_handler.py                 # Data operations
│   └── response_generator.py           # Response generation
│
└── data/
    ├── timetable.json      # Class schedules
    ├── exams.json          # Exam schedules
    ├── departments.json    # Department information
    ├── campus_info.json    # Facilities & events
    └── faqs.json           # Frequently asked questions
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Microphone (for voice input)
- Speakers/Headphones (for voice output)

### Step 1: Clone or Download the Project

```bash
cd Voice-control-campus-assistance
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install PyAudio (Windows)

If you face issues installing PyAudio on Windows:

```bash
pip install pipwin
pipwin install pyaudio
```

Or download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

## 🎮 Usage

### GUI Mode (Recommended)

```bash
python gui_app.py
```

This opens a graphical interface where you can:
- Click the microphone button to speak
- Type questions in the text box
- Toggle voice output on/off
- View conversation history

### Console Mode

```bash
python main.py
```

#### Command Line Options:

```bash
# Text-only mode (no voice input/output)
python main.py --text-only

# Disable voice input only
python main.py --no-voice-input

# Disable voice output only
python main.py --no-voice-output
```

## 💬 Sample Queries

### Timetable
- "What are today's classes?"
- "CSE schedule for Monday"
- "Tomorrow's timetable for ECE"
- "What is my class schedule?"

### Exams
- "What is the exam schedule?"
- "Tomorrow's exams"
- "CSE exam dates"
- "When is the next exam?"

### Departments
- "Tell me about CSE department"
- "Who is the HOD of ECE?"
- "Department contact information"
- "Information about mechanical department"

### Facilities
- "Library timings"
- "Where is the canteen?"
- "Hostel information"
- "Sports facilities"
- "Medical center contact"

### Events
- "Upcoming events"
- "College fest details"
- "When is the tech fest?"

### FAQs
- "How to apply for leave?"
- "What is the attendance requirement?"
- "Fee structure"
- "How to get bonafide certificate?"

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Voice Input   │────▶│ Speech           │────▶│ Text Query      │
│   (Microphone)  │     │ Recognition      │     │                 │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Voice Output  │◀────│ Text-to-Speech   │◀────│ Response        │
│   (Speaker)     │     │ (pyttsx3)        │     │ Generator       │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │ Data Handler     │◀────│ NLP Processor   │
                        │ (JSON Files)     │     │ (Intent)        │
                        └──────────────────┘     └─────────────────┘
```

## 📊 Workflow

1. **Voice Input Capture**: User speaks into microphone
2. **Speech Recognition**: Google Speech API converts voice to text
3. **Query Processing**: Text is preprocessed and cleaned
4. **Intent Identification**: System identifies user's intent using keyword matching
5. **Entity Extraction**: Extract relevant entities (department, day, facility)
6. **Data Retrieval**: Fetch information from JSON database
7. **Response Generation**: Create meaningful response text
8. **Voice Output**: Convert response to speech and play

## 🔧 Customization

### Adding New Data

Edit the JSON files in the `data/` folder:

- **timetable.json**: Add class schedules
- **exams.json**: Update exam information
- **departments.json**: Modify department details
- **campus_info.json**: Update facility information
- **faqs.json**: Add new FAQs

### Adding New Intents

Edit `modules/nlp_processor.py`:

```python
self.intents = {
    'new_intent': {
        'keywords': ['keyword1', 'keyword2'],
        'patterns': [r'pattern.*regex']
    }
}
```

### Changing Voice Settings

Edit `modules/text_to_speech_module.py` or pass parameters:

```python
tts = TextToSpeech(rate=150, volume=0.9, voice_index=0)
```

## ⚠️ Troubleshooting

### "No module named 'speech_recognition'"
```bash
pip install SpeechRecognition
```

### "No module named 'pyaudio'"
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# Linux
sudo apt-get install portaudio19-dev
pip install pyaudio

# macOS
brew install portaudio
pip install pyaudio
```

### "Could not request results from Google Speech Recognition"
- Check your internet connection
- Google Speech API requires internet access

### No voice output
- Check if speakers are connected
- Verify volume is not muted
- Try: `pip install pyttsx3 --upgrade`

## 🎯 Future Enhancements

- [ ] Multilingual voice support (Hindi, Tamil, etc.)
- [ ] Login-based access for students/staff
- [ ] Machine learning for better intent recognition
- [ ] Web version using Flask
- [ ] Mobile application
- [ ] Integration with college ERP system
- [ ] Offline speech recognition using Vosk

## 📝 License

This project is created for educational purposes.

## 👥 Contributors

- Campus Assistant Development Team

## 📞 Support

For issues or queries, please create an issue in the project repository.

---

**Made with ❤️ for campus community**
