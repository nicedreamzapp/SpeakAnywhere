# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# Find vosk package location for DLLs
import vosk
vosk_path = os.path.dirname(vosk.__file__)

# Find piper package location
import piper
piper_path = os.path.dirname(piper.__file__)

a = Analysis(
    ['speak_anywhere.py'],
    pathex=[],
    binaries=[
        # Vosk DLLs - required for speech recognition
        (os.path.join(vosk_path, 'libvosk.dll'), 'vosk'),
        (os.path.join(vosk_path, 'libgcc_s_seh-1.dll'), 'vosk'),
        (os.path.join(vosk_path, 'libstdc++-6.dll'), 'vosk'),
        (os.path.join(vosk_path, 'libwinpthread-1.dll'), 'vosk'),
    ],
    datas=[
        ('_resources', '_resources'),
        # Include vosk python files
        (vosk_path, 'vosk'),
    ],
    hiddenimports=[
        'piper',
        'piper.voice',
        'onnxruntime',
        'numpy',
        'sounddevice',
        'vosk',
        'pyaudio',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.ImageDraw',
        'PIL.ImageFilter',
        'cv2',
        'pygame',
        'pygame.mixer',
        'pyperclip',
        'pyautogui',
        'winshell',
        'win32com',
        'win32com.client',
        'cffi',
        'vosk.vosk_cffi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy ML frameworks not needed by the app
        'torch',
        'torchvision',
        'torchaudio',
        'tensorflow',
        'keras',
        'scipy',
        'pandas',
        'matplotlib',
        'sympy',
        'h5py',
        'imageio',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'sphinx',
        'docutils',
        'lxml',
        'coremltools',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='speak_anywhere',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='_resources/SpeakAnywhere.ico',
)
