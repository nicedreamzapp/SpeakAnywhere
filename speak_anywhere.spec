# -*- mode: python ; coding: utf-8 -*-
# Builds the Windows download: one folder holding Speak Anywhere.exe and Voice Picker.exe,
# sharing one copy of Python and the libraries. The speech models are NOT bundled (about
# 3 GB); the app fetches them on first run into %LOCALAPPDATA%\SpeakAnywhere\models.
#   pyinstaller --noconfirm speak_anywhere.spec   ->  dist\Speak Anywhere\
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = [], [], []
for pkg in ("sherpa_onnx", "cv2"):
    d, b, h = collect_all(pkg)
    datas += d; binaries += b; hiddenimports += h

# Only the app's own small files; models stay out of the package.
datas += [
    ("_resources/SpeakAnywhere.ico", "_resources"),
    ("_resources/splash.png", "_resources"),
    ("_resources/splash_audio.mp3", "_resources"),
    ("_resources/splash_video.mp4", "_resources"),
]
excludes = ["torch", "torchvision", "torchaudio", "tensorflow", "keras", "scipy", "pandas",
            "matplotlib", "sympy", "IPython", "jupyter", "notebook", "pytest", "vosk", "piper"]

app = Analysis(["speak_anywhere.py"], datas=datas, binaries=binaries,
               hiddenimports=hiddenimports + ["models", "voices"], excludes=excludes)
picker = Analysis(["voice_picker.pyw"], hiddenimports=["models", "voices"], excludes=excludes)

app_exe = EXE(PYZ(app.pure), app.scripts, [], exclude_binaries=True, name="Speak Anywhere",
              console=False, icon="_resources/SpeakAnywhere.ico")
picker_exe = EXE(PYZ(picker.pure), picker.scripts, [], exclude_binaries=True, name="Voice Picker",
                 console=False, icon="_resources/SpeakAnywhere.ico")

COLLECT(app_exe, app.binaries, app.datas, picker_exe, picker.binaries, picker.datas,
        name="Speak Anywhere")
