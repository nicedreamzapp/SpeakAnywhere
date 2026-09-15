"""Voice catalog, saved selection, and synthesis - shared by the app and the picker.

Two engines live behind one call. Kokoro-82M (via sherpa-onnx) is the default:
newer than Piper, markedly more natural, and only 82M parameters. Piper is kept
because some of its voices hold up well and there is no reason to throw them out.

The Kokoro catalog is deliberately not the full 54 voices. Kokoro publishes a
quality grade per voice in its VOICES.md, and anything graded C or D is audibly
worse - am_adam is a D. Two more (af_sky, am_santa) are marked as trained on
only minutes of audio. All of those are left out so the picker is a short list
of voices worth hearing rather than a pile to sift through.
"""
import json
import os
import wave

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_resources")
KOKORO_DIR = os.path.join(RESOURCES_DIR, "kokoro-multi-lang-v1_0")
PIPER_DIR = os.path.join(RESOURCES_DIR, "piper")

CONFIG_PATH = os.path.join(
    os.environ.get("APPDATA", os.path.expanduser("~")), "SpeakAnywhere", "voice.json"
)

# Speaker ids are the model's own, read from its metadata - not a guess at
# alphabetical order. Grades are from Kokoro's published VOICES.md.
KOKORO_VOICES = [
    (3,  "af_heart",    "Heart",     "American female", "default voice"),
    (2,  "af_bella",    "Bella",     "American female", "grade A"),
    (6,  "af_nicole",   "Nicole",    "American female", "grade B"),
    (1,  "af_aoede",    "Aoede",     "American female", "grade B"),
    (5,  "af_kore",     "Kore",      "American female", "grade B"),
    (9,  "af_sarah",    "Sarah",     "American female", "grade B"),
    (7,  "af_nova",     "Nova",      "American female", "grade B"),
    (0,  "af_alloy",    "Alloy",     "American female", "grade B"),
    (16, "am_michael",  "Michael",   "American male",   "grade B"),
    (14, "am_fenrir",   "Fenrir",    "American male",   "grade B"),
    (18, "am_puck",     "Puck",      "American male",   "grade B"),
    (21, "bf_emma",     "Emma",      "British female",  "grade B"),
    (22, "bf_isabella", "Isabella",  "British female",  "grade B"),
    (26, "bm_george",   "George",    "British male",    "grade B"),
    (25, "bm_fable",    "Fable",     "British male",    "grade B"),
]

# Only the Piper voices that actually sound decent. The rest of the files in
# _resources/piper are left on disk but kept out of the menu.
PIPER_VOICES = [
    ("en_US-hfc_male-medium.onnx",   "HFC Male",    "American male",   "Piper"),
    ("en_US-hfc_female-medium.onnx", "HFC Female",  "American female", "Piper"),
    ("en_US-libritts_r-medium.onnx", "LibriTTS R",  "American",        "Piper"),
]

DEFAULT_CHOICE = {"engine": "kokoro", "id": 16, "name": "am_michael"}


def catalog():
    """Everything the picker should offer, best first."""
    items = []
    for sid, name, label, who, note in KOKORO_VOICES:
        items.append({
            "engine": "kokoro", "id": sid, "name": name,
            "label": f"{label} - {who}", "note": f"Kokoro, {note}",
        })
    for fname, label, who, note in PIPER_VOICES:
        if os.path.exists(os.path.join(PIPER_DIR, fname)):
            items.append({
                "engine": "piper", "file": fname, "name": fname.replace(".onnx", ""),
                "label": f"{label} - {who}", "note": note,
            })
    return items


def load_choice():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            choice = json.load(f)
        if choice.get("engine") in ("kokoro", "piper"):
            return choice
    except Exception:
        pass
    return dict(DEFAULT_CHOICE)


def save_choice(choice):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(choice, f, indent=2)


# --------------------------------------------------------------------------
# Engines, built on first use and then cached. Kokoro is one model for every
# voice, so it is loaded once no matter how many voices get auditioned; Piper
# needs a separate model file per voice.
# --------------------------------------------------------------------------
_kokoro = [None]
_piper_cache = {}


def _kokoro_engine(num_threads=None):
    if _kokoro[0] is None:
        import sherpa_onnx
        if num_threads is None:
            num_threads = max(2, min(8, (os.cpu_count() or 4) // 2))
        _kokoro[0] = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                    model=os.path.join(KOKORO_DIR, "model.onnx"),
                    voices=os.path.join(KOKORO_DIR, "voices.bin"),
                    tokens=os.path.join(KOKORO_DIR, "tokens.txt"),
                    data_dir=os.path.join(KOKORO_DIR, "espeak-ng-data"),
                    dict_dir=os.path.join(KOKORO_DIR, "dict"),
                    lexicon=os.path.join(KOKORO_DIR, "lexicon-us-en.txt") + ","
                            + os.path.join(KOKORO_DIR, "lexicon-zh.txt"),
                ),
                num_threads=num_threads,
                provider="cpu",
            ),
            max_num_sentences=1,
        ))
    return _kokoro[0]


def _piper_engine(fname):
    if fname not in _piper_cache:
        from piper import PiperVoice
        _piper_cache[fname] = PiperVoice.load(os.path.join(PIPER_DIR, fname))
    return _piper_cache[fname]


def synthesize(text, choice=None, speed=1.0):
    """Render text with the chosen voice. Returns (int16 bytes, sample_rate).

    Kokoro takes a real speed parameter, so timing changes without shifting
    pitch. Piper has no such control, so speed there is still what it always
    was in this app: playing the audio back at an altered sample rate.
    """
    choice = choice or load_choice()

    if choice.get("engine") == "piper":
        voice = _piper_engine(choice["file"])
        audio = b""
        rate = None
        for chunk in voice.synthesize(text):
            audio += chunk.audio_int16_bytes
            rate = chunk.sample_rate
        return audio, int(rate * speed)

    import numpy as np
    out = _kokoro_engine().generate(text, sid=int(choice.get("id", 16)), speed=float(speed))
    pcm = np.clip(np.array(out.samples) * 32767, -32768, 32767).astype("<i2")
    return pcm.tobytes(), out.sample_rate


def write_wav(path, pcm_bytes, sample_rate):
    with wave.open(path, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(pcm_bytes)
