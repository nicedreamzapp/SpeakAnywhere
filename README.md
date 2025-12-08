# Speak Anywhere

**Voice-powered productivity for Windows** - Dictate text anywhere and have any text read aloud with natural voices.

---

## Features

### Voice Dictation
Tap the microphone and speak - your words are typed automatically wherever your cursor is. Perfect for:
- Writing emails and documents
- Messaging and chat
- Taking notes
- Any text input field

### Text-to-Speech
Copy any text to your clipboard, then tap "Speak Clipboard" to hear it read aloud using natural-sounding Microsoft neural voices. Great for:
- Proofreading your writing
- Accessibility
- Multitasking while listening
- Learning and comprehension

### Additional Features
- **Speed Control** - Adjust playback speed from 0.5x to 2.0x
- **Device Selection** - Choose your preferred microphone and speaker
- **Offline Speech Recognition** - Uses Vosk for privacy-focused, offline voice recognition
- **Desktop Shortcuts** - Optional desktop and Start Menu shortcuts on first run
- **Portable** - Run from USB drive without installation

---

## Requirements

- Windows 10 or Windows 11
- Microphone (built-in or USB)
- Speakers or headphones

---

## Quick Start

### Option 1: Download Release (Recommended)
1. Download `SpeakAnywhere.exe` from [Releases](https://github.com/nicedreamzapp/SpeakAnywhere/releases)
2. Download the Vosk model (see below)
3. Run the executable

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/nicedreamzapp/SpeakAnywhere.git
cd SpeakAnywhere

# Install dependencies
pip install -r requirements.txt

# Download Vosk model (required)
# Place in _resources/vosk-model-small-en-us-0.15/

# Run
python speak_anywhere.py
```

---

## Vosk Model Setup

Speak Anywhere uses Vosk for offline speech recognition. You need to download the model:

1. Download from: https://alphacephei.com/vosk/models
2. Get: `vosk-model-small-en-us-0.15` (40 MB) or larger models for better accuracy
3. Extract to: `_resources/vosk-model-small-en-us-0.15/`

---

## How to Use

1. **Launch** - Run `SpeakAnywhere.exe` or `python speak_anywhere.py`
2. **Wait for splash** - The app loads the speech model (first time may take a moment)
3. **Setup options** - Choose to create desktop shortcuts if desired
4. **Dictate** - Tap the microphone icon, speak, and watch your words appear
5. **Listen** - Copy text, tap "Speak Clipboard" to hear it read aloud
6. **Close** - Click the X button to exit

### Voice Commands
- Say "new line" to press Enter
- Say "period" or "comma" to insert punctuation

---

## Building from Source

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --noconsole --icon="_resources\SpeakAnywhere.ico" --name="SpeakAnywhere" --collect-all vosk --collect-all cv2 speak_anywhere.py
```

The executable will be created in the `dist/` folder.

---

## Project Structure

```
SpeakAnywhere/
├── speak_anywhere.py      # Main application
├── LICENSE.txt            # License agreement
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── _resources/            # App resources (hidden folder)
│   ├── SpeakAnywhere.ico  # App icon
│   ├── splash_video.mp4   # Splash screen video
│   ├── splash_audio.mp3   # Splash screen audio
│   └── vosk-model-*/      # Speech recognition model
└── dist/                  # Built executable (after build)
```

---

## Technologies Used

- **[Vosk](https://alphacephei.com/vosk/)** - Offline speech recognition
- **[Edge TTS](https://github.com/rany2/edge-tts)** - Microsoft neural text-to-speech
- **[PyAudio](https://pypi.org/project/PyAudio/)** - Audio I/O
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)** - GUI framework
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)** - Keyboard automation
- **[Pygame](https://www.pygame.org/)** - Audio playback
- **[OpenCV](https://opencv.org/)** - Video playback for splash screen

---

## License

Copyright (c) 2024 Nice Dreamz LLC. All Rights Reserved.

This is proprietary software. See [LICENSE.txt](LICENSE.txt) for details.

---

## Author

**Matt Macosko**
Nice Dreamz LLC
info@nicedreamz.wholesale.com

---

## Support

For issues and feature requests, please open an issue on GitHub.
