# Speak Anywhere press kit

Draft for review. Items marked **TODO-VERIFY** need Matt to confirm or fill in before anything goes out.

## Fact sheet

| | |
|---|---|
| Name | Speak Anywhere |
| What it is | Offline dictation and read-aloud for Windows |
| Platforms | Windows 10 and 11 (desktop). No Mac, Linux, iOS or Android version. |
| Price | Free download from GitHub releases. **TODO-VERIFY** that free is the intended price for press. |
| Current version | 1.1 (GitHub release `v1.1.0`, published 2026-09-21). Note: `APP_VERSION` in `speak_anywhere.py` still reads `1.0.0`. **TODO-VERIFY** |
| Download | https://github.com/nicedreamzapp/SpeakAnywhere/releases/latest/download/Speak-Anywhere-windows.zip |
| Source | https://github.com/nicedreamzapp/SpeakAnywhere |
| App Store / Google Play | None in the repo. **TODO-VERIFY** (likely not applicable) |
| Requirements | Windows 10 or 11, a microphone, speakers or headphones, about 3 GB of disk for the models, internet once for the first-run download. No GPU. |
| Developer | Matt Macosko / Nice Dreamz LLC |
| Contact | info@nicedreamzwholesale.com |
| Web | https://nicedreamzwholesale.com/software/ (**TODO-VERIFY** final page URL for Speak Anywhere) |
| License | Proprietary, copyright 2024 Nice Dreamz LLC |
| Built on | NVIDIA Parakeet TDT 0.6B v2 (recognition), Kokoro-82M (voices), Silero VAD (speech detection), sherpa-onnx (runtime), Piper (alternate voices, source build only), PyAutoGUI, PyAudio, sounddevice, Tkinter, OpenCV, Pygame |
| Assets | Icon `_resources/SpeakAnywhere.ico`, splash image `_resources/splash.png` (320x140). **TODO-VERIFY**: no screenshots of the main window or Voice Picker exist in the repo yet. |

### Release history (from git history and GitHub releases)

| Date | What |
|---|---|
| 2025-12-07 | First commit, "Speak Anywhere v1.0.0". Vosk recognition, Microsoft neural voices through edge-tts. |
| 2025-12-08 | Switched to offline Piper voices, added speaker selection, loading progress bar, standalone exe packaging fixes. |
| 2026-08-06 | Added CREDITS.md for upstream projects. |
| 2026-09-14 | Replaced Vosk with NVIDIA Parakeet TDT 0.6B v2. Replaced Piper as the default with Kokoro-82M and added the voice picker. Device menus rebuilt from WASAPI. |
| 2026-09-16 | Streaming reader that starts on the first sentence. Window no longer waits for the recognizer to load. |
| 2026-09-21 | Windows download: one folder with Speak Anywhere.exe and Voice Picker.exe, models fetched on first run. Published as GitHub release v1.1.0 "Speak Anywhere for Windows 1.1". |

There are no git tags in the local clone; v1.1.0 exists only as a GitHub release.

### Numbers you can quote

All from the project README, measured on an 11th-gen Core i7-1185G7 (4 cores, no discrete GPU), old Vosk build vs current build:

- Time to window: 129.5 s to 2.6 s
- First word of a 2,500 character read: 77 s to 1.2 s
- Memory: 9.6 GB to 2.3 GB
- Recognizer decode speed: 1.9x realtime at 4 threads
- Kokoro voice rendering: about 1.75x realtime on CPU
- Stop while reading: within 0.2 s

Same 7 second clip, same mic: Vosk output was "it's the work and get ready for you". Parakeet got the full sentence with contractions, punctuation and capitals. (See Privacy flags in the PR before quoting the actual sentence.)

## 50-word description

Speak Anywhere is a free Windows app for dictation and read-aloud that runs entirely on your own PC. Talk, and your words are typed into whatever window has focus. Copy text, and it reads it back in a natural voice. After a one-time model download, nothing goes over the network.

## 150-word description

Speak Anywhere is a Windows 10 and 11 app that does two things. Tap the mic and talk, and when you finish a phrase the words are typed into whatever window has focus, with capitals and punctuation. Copy any text and tap Speak Clipboard, and it reads it aloud, starting on the first sentence, at speeds from 0.5x to 2x.

Everything runs on the CPU. Recognition is NVIDIA's Parakeet TDT 0.6B v2, voices are Kokoro-82M, and Silero VAD keeps background noise away from the recognizer, all through the sherpa-onnx runtime. The first launch downloads about 3 GB of models once; after that it works offline, with no account, no API key and no GPU.

A separate Voice Picker lets you audition 15 English voices and keep one. On a 4-core laptop the window opens in 2.6 seconds and a long read starts talking in 1.2.

## Feature bullets

- Types what you say into any Windows app, with punctuation.
- Reads copied text aloud, starting on the first sentence.
- Runs offline on your CPU after a one-time download.
- 15 graded English voices, picked in a separate Voice Picker.
- Speed from 0.5x to 2x, any mic and any speaker.

## Pitch email to app reviewers

Subject: Speak Anywhere, offline dictation and read-aloud for Windows

Hi {name},

I made a Windows app that types what you say into any window and reads copied text back to you, and none of it leaves the PC. The speech recognition is NVIDIA's Parakeet model and the voices are Kokoro, both running on the CPU through sherpa-onnx. No account, no API key, no GPU.

The thing I'm happiest with is the reader. It starts talking 1.2 seconds after you hit the button, even on a long paste. The old version took 77 seconds on the same text because it rendered the whole thing first.

It's free. The download is here:
https://github.com/nicedreamzapp/SpeakAnywhere/releases/latest/download/Speak-Anywhere-windows.zip

First launch pulls about 3 GB of models once. It isn't code-signed yet, so Windows will ask you to click More info and Run anyway.

Press page with screenshots and details: {TODO-VERIFY: press page URL}

Matt Macosko
Nice Dreamz LLC
info@nicedreamzwholesale.com
