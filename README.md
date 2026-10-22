<div align="center">

# 🎙️ Speak Anywhere

### 🗣️ Talk to any app. 🔊 Have any text read back.

**💯 Completely offline.** No API keys. No accounts. No cloud.
**Nothing ever leaves your machine.**


A Windows desktop app that types what you say into any window and reads copied text aloud,
using speech models that run on your own CPU.

**[⬇️ Download for Windows](https://github.com/nicedreamzapp/SpeakAnywhere/releases/latest/download/Speak-Anywhere-windows.zip)**
· [🔥 Before and after](#-the-big-change-vosk-is-gone) · [📈 Measured numbers](#-performance)


![Offline](https://img.shields.io/badge/100%25-OFFLINE-2ea44f?style=for-the-badge)
![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![No GPU](https://img.shields.io/badge/GPU-NOT%20REQUIRED-FF8700?style=for-the-badge)

![ASR](https://img.shields.io/badge/🎧_Recognition-Parakeet_TDT_0.6B-76B900?style=flat-square)
![TTS](https://img.shields.io/badge/🗣️_Speech-Kokoro--82M-FF6B9D?style=flat-square)
![VAD](https://img.shields.io/badge/🧠_Detection-Silero-5865F2?style=flat-square)
![Runtime](https://img.shields.io/badge/⚙️_Runtime-sherpa--onnx-24292e?style=flat-square)

</div>

<a id="s1"></a>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s01-banner-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s01-banner-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s01-banner.svg" width="100%" alt="01. What it does. Dictate, listen, stay private"></picture>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s01-r1-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s01-r1-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s01-r1.svg" width="100%" alt="Dictate. Tap the mic and talk. Your words are typed into whatever window has focus. Listen. Copy any text, tap Speak Clipboard, hear it in a natural neural voice. Stay private. Every model runs locally. After the one-time model download, nothing goes over the network."></picture>

<a id="-what-it-does"></a>
<a id="-what-i-built"></a>
## 👤 What I built

Speak Anywhere is written by **Matt Macosko**. The speech models and runtime are upstream
projects (see [Built on](#-built-on)); the app around them is this repo:

- 🎤 **Dictation pipeline**: microphone ▸ Silero VAD ▸ a decoder thread ▸ keystrokes, with nothing dropped during a decode or on stop. `dictation_loop()` in [`speak_anywhere.py`](speak_anywhere.py)
- 🔊 **Streaming clipboard reader**: growing chunks, a 3-deep render queue and one gapless output stream. `speech_chunks()` and `speak_clipboard()` in [`speak_anywhere.py`](speak_anywhere.py)
- ⏱️ **Fast startup**: the window opens while the recognizer loads in the background, and the thread count is picked per machine. `load_model()`, `asr_model()` and `_asr_threads()` in [`speak_anywhere.py`](speak_anywhere.py)
- 🗣️ **Voice catalog and synthesis** over Kokoro and Piper, with the saved choice. [`voices.py`](voices.py)
- 🎚️ **Voice picker** window. [`voice_picker.pyw`](voice_picker.pyw)
- ⬇️ **First-run model download** with a progress bar, written through `.part` files so a cut-off download is never mistaken for a finished one. [`models.py`](models.py)
- 📦 **Windows packaging**: two exes in one folder, models left out, plus a no-click build check (`SPEAKANYWHERE_SMOKE`). [`speak_anywhere.spec`](speak_anywhere.spec), [`build-windows.ps1`](build-windows.ps1)

The recognizer (NVIDIA Parakeet), voices (Kokoro-82M, Piper), speech detector (Silero VAD)
and runtime (sherpa-onnx) are not mine.

<img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s01-rule.svg" width="100%" alt="">

<a id="s2"></a>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s02-banner-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s02-banner-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s02-banner.svg" width="100%" alt="02. The big change: Vosk is gone. Before and after, measured"></picture>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s02-r1-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s02-r1-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s02-r1.svg" width="100%" alt="2.6 s time to window, was 129.5 s. 1.2 s first word of a long read, was 77 s. 2.3 GB memory, was 9.6 GB."></picture>

<a id="-the-big-change-vosk-is-gone"></a>
<a id="-and-it-got-dramatically-faster"></a>
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

<img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s02-rule.svg" width="100%" alt="">

<a id="s3"></a>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s03-banner-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s03-banner-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s03-banner.svg" width="100%" alt="03. The voice. Kokoro-82M, and how to pick one"></picture>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s03-r1-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s03-r1-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s03-r1.svg" width="100%" alt="Kokoro-82M. Runs through sherpa-onnx, which was already a dependency. Piper stays. Still available, source-only. Voice picker. Audition voices and keep one."></picture>

<a id="️-the-voice"></a>
Text-to-speech used to be **Piper** on `en_US-hfc_male-medium`. Small, fast, and **audibly
synthetic** on anything longer than a sentence.

It now runs **[Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)** through sherpa-onnx — which
was **already a dependency**, so this added **zero** new ones.

<div align="center">

| | 🔈 **Piper** | 🔊 **Kokoro-82M** |
|---:|:---:|:---:|
| 🧬 **Parameters** | ~20 M | **82 M** |
| 🎭 **Naturalness** | flat, synthetic | **markedly better** |
| ⚡ **Speed on CPU** | fast | **~1.75x realtime** |
| 📅 **Generation** | older | **current** |

</div>

Piper **stays available** rather than deleted. A few of its voices hold up fine. It is
source-only: the Windows download leaves Piper out, and its voice files are not in this repo.


### 🎚️ Picking one

```bash
python voice_picker.pyw
```

**Click a voice** ▸ hear it read a sample line ▸ **Use this voice**.
Saved to `%APPDATA%/SpeakAnywhere/voice.json`, picked up on next launch.
Until you pick one, it reads in **Michael** (`am_michael`).

> [!TIP]
> 🧹 **The list is short on purpose.** Kokoro ships **54 voices** and publishes a
> [quality grade for each](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md).
> Everything graded **C or D is excluded** — `am_adam` is a **D** — plus `af_sky` and `am_santa`,
> both trained on only **minutes** of audio.
>
> ✅ **What's left: 15 English voices at grade A or B, plus 3 Piper voices.**
> The point is to *pick* a voice, not to audition a pile of bad ones.

<img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s03-rule.svg" width="100%" alt="">

<a id="s4"></a>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s04-banner-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s04-banner-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s04-banner.svg" width="100%" alt="04. How it works. The reader and the dictation loop"></picture>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s04-r1-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s04-r1-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s04-r1.svg" width="100%" alt="Reader. Starts talking on the first sentence. Dictation. Silero decides what is speech, decoding runs off the audio thread. Nothing lost. Switching dictation off drains the queue first."></picture>

<a id="-how-the-reader-actually-works"></a>
<a id="️-how-dictation-actually-works"></a>
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

<img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s04-rule.svg" width="100%" alt="">

<a id="s5"></a>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s05-banner-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s05-banner-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s05-banner.svg" width="100%" alt="05. Performance. Measured on an 11th-gen Core i7-1185G7"></picture>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s05-r1-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s05-r1-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s05-r1.svg" width="100%" alt="2.6 s window on screen. 1.2 s first word of a read. 1.9x decode at 4 threads."></picture>

<a id="-performance"></a>
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

<img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s05-rule.svg" width="100%" alt="">

<a id="s6"></a>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s06-banner-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s06-banner-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s06-banner.svg" width="100%" alt="06. Download, setup and use. Windows installer, source setup, voice commands"></picture>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s06-r1-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s06-r1-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s06-r1.svg" width="100%" alt="Windows 10 and 11. Download the zip, unzip, run Speak Anywhere.exe. About 3 GB. One-time model download on first run, with a progress bar. Python 3.11. For setup from source."></picture>

<a id="️-download-windows-10-and-11"></a>
<a id="-setup-from-source"></a>
<a id="️-using-it"></a>
**[Download Speak Anywhere for Windows](https://github.com/nicedreamzapp/SpeakAnywhere/releases/latest/download/Speak-Anywhere-windows.zip)**

Unzip it, open the **Speak Anywhere** folder and run **Speak Anywhere.exe**. The first time, it
downloads its speech model and voices once (about **3 GB**, with a progress bar) into
`%LOCALAPPDATA%\SpeakAnywhere\models`. After that it starts in seconds and runs offline.
**Voice Picker.exe** in the same folder lets you audition voices and keep one.

If Windows shows a blue "protected your PC" box, click **More info**, then **Run anyway**.



## 📦 Setup from source

Needs **Windows 10 or 11** and **Python 3.11** (`requirements.txt` includes `pywin32` and
`winshell`). The commands below are bash, so run them in Git Bash.

```bash
git clone https://github.com/nicedreamzapp/SpeakAnywhere.git
cd SpeakAnywhere
pip install -r requirements.txt
```

⬇️ The models are **not** in this repo — they're about **3 GB** together.

The steps below fetch them by hand. If you skip them, the app downloads the same files into
`_resources` on first launch, with a progress bar ([`models.py`](models.py)).

<details>
<summary><b>🎧 &nbsp;Download the speech recognizer</b> &nbsp;·&nbsp; <code>2.5 GB</code></summary>


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


```bash
cd _resources
curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx
```

</details>

<details>
<summary><b>🗣️ &nbsp;Download the text-to-speech voices</b> &nbsp;·&nbsp; <code>350 MB</code></summary>


```bash
cd _resources
curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_0.tar.bz2
tar -xjf kokoro-multi-lang-v1_0.tar.bz2 && rm kokoro-multi-lang-v1_0.tar.bz2
```

> [!CAUTION]
> 🔢 Take **`v1_0`**, not `v1_1`. Despite the higher number, **v1.1 is the Chinese-focused
> release** — it carries **3** English voices against v1.0's **28**.

</details>


▶️ **Then run it:**

```bash
python speak_anywhere.py
```



## 🎛️ Using it

<div align="center">

| | Step | |
|:--:|:--|:--|
| **1️⃣** | **Launch** | the window is up in about 2.6 seconds once the models are on disk |
| **2️⃣** | 🎤 **Tap the mic and talk** | tap again to stop |
| **3️⃣** | 🔊 **Copy text, tap Speak Clipboard** | hear it read back |
| **4️⃣** | 🎚️ **Open the voice picker** | keep the one you like |
| **5️⃣** | ⏩ **Adjust** | speed `0.5x`, `1x`, `1.5x` or `2x`, mic and speaker both selectable |

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

<img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s06-rule.svg" width="100%" alt="">

<a id="s7"></a>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s07-banner-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s07-banner-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s07-banner.svg" width="100%" alt="07. Limits, structure, credits and license. What it does not do, where things live, who it builds on"></picture>
<picture><source media="(max-width: 610px), (min-width: 768px) and (max-width: 895px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s07-r1-m.svg"><source media="(max-width: 1149px)" srcset="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s07-r1-mid.svg"><img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s07-r1.svg" width="100%" alt="Windows only. It uses pywin32, winshell and %APPDATA%. Text lands per phrase. Not word by word. Proprietary. Copyright Nice Dreamz LLC, see LICENSE.txt."></picture>

<a id="-known-limits"></a>
<a id="-project-structure"></a>
<a id="-building-the-download"></a>
<a id="-built-on"></a>
- 🪟 **Windows only.** It uses `pywin32`, `winshell` and `%APPDATA%`; there is no Mac or Linux build.
- ⏳ **Text lands after each phrase**, not word by word (see the tradeoff above).
- 🌐 **The first run needs internet** for the one-time ~3 GB model download. Files that finished
  are kept if it is cut off; the file in progress starts over.
- 🔈 **Piper voices are source-only** and you supply the files in `_resources/piper` yourself.
- ↩️ **Saying "new line" presses Enter and drops the rest of that phrase.**
- 🛡️ **The download is not code-signed**, which is why Windows shows the "protected your PC" box.



## 📁 Project structure

```
SpeakAnywhere/
├── 📄 speak_anywhere.py            # the application
├── 🗣️ voices.py                    # voice catalog, saved choice, synthesis
├── 🎚️ voice_picker.pyw             # audition voices and pick one
├── ⬇️ models.py                    # where models live, first-run download
├── 📦 speak_anywhere.spec          # PyInstaller build of both exes
├── 🔨 build-windows.ps1            # builds the Windows zip
├── 📋 requirements.txt
├── ⚖️ LICENSE.txt
├── 🙏 CREDITS.md
└── 📦 _resources/
    ├── 🖼️ SpeakAnywhere.ico
    ├── 🖼️ splash.png
    ├── 🎬 splash_video.mp4
    ├── 🎵 splash_audio.mp3
    ├── 🧠 silero_vad.onnx           ⬇️ downloaded
    ├── 🎧 parakeet-tdt-0.6b-v2/     ⬇️ downloaded
    ├── 🗣️ kokoro-multi-lang-v1_0/   ⬇️ downloaded
    └── 🔈 piper/                    optional alternate voices
```



## 🔨 Building the download

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File build-windows.ps1
```

It builds in its own clean environment and writes `dist\Speak-Anywhere-windows.zip`: one folder
with **Speak Anywhere.exe** and **Voice Picker.exe**. The models are left out and fetched on first run.



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

[**CREDITS.md**](CREDITS.md) also credits tools earlier versions used (Vosk, edge-tts).



<div align="center">

### ⚖️ License

Copyright © 2024 **Nice Dreamz LLC**. All Rights Reserved.
Proprietary software — see [**LICENSE.txt**](LICENSE.txt).


### 👤 Author

**Matt Macosko** · Nice Dreamz LLC
[info@nicedreamzwholesale.com](mailto:info@nicedreamzwholesale.com)


![Made offline](https://img.shields.io/badge/Made%20to%20run-entirely%20offline-2ea44f?style=for-the-badge)

</div>

<img src="https://raw.githubusercontent.com/nicedreamzapp/SpeakAnywhere/main/assets/readme/s07-rule.svg" width="100%" alt="">
