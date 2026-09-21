<div align="center">

# 🎙️ Speak Anywhere

### 🗣️ Talk to any app. 🔊 Have any text read back.

**💯 Completely offline.** No API keys. No accounts. No cloud.
**Nothing ever leaves your machine.**

<br>

![Offline](https://img.shields.io/badge/100%25-OFFLINE-2ea44f?style=for-the-badge)
![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![No GPU](https://img.shields.io/badge/GPU-NOT%20REQUIRED-FF8700?style=for-the-badge)

![ASR](https://img.shields.io/badge/🎧_Recognition-Parakeet_TDT_0.6B-76B900?style=flat-square)
![TTS](https://img.shields.io/badge/🗣️_Speech-Kokoro--82M-FF6B9D?style=flat-square)
![VAD](https://img.shields.io/badge/🧠_Detection-Silero-5865F2?style=flat-square)
![Runtime](https://img.shields.io/badge/⚙️_Runtime-sherpa--onnx-24292e?style=flat-square)

</div>

<br>

---

## 📑 Contents

<table>
<tr>
<td valign="top" width="33%">

**🚀 Start here**
- [⚡ What it does](#-what-it-does)
- [📦 Setup](#-setup)
- [🎛️ Using it](#-using-it)

</td>
<td valign="top" width="33%">

**🔬 What changed**
- [🔥 Vosk is gone](#-the-big-change-vosk-is-gone)
- [📊 Speed & memory](#-and-it-got-dramatically-faster)
- [🗣️ The voice](#-the-voice)

</td>
<td valign="top" width="33%">

**🛠️ Under the hood**
- [🔊 How the reader works](#-how-the-reader-actually-works)
- [⚙️ How dictation works](#-how-dictation-actually-works)
- [📈 Performance](#-performance)
- [📁 Structure](#-project-structure)
- [🙏 Built on](#-built-on)

</td>
</tr>
</table>

<br>

---

## ⚡ What it does

<table>
<tr>
<td align="center" width="33%">

### 🎤
### **Dictate**

Tap the mic and talk.
Your words are **typed into
whatever window has focus.**

</td>
<td align="center" width="33%">

### 🔊
### **Listen**

Copy any text, tap
**Speak Clipboard**, hear it
in a natural neural voice.

</td>
<td align="center" width="33%">

### 🔒
### **Stay private**

Every model runs locally.
The app **never opens a
network connection.**

</td>
</tr>
</table>

<br>

---

## 🔥 The big change: Vosk is gone

<table>
<tr>
<td width="50%" valign="top">

### ❌ **Before** — Vosk

> it's the work and get ready for you

**Not one content word correct.**
No punctuation. No capitals.

</td>
<td width="50%" valign="top">

### ✅ **After** — Parakeet

> So we're gonna get ready for some soccer, okay? Love you.

**Sentence, contractions, punctuation, capitals.** All of it.

</td>
</tr>
</table>

> 🎧 **Same 7-second recording. Same USB microphone. Same moment.** Only the engine changed.

Vosk is built on **Kaldi**, and that generation of recognizer has simply been overtaken. Switching
to Vosk's *most accurate* English model didn't fix it either — it just pushed cold start to
**35 seconds**.

<br>

### 📊 And it got dramatically faster

<div align="center">

| | 🐌 **Before** | 🚀 **Now** | 🎯 **Gain** |
|---:|:---:|:---:|:--|
| ⏱️ **Time to window** | `129.5 s` | `2.6 s` | **127 seconds faster** |
| 🎤 **Dictation ready** | `129.5 s` | `~5 s` | *the recognizer loads behind the open window* |
| 🔊 **First word of a long read** | `77 s` | `1.2 s` | *no longer grows with the text* |
| 🧠 **Memory** | `9.6 GB` | `2.3 GB` | **7.3 GB lighter** |

</div>

> [!NOTE]
> 🕵️ **Why the old number was so bad.** The old build loaded its 2.7 GB speech model **twice** —
> once in the launcher, once in the app, which never read the launcher's copy. That 9.6 GB was
> **two full copies of the same model** sitting in RAM.

> [!NOTE]
> ⏱️ **Nothing on screen waits for a model any more.** The window used to sit behind the full
> splash video *and* a 2.4 GB recognizer load. Speak Clipboard never touches the recognizer, and
> dictation only needs it to **decode** — so it loads behind the open window, the microphone opens
> immediately, and audio is buffered until it arrives. **Nothing spoken in those first seconds is
> lost.**
>
> The `77 s` above was a **2,500 character** paste. It is not a typo: the old reader rendered the
> **entire** clipboard to a WAV before playing a single word, so the silence scaled with the text.

<br>

---

## 🗣️ The voice

Text-to-speech used to be **Piper** on `en_US-hfc_male-medium`. Small, fast, and **audibly
synthetic** on anything longer than a sentence.

It now runs **[Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)** through sherpa-onnx — which
was **already a dependency**, so this added **zero** new ones.

<div align="center">

| | 🔈 **Piper** | 🔊 **Kokoro-82M** |
|---:|:---:|:---:|
| 🧬 **Parameters** | ~20 M | **82 M** |
| 🎭 **Naturalness** | flat, synthetic | **markedly better** |
| ⚡ **Speed on CPU** | fast | **~1.5x realtime** |
| 📅 **Generation** | older | **current** |

</div>

Piper **stays available** rather than deleted. A few of its voices hold up fine.

<br>

### 🎚️ Picking one

```bash
python voice_picker.pyw
```

**Click a voice** ▸ hear it read a sample line ▸ **Use this voice**.
Saved to `%APPDATA%/SpeakAnywhere/voice.json`, picked up on next launch.

> [!TIP]
> 🧹 **The list is short on purpose.** Kokoro ships **54 voices** and publishes a
> [quality grade for each](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md).
> Everything graded **C or D is excluded** — `am_adam` is a **D** — plus `af_sky` and `am_santa`,
> both trained on only **minutes** of audio.
>
> ✅ **What's left: 15 English voices at grade A or B, plus 3 Piper voices.**
> The point is to *pick* a voice, not to audition a pile of bad ones.

<br>

---

## 🔊 How the reader actually works

It **starts talking on the first sentence** instead of rendering the whole clipboard first.

<div align="center">

```
  📋 clipboard
       │
       ▼
  sentences ──► chunks: 60 chars ─► 90 ─► 135 ─► 202 ─► 400 …
                          │
                          ▼
                   🗣️ render thread ──► 📥 queue (3 deep) ──► 🔈 one output stream
                       ~1.75x realtime                          gapless
```

</div>

**The opener is short because it is the only piece anyone waits on.** Everything after it is
rendered while earlier audio is still playing.

<div align="center">

| | Why it is built this way |
|:--:|:--|
| 📈 | **Chunks grow by half each time.** Rendering runs ~1.75x faster than speech plays, so every pass banks more finished audio than it spends. Jumping straight to full size leaves the renderer **8 seconds behind** after a 2 second opener — a stall exactly where it is most audible. |
| ✂️ | **A long opening sentence is broken at its commas.** Only near the start, where there is no buffer to coast on. Past that, sentences are left whole so chunk edges land where a reader would pause anyway. |
| 🔗 | **One output stream for the whole read**, opened on the first chunk's rate — so the joins are silent instead of a click per sentence. |
| ⏹️ | **Stop lands within 0.2 s.** Audio is written to the device in fifths of a second rather than a chunk at a time. |

</div>

> [!NOTE]
> 🎯 **Measured on a 2 minute read: no gap at all.** `1.2 s` to the first word, and the renderer
> stayed ahead of the listener for the remaining `128 s` of audio.

<br>

---

## ⚙️ How dictation actually works

<div align="center">

```
  🎤 microphone
       │
       ▼
  512-sample windows ──► 🧠 Silero VAD ──► speech segments
                                                │
                                                ▼
                                         📥 segment queue
                                                │
                                                ▼
                            🔀 decoder thread ──► Parakeet ──► ⌨️ typed
```

</div>

<table>
<tr>
<td width="33%" valign="top">

### 🧠 **Silero decides what is speech**

The recognizer **never sees room noise** or keyboard clatter.

An early energy-threshold version fired on a single **door bump** and transcribed nothing.

</td>
<td width="33%" valign="top">

### 🔀 **Decoding is off the audio thread**

Transcribing a phrase takes **about as long as saying it**.

Inline, every word spoken *during* a decode would be **dropped by the buffer**.

</td>
<td width="33%" valign="top">

### 📥 **Nothing is lost on stop**

Switching dictation off **drains the queue first**.

The last thing you said before hitting the button **still lands**.

</td>
</tr>
</table>

> [!IMPORTANT]
> ⚖️ **The tradeoff, stated plainly.** Vosk **streamed** words as you spoke them. Parakeet
> transcribes a **whole utterance**, so text lands a second or two *after* you finish a phrase
> instead of trickling out live.
>
> That is the **cost of the accuracy** — and the reason the dictation loop was rewritten rather
> than just repointed at a new model file.

<br>

---

## 📈 Performance

Measured on an **11th-gen Core i7-1185G7** — 4 cores, no discrete GPU:

<div align="center">

| | Step | Result |
|:--:|:--|:--|
| 🪟 | **Window on screen** | **`2.6 s`** · *waits for nothing but itself* |
| 🧩 | **Parakeet model load** | `3.5 s` warm, much longer on a cold disk · *behind the open window* |
| 🗣️ | **Kokoro voice load** | `~3 s` · *after the recognizer, not competing with it* |
| 🔊 | **First word of a read** | **`1.2 s`** · *any length of text* |
| ⚡ | **Decode @ 4 threads** | **`1.9x realtime`** ✅ |
| 🐢 | **Decode @ 8 threads** | `1.1x realtime` ❌ |

</div>

> [!NOTE]
> 🧱 **What is left is the floor, not a bug.** That `3.5 s` is 2.4 GB of **full precision** encoder
> weights coming off disk. There are smaller quantized builds; this project does not use one.
> It is now spent behind an open window instead of in front of it.

> [!WARNING]
> 🧵 **More threads is slower.** Hyperthread siblings contend for the **same execution units**.
> The app derives its own thread count — roughly half the logical processors, clamped to **2–8** —
> so there is **nothing to configure** and nothing tuned to one machine.

<br>

---

## ⬇️ Download (Windows 10 and 11)

**[Download Speak Anywhere for Windows](https://github.com/nicedreamzapp/SpeakAnywhere/releases/latest/download/Speak-Anywhere-windows.zip)**

Unzip it, open the **Speak Anywhere** folder and run **Speak Anywhere.exe**. The first time, it
downloads its speech model and voices once (about **3 GB**, with a progress bar) into
`%LOCALAPPDATA%\SpeakAnywhere\models`. After that it starts in seconds and runs offline.
**Voice Picker.exe** in the same folder lets you audition voices and keep one.

If Windows shows a blue "protected your PC" box, click **More info**, then **Run anyway**.

<br>

---

## 📦 Setup from source

```bash
git clone https://github.com/nicedreamzapp/SpeakAnywhere.git
cd SpeakAnywhere
pip install -r requirements.txt
```

⬇️ The models are **not** in this repo — they're about **3 GB** together.

<details>
<summary><b>🎧 &nbsp;Download the speech recognizer</b> &nbsp;·&nbsp; <code>2.5 GB</code></summary>

<br>

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

⚠️ `encoder.onnx` references `encoder.weights` as **external data**, so both files must sit in the
**same folder**.

🎯 There are **int8** builds that load faster and use a third of the memory. This project
deliberately uses the **full-precision** export — accuracy is the entire reason for the switch, and
quantization is the first thing that erodes it.

</details>

<details>
<summary><b>🧠 &nbsp;Download the voice activity detector</b> &nbsp;·&nbsp; <code>630 KB</code></summary>

<br>

```bash
cd _resources
curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx
```

</details>

<details>
<summary><b>🗣️ &nbsp;Download the text-to-speech voices</b> &nbsp;·&nbsp; <code>350 MB</code></summary>

<br>

```bash
cd _resources
curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_0.tar.bz2
tar -xjf kokoro-multi-lang-v1_0.tar.bz2 && rm kokoro-multi-lang-v1_0.tar.bz2
```

> [!CAUTION]
> 🔢 Take **`v1_0`**, not `v1_1`. Despite the higher number, **v1.1 is the Chinese-focused
> release** — it carries **3** English voices against v1.0's **28**.

</details>

<br>

▶️ **Then run it:**

```bash
python speak_anywhere.py
```

<br>

---

## 🎛️ Using it

<div align="center">

| | Step | |
|:--:|:--|:--|
| **1️⃣** | **Launch** | the window is up in about 2 seconds |
| **2️⃣** | 🎤 **Tap the mic and talk** | tap again to stop |
| **3️⃣** | 🔊 **Copy text, tap Speak Clipboard** | hear it read back |
| **4️⃣** | 🎚️ **Open the voice picker** | keep the one you like |
| **5️⃣** | ⏩ **Adjust** | speed `0.5x`–`2.0x`, mic and speaker both selectable |

</div>

### 💬 Voice commands

<div align="center">

| Say | Get |
|:--|:--|
| 🗣️ `"new line"` | ⏎ **Enter** |
| 🗣️ `"period"` | **`.`** |
| 🗣️ `"comma"` | **`,`** |

</div>

> ✨ Parakeet emits **real punctuation on its own**, so these are mostly a holdover for when you
> want to be explicit.

<br>

---

## 📁 Project structure

```
SpeakAnywhere/
├── 📄 speak_anywhere.py            # the application
├── 🗣️ voices.py                    # voice catalog, saved choice, synthesis
├── 🎚️ voice_picker.pyw             # audition voices and pick one
├── 📋 requirements.txt
├── ⚖️ LICENSE.txt
├── 🙏 CREDITS.md
└── 📦 _resources/
    ├── 🖼️ SpeakAnywhere.ico
    ├── 🎬 splash_video.mp4
    ├── 🎵 splash_audio.mp3
    ├── 🧠 silero_vad.onnx           ⬇️ downloaded
    ├── 🎧 parakeet-tdt-0.6b-v2/     ⬇️ downloaded
    ├── 🗣️ kokoro-multi-lang-v1_0/   ⬇️ downloaded
    └── 🔈 piper/                    optional alternate voices
```

<br>

---

## 🔨 Building the download

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File build-windows.ps1
```

It builds in its own clean environment and writes `dist\Speak-Anywhere-windows.zip`: one folder
with **Speak Anywhere.exe** and **Voice Picker.exe**. The models are left out and fetched on first run.

<br>

---

## 🙏 Built on

<div align="center">

| | Project | Role |
|:--:|:--|:--|
| 🎧 | [**NVIDIA Parakeet TDT**](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2) | Speech recognition |
| 🗣️ | [**Kokoro-82M**](https://huggingface.co/hexgrad/Kokoro-82M) | Text-to-speech |
| 🧠 | [**Silero VAD**](https://github.com/snakers4/silero-vad) | Voice activity detection |
| ⚙️ | [**sherpa-onnx**](https://github.com/k2-fsa/sherpa-onnx) | Runtime for all three |
| 🔈 | [**Piper**](https://github.com/rhasspy/piper) | Alternate voices |
| 🎚️ | [**PyAudio**](https://pypi.org/project/PyAudio/) · [**sounddevice**](https://python-sounddevice.readthedocs.io/) | Audio I/O |
| ⌨️ | [**PyAutoGUI**](https://pyautogui.readthedocs.io/) | Keyboard automation |
| 🖥️ | [**Tkinter**](https://docs.python.org/3/library/tkinter.html) | Interface |
| 🎬 | [**OpenCV**](https://opencv.org/) · [**Pygame**](https://www.pygame.org/) | Splash video and audio |

</div>

Full attribution in [**CREDITS.md**](CREDITS.md).

<br>

---

<div align="center">

### ⚖️ License

Copyright © 2024 **Nice Dreamz LLC**. All Rights Reserved.
Proprietary software — see [**LICENSE.txt**](LICENSE.txt).

<br>

### 👤 Author

**Matt Macosko** · Nice Dreamz LLC
[info@nicedreamz.wholesale.com](mailto:info@nicedreamz.wholesale.com)

<br>

![Made offline](https://img.shields.io/badge/Made%20to%20run-entirely%20offline-2ea44f?style=for-the-badge)

</div>
