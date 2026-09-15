# Speak Anywhere

**Offline voice dictation and text-to-speech for Windows.** Tap the microphone and your words are
typed into whatever app has focus. Copy any text and have it read back in a natural neural voice.
Nothing leaves the machine — no API keys, no accounts, no cloud.

---

## What changed in this version

Speak Anywhere originally used [Vosk](https://alphacephei.com/vosk/) for speech recognition. Vosk
is fast and tiny, but it is built on Kaldi, and that generation of recognizer has been overtaken.
In everyday use it got conversational speech wrong often enough to be frustrating, and moving to
Vosk's *most* accurate English model did not fix it — it just made startup take 35 seconds.

The recognizer is now **[NVIDIA Parakeet TDT 0.6B v2](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2)**,
running on the CPU through [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx), with
[Silero VAD](https://github.com/snakers4/silero-vad) deciding what counts as speech.

Here is the actual difference. One 7-second recording from a USB microphone, normal speaking voice,
transcribed by both engines:

| Engine | Transcript |
|---|---|
| Vosk (large English model) | `it's the work and get ready for you` |
| Parakeet TDT 0.6B v2 | `So we're gonna get ready for some soccer, okay? Love you.` |

Vosk did not recover a single content word. Parakeet got the sentence, the contractions, the
punctuation, and the capitalization — none of which Vosk emits at all.

### The tradeoff, stated plainly

Vosk is a streaming recognizer: words appear as you say them. Parakeet transcribes a whole
utterance at once, so text lands roughly a second or two **after** you finish a phrase rather than
trickling out live. That is the cost of the accuracy, and it is the reason the dictation loop had
to be rewritten rather than just repointed at a new model file.

---

## How dictation works now

```
microphone ──► 512-sample windows ──► Silero VAD ──► speech segments
                                                          │
                                                          ▼
                                                   segment queue
                                                          │
                                                          ▼
                                    decoder thread ──► Parakeet ──► pyautogui types it
```

Three things matter in that diagram:

**Silero decides what is speech.** The recognizer never sees room noise, keyboard clatter, or a
door closing. An earlier energy-threshold version of this triggered on a single loud bump and
transcribed nothing; a real VAD does not make that mistake.

**Decoding happens off the audio thread.** Transcribing a phrase takes about as long as saying it.
If that ran on the thread draining the microphone, every word spoken *during* a decode would be
dropped by the audio buffer. Segments go onto a queue and a worker thread handles them, so you can
keep talking straight through.

**Pending speech still gets typed when you stop.** Switching dictation off drains the queue first,
so the last thing you said before hitting the button is not silently lost.

---

## Startup

Launch does three slow things: play a 6-second splash video, load the speech model, and load the
Piper voice. Both model loads now run on background threads started *before* the video is waited
on, so they finish behind the animation instead of adding their time on top of it.

Measured on an 11th-gen Core i7-1185G7 (4 cores, no discrete GPU):

| Step | Time |
|---|---|
| Parakeet model load | ~15 s (overlaps the splash) |
| Piper voice load | overlaps the splash |
| Decode, 4 threads | ~1.9x realtime |
| Decode, 8 threads | ~1.1x realtime |

Note the thread count. Hyperthreading actively hurts here — 8 threads is slower than 4 on this CPU,
because the sibling threads contend for the same execution units. The app derives its thread count
from your machine rather than hardcoding one: roughly half the logical processors, clamped between
2 and 8. Nothing to configure.

---

## Requirements

- Windows 10 or 11
- Python 3.11 (if running from source)
- A microphone, and speakers or headphones
- ~3 GB of disk for the speech model
- No GPU required

---

## Setup

```bash
git clone https://github.com/nicedreamzapp/SpeakAnywhere.git
cd SpeakAnywhere
pip install -r requirements.txt
```

### Download the speech model

The model is not in this repository — it is 2.5 GB. Pull the full-precision ONNX export into
`_resources/parakeet-tdt-0.6b-v2/`:

```bash
mkdir -p _resources/parakeet-tdt-0.6b-v2
cd _resources/parakeet-tdt-0.6b-v2
BASE=https://huggingface.co/csukuangfj/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2/resolve/main
curl -LO $BASE/encoder.onnx
curl -LO $BASE/encoder.weights    # 2.4 GB, this is the slow one
curl -LO $BASE/decoder.onnx
curl -LO $BASE/joiner.onnx
curl -LO $BASE/tokens.txt
```

`encoder.onnx` references `encoder.weights` as external data, so both files must sit in the same
folder.

### Download the voice activity detector

```bash
cd _resources
curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx
```

### Run

```bash
python speak_anywhere.py
```

There are int8 builds of the same model that load faster and use a third of the memory. This
project deliberately uses the full-precision export — accuracy is the entire reason for the switch,
and quantization is the first thing that erodes it.

---

## Using it

1. **Launch** and wait out the splash.
2. **Dictate** — tap the microphone, talk, and your words are typed at the cursor. Tap again to stop.
3. **Listen** — copy text to the clipboard, tap Speak Clipboard.
4. **Adjust** — playback speed runs 0.5x to 2.0x, and the microphone and speaker are both selectable.

### Voice commands

| Say | Get |
|---|---|
| "new line" | Enter keypress |
| "period" | `.` |
| "comma" | `,` |

Parakeet emits real punctuation on its own, so these are mostly a holdover for when you want to be
explicit.

---

## Project structure

```
SpeakAnywhere/
├── speak_anywhere.py               # the whole application
├── requirements.txt
├── LICENSE.txt
├── CREDITS.md                      # upstream projects this is built on
└── _resources/
    ├── SpeakAnywhere.ico
    ├── splash_video.mp4
    ├── splash_audio.mp3
    ├── silero_vad.onnx             # downloaded, see setup
    ├── parakeet-tdt-0.6b-v2/       # downloaded, see setup
    └── piper/                      # Piper neural voices
```

---

## Building an executable

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole \
  --icon="_resources\SpeakAnywhere.ico" \
  --name="SpeakAnywhere" \
  --collect-all sherpa_onnx --collect-all cv2 \
  speak_anywhere.py
```

---

## Built on

- **[NVIDIA Parakeet TDT](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2)** — speech recognition
- **[sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)** — ONNX runtime for the recognizer and VAD
- **[Silero VAD](https://github.com/snakers4/silero-vad)** — voice activity detection
- **[Piper](https://github.com/rhasspy/piper)** — offline neural text-to-speech
- **[PyAudio](https://pypi.org/project/PyAudio/)** / **[sounddevice](https://python-sounddevice.readthedocs.io/)** — audio I/O
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)** — keyboard automation
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)** — interface
- **[OpenCV](https://opencv.org/)** and **[Pygame](https://www.pygame.org/)** — splash video and audio

See [CREDITS.md](CREDITS.md) for full attribution.

---

## License

Copyright (c) 2024 Nice Dreamz LLC. All Rights Reserved.
Proprietary software — see [LICENSE.txt](LICENSE.txt).

## Author

Matt Macosko, Nice Dreamz LLC
info@nicedreamz.wholesale.com
