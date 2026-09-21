"""Where the speech models live, and fetching them the first time the downloaded app runs.

The models are about 3 GB, far too big to ship inside the download, so the packaged app
fetches them once from the same places the README's setup steps use, with a progress bar,
and keeps them in %LOCALAPPDATA%\\SpeakAnywhere\\models. Run from source, nothing changes:
the models stay in _resources next to the script, set up by hand as the README says.
"""
import os
import sys
import tarfile
import time
import urllib.request

FROZEN = getattr(sys, "frozen", False)

PARAKEET = "parakeet-tdt-0.6b-v2"
KOKORO = "kokoro-multi-lang-v1_0"
_HF = "https://huggingface.co/csukuangfj/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2/resolve/main"
_SHERPA = "https://github.com/k2-fsa/sherpa-onnx/releases/download"

# (what the app needs on disk, where to get it, rough size for the progress bar)
DOWNLOADS = [
    ("silero_vad.onnx", f"{_SHERPA}/asr-models/silero_vad.onnx", 650_000),
    (f"{PARAKEET}/tokens.txt", f"{_HF}/tokens.txt", 10_000),
    (f"{PARAKEET}/decoder.onnx", f"{_HF}/decoder.onnx", 30_000_000),
    (f"{PARAKEET}/joiner.onnx", f"{_HF}/joiner.onnx", 10_000_000),
    (f"{PARAKEET}/encoder.onnx", f"{_HF}/encoder.onnx", 50_000_000),
    (f"{PARAKEET}/encoder.weights", f"{_HF}/encoder.weights", 2_400_000_000),
    # Unpacked on arrival; the folder it makes is what the app checks for.
    (f"{KOKORO}/model.onnx", f"{_SHERPA}/tts-models/{KOKORO}.tar.bz2", 350_000_000),
]


def bundle_dir():
    """The app's own small files (icon, splash video) - inside the package when frozen."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "_resources")


def models_dir():
    override = os.environ.get("SPEAKANYWHERE_MODELS")
    if override:
        return override
    if FROZEN:
        local = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
        return os.path.join(local, "SpeakAnywhere", "models")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "_resources")


def missing():
    root = models_dir()
    return [d for d in DOWNLOADS if not os.path.exists(os.path.join(root, d[0]))]


def _fetch(url, dest, on_bytes):
    """Download url to dest through a .part file, so a cut-off download is never mistaken
    for a finished one."""
    part = dest + ".part"
    req = urllib.request.Request(url, headers={"User-Agent": "SpeakAnywhere"})
    with urllib.request.urlopen(req, timeout=60) as r, open(part, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
            on_bytes(len(chunk))
    os.replace(part, dest)


def ensure(progress):
    """Fetch whatever is missing. progress(percent, text) is called as it goes."""
    todo = missing()
    if not todo:
        return
    root = models_dir()
    total = sum(d[2] for d in todo)
    done = [0]
    last = [0.0]

    def on_bytes(n):
        done[0] += n
        now = time.monotonic()
        if now - last[0] > 0.2:
            last[0] = now
            gb = done[0] / 1e9
            progress(min(99, 100 * done[0] / total),
                     f"Getting voices ready, one time: {gb:.1f} of {total / 1e9:.1f} GB")

    for rel, url, _size in todo:
        dest = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if url.endswith(".tar.bz2"):
            archive = os.path.join(root, url.rsplit("/", 1)[1])
            _fetch(url, archive, on_bytes)
            progress(99, "Unpacking the voices...")
            with tarfile.open(archive, "r:bz2") as t:
                try:
                    t.extractall(root, filter="data")
                except TypeError:  # Python before 3.11.4 has no extraction filters
                    t.extractall(root)
            os.remove(archive)
        else:
            _fetch(url, dest, on_bytes)
    progress(100, "Ready")
