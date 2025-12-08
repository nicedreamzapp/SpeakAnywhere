"""
================================================================================
SPEAK ANYWHERE - Voice Dictation & Text-to-Speech Application
================================================================================

Copyright (c) 2024 Nice Dreamz LLC
All Rights Reserved.

Author: Matt Macosko
Contact: info@nicedreamz.wholesale.com
Company: Nice Dreamz LLC

License: Proprietary - For authorized use only.
Unauthorized copying, modification, or distribution of this software
is strictly prohibited.

Description:
    Speak Anywhere is a voice-powered productivity tool that provides:
    - Voice dictation: Speak and have your words typed automatically
    - Text-to-speech: Copy text and have it read aloud with natural voices
    - Offline speech recognition using Vosk
    - Neural text-to-speech using Microsoft Edge TTS

Requirements:
    - Windows 10/11
    - Microphone for voice input
    - Speakers/headphones for audio output

================================================================================
"""

import pyperclip
import tkinter as tk
from tkinter import Canvas
import threading
import os
import sys
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import pyautogui
import time
import pyaudio
from vosk import Model, KaldiRecognizer
import json
import cv2
import pygame
import asyncio
import edge_tts
import tempfile

# ============================================================================
# APPLICATION INFO
# ============================================================================
APP_NAME = "Speak Anywhere"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Matt Macosko"
APP_COMPANY = "Nice Dreamz LLC"
APP_EMAIL = "info@nicedreamz.wholesale.com"
APP_COPYRIGHT = "Copyright (c) 2024 Nice Dreamz LLC. All Rights Reserved."

# ============================================================================
# SETTINGS - Auto-detect paths for portability
# ============================================================================
FORCE_MICROPHONE_INDEX = None

# Get the application directory (works for both script and PyInstaller exe)
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    APP_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Resources folder (hidden from user)
RESOURCES_DIR = os.path.join(APP_DIR, "_resources")

VIDEO_FILE = os.path.join(RESOURCES_DIR, "splash_video.mp4")
MODEL_PATH = os.path.join(RESOURCES_DIR, "vosk-model-small-en-us-0.15")
# Neural voice options: en-US-GuyNeural (male), en-US-JennyNeural (female), en-US-AriaNeural (female)
NEURAL_VOICE = "en-US-GuyNeural"
# ============================================================================

# ============================================================================
# VIDEO SPLASH SCREEN WITH AUDIO
# ============================================================================
splash = tk.Tk()
splash.overrideredirect(True)
splash.attributes('-topmost', True)
splash.configure(bg='black')

# Initialize pygame mixer for audio
AUDIO_FILE = os.path.join(RESOURCES_DIR, "splash_audio.mp3")
pygame.mixer.init()
try:
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(0)  # Play once
except:
    pass

# Get video dimensions
cap = cv2.VideoCapture(VIDEO_FILE)
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 24

# Crop to square
square_size = min(video_width, video_height)
crop_x = (video_width - square_size) // 2
crop_y = (video_height - square_size) // 2
display_size = 250

# Center on screen
x = (splash.winfo_screenwidth() - display_size) // 2
y = (splash.winfo_screenheight() - display_size) // 2
splash.geometry(f"{display_size}x{display_size + 30}+{x}+{y}")

video_label = tk.Label(splash, bg='black')
video_label.pack()

loading_text = tk.Label(splash, text="Loading...", bg='black', fg='#00d4ff', font=("Segoe UI", 9))
loading_text.pack(pady=3)

# Play video once
model_loaded = [False]
video_finished = [False]

def play_video():
    ret, frame = cap.read()
    if not ret:
        video_finished[0] = True
        try:
            pygame.mixer.music.stop()
        except:
            pass
        return

    frame = frame[crop_y:crop_y+square_size, crop_x:crop_x+square_size]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (display_size, display_size))
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    if not video_finished[0]:
        splash.after(int(1000/fps), play_video)

play_video()
splash.update()

# Load model in background
model = [None]
def load_model():
    model[0] = Model(MODEL_PATH)
    model_loaded[0] = True

load_thread = threading.Thread(target=load_model, daemon=True)
load_thread.start()

# Wait for video to finish
while not video_finished[0]:
    splash.update()
    time.sleep(0.01)

cap.release()

# Wait for model if needed
if not model_loaded[0]:
    loading_text.config(text="Almost ready...")
    splash.update()
    while not model_loaded[0]:
        splash.update()
        time.sleep(0.01)

model = model[0]

# ============================================================================
# SETUP DIALOG - First run options
# ============================================================================
def show_setup_dialog():
    """Show setup dialog with options to launch, create shortcuts, etc."""
    setup = tk.Toplevel(splash)
    setup.title("Speak Anywhere Setup")
    setup.overrideredirect(True)
    setup.attributes('-topmost', True)
    setup.configure(bg='#1a1a2e')

    # Window size and position
    setup_w, setup_h = 320, 280
    x = (setup.winfo_screenwidth() - setup_w) // 2
    y = (setup.winfo_screenheight() - setup_h) // 2
    setup.geometry(f"{setup_w}x{setup_h}+{x}+{y}")

    # Title
    title = tk.Label(setup, text="Speak Anywhere", bg='#1a1a2e', fg='#00d4ff',
                     font=("Segoe UI", 16, "bold"))
    title.pack(pady=(20, 5))

    subtitle = tk.Label(setup, text="Ready to use!", bg='#1a1a2e', fg='#10b981',
                        font=("Segoe UI", 10))
    subtitle.pack(pady=(0, 15))

    # Checkbox variables
    create_desktop = tk.BooleanVar(value=True)
    create_startmenu = tk.BooleanVar(value=False)
    launch_now = tk.BooleanVar(value=True)

    # Checkboxes frame
    check_frame = tk.Frame(setup, bg='#1a1a2e')
    check_frame.pack(pady=10)

    style_opts = {'bg': '#1a1a2e', 'fg': '#ffffff', 'selectcolor': '#2d2d44',
                  'activebackground': '#1a1a2e', 'activeforeground': '#ffffff',
                  'font': ("Segoe UI", 10)}

    cb1 = tk.Checkbutton(check_frame, text="Create Desktop Shortcut",
                         variable=create_desktop, **style_opts)
    cb1.pack(anchor='w', pady=3)

    cb2 = tk.Checkbutton(check_frame, text="Add to Start Menu",
                         variable=create_startmenu, **style_opts)
    cb2.pack(anchor='w', pady=3)

    cb3 = tk.Checkbutton(check_frame, text="Launch Speak Anywhere now",
                         variable=launch_now, **style_opts)
    cb3.pack(anchor='w', pady=3)

    # Result storage
    result = {'launch': False, 'desktop': False, 'startmenu': False}

    def on_ok():
        result['launch'] = launch_now.get()
        result['desktop'] = create_desktop.get()
        result['startmenu'] = create_startmenu.get()
        setup.destroy()

    def on_cancel():
        result['launch'] = False
        setup.destroy()

    # Buttons frame
    btn_frame = tk.Frame(setup, bg='#1a1a2e')
    btn_frame.pack(pady=20)

    ok_btn = tk.Label(btn_frame, text="  OK  ", bg='#3b82f6', fg='#ffffff',
                      font=("Segoe UI", 11), cursor="hand2", padx=20, pady=6)
    ok_btn.pack(side='left', padx=10)
    ok_btn.bind("<Button-1>", lambda e: on_ok())
    ok_btn.bind("<Enter>", lambda e: ok_btn.config(bg='#2563eb'))
    ok_btn.bind("<Leave>", lambda e: ok_btn.config(bg='#3b82f6'))

    cancel_btn = tk.Label(btn_frame, text="Cancel", bg='#4b5563', fg='#ffffff',
                          font=("Segoe UI", 11), cursor="hand2", padx=15, pady=6)
    cancel_btn.pack(side='left', padx=10)
    cancel_btn.bind("<Button-1>", lambda e: on_cancel())
    cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg='#374151'))
    cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg='#4b5563'))

    # Wait for dialog to close
    setup.grab_set()
    splash.wait_window(setup)

    return result

def create_shortcuts(desktop=False, startmenu=False):
    """Create Windows shortcuts"""
    if not (desktop or startmenu):
        return

    try:
        import winshell
        from win32com.client import Dispatch

        # Get the exe path
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            exe_path = os.path.abspath(__file__)

        icon_path = os.path.join(RESOURCES_DIR, "SpeakAnywhere.ico")

        shell = Dispatch('WScript.Shell')

        if desktop:
            desktop_path = winshell.desktop()
            shortcut_path = os.path.join(desktop_path, "Speak Anywhere.lnk")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = exe_path
            shortcut.WorkingDirectory = APP_DIR
            shortcut.IconLocation = icon_path if os.path.exists(icon_path) else exe_path
            shortcut.Description = "Speak Anywhere - Voice Dictation & Text-to-Speech"
            shortcut.save()

        if startmenu:
            startmenu_path = winshell.start_menu()
            shortcut_path = os.path.join(startmenu_path, "Speak Anywhere.lnk")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = exe_path
            shortcut.WorkingDirectory = APP_DIR
            shortcut.IconLocation = icon_path if os.path.exists(icon_path) else exe_path
            shortcut.Description = "Speak Anywhere - Voice Dictation & Text-to-Speech"
            shortcut.save()
    except Exception as e:
        print(f"Could not create shortcut: {e}")

# Show setup dialog
setup_result = show_setup_dialog()

# Create shortcuts if requested
create_shortcuts(setup_result.get('desktop', False), setup_result.get('startmenu', False))

# Exit if user doesn't want to launch now
if not setup_result.get('launch', True):
    splash.destroy()
    sys.exit(0)

# ============================================================================
# SETUP
# ============================================================================
speaking_thread = None
dictation_thread = None
dictation_active = False
stream = None
is_speaking = False
stop_playback = False
last_click_time = 0
DEBOUNCE_SECONDS = 0.3
current_speed = 1.0
temp_audio_file = os.path.join(APP_DIR, "tts_temp.mp3")

pa = pyaudio.PyAudio()
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
TIMEOUT_SECONDS = 10

def find_best_microphone():
    for i in range(pa.get_device_count()):
        try:
            info = pa.get_device_info_by_index(i)
            if info.get('maxInputChannels', 0) > 0:
                name = info.get('name', '').lower()
                if 'usb' in name or 'external' in name or 'headset' in name:
                    return i
        except:
            pass
    return 0

MICROPHONE_INDEX = FORCE_MICROPHONE_INDEX if FORCE_MICROPHONE_INDEX is not None else find_best_microphone()
try:
    selected_mic_name = pa.get_device_info_by_index(MICROPHONE_INDEX)['name']
except:
    selected_mic_name = "Default"

# Get available microphones - show all real input devices
def get_input_devices():
    devices = []
    seen_names = set()
    for i in range(pa.get_device_count()):
        try:
            info = pa.get_device_info_by_index(i)
            if info.get('maxInputChannels', 0) > 0:
                name = info['name']
                name_lower = name.lower()

                # ONLY skip obvious virtual/fake devices
                skip = False
                skip_words = ['mapper', 'virtual', 'stereo mix', 'what u hear',
                             'loopback', 'voicemeeter', 'cable', 'vb-audio']
                for word in skip_words:
                    if word in name_lower:
                        skip = True
                        break
                if skip:
                    continue

                # Dedupe by simplified name
                simple = name.split('(')[0].strip().lower()[:25]
                if simple in seen_names:
                    continue
                seen_names.add(simple)

                # Clean up the display name
                display = name[:35]
                devices.append((i, display))
        except:
            pass

    # If nothing found, add system default
    if not devices:
        devices.append((0, "Default Microphone"))
    return devices

# Get available speakers - show all real output devices
def get_output_devices():
    devices = []
    seen_names = set()
    for i in range(pa.get_device_count()):
        try:
            info = pa.get_device_info_by_index(i)
            if info.get('maxOutputChannels', 0) > 0:
                name = info['name']
                name_lower = name.lower()

                # ONLY skip obvious virtual/fake devices
                skip = False
                skip_words = ['mapper', 'virtual', 'loopback', 'voicemeeter', 'cable', 'vb-audio']
                for word in skip_words:
                    if word in name_lower:
                        skip = True
                        break
                if skip:
                    continue

                # Dedupe by simplified name
                simple = name.split('(')[0].strip().lower()[:25]
                if simple in seen_names:
                    continue
                seen_names.add(simple)

                # Clean up display name
                display = name[:35]
                devices.append((i, display))
        except:
            pass

    # If nothing found, add default
    if not devices:
        devices.append((-1, "Default Speakers"))
    return devices

input_devices = get_input_devices()
output_devices = get_output_devices()

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.01

# ============================================================================
# HELPER: Create gradient/glass button images
# ============================================================================
def create_glass_button(width, height, color1, color2, radius=15):
    """Create a glossy 3D glass button"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Main gradient background
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.rectangle([radius, y, width - radius, y + 1], fill=(r, g, b, 230))

    # Rounded corners
    draw.ellipse([0, 0, radius * 2, radius * 2], fill=(*color1, 230))
    draw.ellipse([width - radius * 2, 0, width, radius * 2], fill=(*color1, 230))
    draw.ellipse([0, height - radius * 2, radius * 2, height], fill=(*color2, 230))
    draw.ellipse([width - radius * 2, height - radius * 2, width, height], fill=(*color2, 230))

    # Fill in the sides
    draw.rectangle([0, radius, radius, height - radius], fill=(*color1, 230))
    draw.rectangle([width - radius, radius, width, height - radius], fill=(*color2, 230))

    # Glass highlight on top
    highlight = Image.new('RGBA', (width - 20, height // 3), (255, 255, 255, 60))
    img.paste(highlight, (10, 5), highlight)

    return img

def create_mic_button(size, color, glow=False):
    """Create a circular mic button with glow effect"""
    padding = 20 if glow else 0
    total = size + padding * 2
    img = Image.new('RGBA', (total, total), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Glow effect
    if glow:
        for i in range(20, 0, -2):
            alpha = int(30 * (1 - i / 20))
            draw.ellipse([padding - i, padding - i, size + padding + i, size + padding + i],
                        fill=(*color, alpha))

    # Main circle with gradient
    for r in range(size // 2, 0, -1):
        ratio = r / (size // 2)
        brightness = int(255 * (0.3 + 0.7 * ratio))
        c = tuple(min(255, int(c * brightness / 255)) for c in color)
        draw.ellipse([padding + size//2 - r, padding + size//2 - r,
                     padding + size//2 + r, padding + size//2 + r], fill=(*c, 255))

    # Glass highlight
    draw.ellipse([padding + 15, padding + 10, padding + size - 25, padding + size // 2],
                fill=(255, 255, 255, 50))

    return img

# ============================================================================
# FUNCTIONS
# ============================================================================
async def generate_speech(text, output_file):
    """Generate speech using Microsoft neural voice"""
    # Adjust rate based on speed setting (default is +0%, range from -50% to +50%)
    rate_adjust = int((current_speed - 1.0) * 50)
    rate_str = f"+{rate_adjust}%" if rate_adjust >= 0 else f"{rate_adjust}%"

    communicate = edge_tts.Communicate(text, NEURAL_VOICE, rate=rate_str)
    await communicate.save(output_file)

def speak_clipboard():
    global speaking_thread, is_speaking, stop_playback

    text = pyperclip.paste().strip()
    if not text:
        return

    # If already speaking, stop first and reset
    if is_speaking or (speaking_thread and speaking_thread.is_alive()):
        stop_playback = True
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except:
            pass
        time.sleep(0.1)  # Brief pause to let thread finish

    # Reset state
    is_speaking = True
    stop_playback = False
    update_speak_button()

    def run():
        global is_speaking, stop_playback
        try:
            # Generate speech with neural voice
            asyncio.run(generate_speech(text, temp_audio_file))

            if stop_playback:
                is_speaking = False
                update_speak_button()
                return

            # Unload any previous audio first
            try:
                pygame.mixer.music.unload()
            except:
                pass

            # Play the audio
            pygame.mixer.music.load(temp_audio_file)
            pygame.mixer.music.play()

            # Wait for playback to finish or be stopped
            while pygame.mixer.music.get_busy() and not stop_playback:
                time.sleep(0.1)

            pygame.mixer.music.stop()
            try:
                pygame.mixer.music.unload()
            except:
                pass
        except Exception as e:
            print(f"Speech error: {e}")

        is_speaking = False
        update_speak_button()

    speaking_thread = threading.Thread(target=run, daemon=True)
    speaking_thread.start()

def stop_speaking():
    global speaking_thread, is_speaking, stop_playback
    stop_playback = True
    is_speaking = False
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    except:
        pass
    speaking_thread = None
    update_speak_button()

def update_speak_button():
    try:
        if is_speaking:
            # Green stop icon when speaking
            speak_label_icon.config(text="🛑", fg='#00ff88')
            speak_label.config(text="Tap to stop", fg='#ff6b6b')
        else:
            # Cyan speaker icon
            speak_label_icon.config(text="🔊", fg='#00d4ff')
            speak_label.config(text="Copy text,\ntap to read", fg='#00d4ff')
        root.update()
    except:
        pass

def dictation_loop():
    global dictation_active, stream
    try:
        stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE,
                        input=True, frames_per_buffer=CHUNK_SIZE, input_device_index=MICROPHONE_INDEX)
    except:
        dictation_active = False
        return

    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    last_speech_time = time.time()
    start_time = time.time()
    typed_words = []
    last_partial_words = []

    while dictation_active:
        try:
            if stream is None or not dictation_active or not stream.is_active():
                break
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            if not dictation_active:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if 'text' in result and result['text']:
                    text = result['text']
                    final_words = text.split()
                    new_words = final_words[len(typed_words):]
                    if new_words:
                        new_text = " ".join(new_words)
                        if "new line" in new_text.lower():
                            pyautogui.press("enter")
                        else:
                            new_text = new_text.replace(" period", ".").replace(" comma", ",")
                            pyautogui.write(new_text + " ", interval=0.005)
                    typed_words = []
                    last_partial_words = []
                    last_speech_time = time.time()
            else:
                partial_result = json.loads(recognizer.PartialResult())
                if 'partial' in partial_result and partial_result['partial']:
                    partial_words = partial_result['partial'].split()
                    if len(partial_words) > len(typed_words):
                        stable_new_words = []
                        for i, word in enumerate(partial_words[len(typed_words):], start=len(typed_words)):
                            if i < len(last_partial_words):
                                stable_new_words.append(word)
                        if stable_new_words:
                            new_text = " ".join(stable_new_words)
                            if "new line" in new_text.lower():
                                pyautogui.press("enter")
                            else:
                                new_text = new_text.replace(" period", ".").replace(" comma", ",")
                                pyautogui.write(new_text + " ", interval=0.005)
                            typed_words.extend(stable_new_words)
                    last_partial_words = partial_words
                    last_speech_time = time.time()
            if (time.time() - start_time) > 1.0 and (time.time() - last_speech_time) > TIMEOUT_SECONDS:
                break
        except:
            break

    dictation_active = False
    if stream:
        try:
            stream.stop_stream()
            stream.close()
        except:
            pass
        stream = None
    try:
        update_mic_button(False)
    except:
        pass

def toggle_dictation(event=None):
    global dictation_active, dictation_thread, stream, last_click_time, is_speaking, stop_playback
    current_time = time.time()
    if current_time - last_click_time < DEBOUNCE_SECONDS:
        return
    last_click_time = current_time

    # If speaking, stop speaking first
    if is_speaking:
        stop_playback = True
        is_speaking = False
        try:
            pygame.mixer.music.stop()
        except:
            pass
        update_speak_button()

    if not dictation_active:
        dictation_active = True
        update_mic_button(True)
        dictation_thread = threading.Thread(target=dictation_loop, daemon=True)
        dictation_thread.start()
    else:
        dictation_active = False
        update_mic_button(False)
        if stream:
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
            stream = None

def update_mic_button_early(active):
    # This is a placeholder - will be replaced after UI is built
    pass

def set_speed(val):
    global current_speed
    current_speed = float(val)
    speed_value.config(text=f"{current_speed:.1f}x")

# Drag window
drag_data = {"x": 0, "y": 0}
def start_drag(event):
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def do_drag(event):
    x = root.winfo_x() + event.x - drag_data["x"]
    y = root.winfo_y() + event.y - drag_data["y"]
    root.geometry(f"+{x}+{y}")

# ============================================================================
# MAIN WINDOW - COMPACT UI WITH ROUNDED CORNERS
# ============================================================================
splash.destroy()

root = tk.Tk()
root.title("SpeakAnywhere")
root.overrideredirect(True)
root.attributes('-topmost', True)
root.attributes('-transparentcolor', '#010101')  # For rounded corners

# Compact window size
WIN_W, WIN_H = 220, 280
root.geometry(f"{WIN_W}x{WIN_H}")

# Colors
BG_TRANSPARENT = '#010101'  # Transparent color
CARD_BG = '#1a1a2e'
GREEN_ACTIVE = '#10b981'
GRAY_INACTIVE = '#6b7280'
TEXT_PRIMARY = '#ffffff'
TEXT_SECONDARY = '#9ca3af'
ACCENT_BLUE = '#3b82f6'

root.configure(bg=BG_TRANSPARENT)

# Create rounded window background
def create_rounded_bg(width, height, radius=15):
    img = Image.new('RGBA', (width, height), (1, 1, 1, 255))  # Match transparent color
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, width-1, height-1], radius=radius,
                          fill=(26, 26, 46, 255), outline=(59, 130, 246, 150), width=1)
    return ImageTk.PhotoImage(img)

bg_img = create_rounded_bg(WIN_W, WIN_H, radius=18)
bg_label = tk.Label(root, image=bg_img, bg=BG_TRANSPARENT)
bg_label.place(x=0, y=0)
bg_label.image = bg_img

# Drag functionality
root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", do_drag)

# ===== TOP BAR (close button + status) =====
top_frame = tk.Frame(root, bg=CARD_BG)
top_frame.place(x=15, y=12, width=WIN_W-30, height=22)

# Status text (shows recording/playing)
status_label = tk.Label(top_frame, text="", fg=TEXT_SECONDARY, bg=CARD_BG, font=("Segoe UI", 8))
status_label.pack(side='left')

# Close button
close_btn = tk.Label(top_frame, text="✕", bg=CARD_BG, fg=TEXT_SECONDARY,
                     font=("Segoe UI", 11), cursor="hand2")
close_btn.pack(side='right')
close_btn.bind("<Button-1>", lambda e: root.destroy())
close_btn.bind("<Enter>", lambda e: close_btn.config(fg='#ef4444'))
close_btn.bind("<Leave>", lambda e: close_btn.config(fg=TEXT_SECONDARY))

# ===== MICROPHONE - Just a big emoji that changes color =====
mic_label = tk.Label(root, text="🎤", bg=CARD_BG, fg=GRAY_INACTIVE,
                     font=("Segoe UI", 48), cursor="hand2")
mic_label.place(relx=0.5, y=75, anchor='center')
mic_label.bind("<Button-1>", toggle_dictation)

# Instruction text under mic
instruction_label = tk.Label(root, text="Tap to dictate", bg=CARD_BG,
                             fg=TEXT_SECONDARY, font=("Segoe UI", 9))
instruction_label.place(relx=0.5, y=115, anchor='center')

# ===== DEVICE DROPDOWNS =====
from tkinter import ttk

style = ttk.Style()
style.theme_use('clam')
style.configure('Dark.TCombobox',
                fieldbackground='#2d2d44', background='#2d2d44',
                foreground='#9ca3af', arrowcolor='#9ca3af',
                bordercolor='#3b82f6', lightcolor='#2d2d44', darkcolor='#2d2d44')
style.map('Dark.TCombobox',
          fieldbackground=[('readonly', '#2d2d44')],
          selectbackground=[('readonly', '#3b82f6')],
          selectforeground=[('readonly', '#ffffff')])

# Mic dropdown
mic_names = [name for idx, name in input_devices]
mic_var = tk.StringVar(value=selected_mic_name[:25] if mic_names else "Default")
mic_combo = ttk.Combobox(root, textvariable=mic_var, values=mic_names,
                         width=24, state='readonly', style='Dark.TCombobox', font=("Segoe UI", 8))
mic_combo.place(relx=0.5, y=145, anchor='center')

def on_mic_change(event):
    global MICROPHONE_INDEX, selected_mic_name
    selected_name = mic_var.get()
    for idx, name in input_devices:
        if name == selected_name:
            MICROPHONE_INDEX = idx
            selected_mic_name = name
            break
mic_combo.bind('<<ComboboxSelected>>', on_mic_change)

# Speaker dropdown
speaker_names = [name for idx, name in output_devices]
speaker_var = tk.StringVar(value=speaker_names[0][:25] if speaker_names else "Default")
speaker_combo = ttk.Combobox(root, textvariable=speaker_var, values=speaker_names,
                             width=24, state='readonly', style='Dark.TCombobox', font=("Segoe UI", 8))
speaker_combo.place(relx=0.5, y=172, anchor='center')

def on_speaker_change(event):
    pass  # pygame uses system default
speaker_combo.bind('<<ComboboxSelected>>', on_speaker_change)

# ===== SPEAK CLIPBOARD BUTTON =====
speak_btn = tk.Label(root, text="🔊 Speak Clipboard", bg='#2d2d44', fg=TEXT_SECONDARY,
                     font=("Segoe UI", 10), cursor="hand2", padx=10, pady=4)
speak_btn.place(relx=0.5, y=210, anchor='center')
speak_btn.bind("<Button-1>", lambda e: stop_speaking() if is_speaking else speak_clipboard())
speak_btn.bind("<Enter>", lambda e: speak_btn.config(bg='#3b82f6', fg=TEXT_PRIMARY) if not is_speaking else None)
speak_btn.bind("<Leave>", lambda e: speak_btn.config(bg='#2d2d44', fg=TEXT_SECONDARY) if not is_speaking else None)

# ===== SPEED SELECTOR (under speak button) =====
speed_frame = tk.Frame(root, bg=CARD_BG)
speed_frame.place(relx=0.5, y=248, anchor='center')

speeds = [0.5, 1.0, 1.5, 2.0]
speed_buttons = []

def select_speed(spd):
    global current_speed
    current_speed = spd
    for i, btn in enumerate(speed_buttons):
        if speeds[i] == spd:
            btn.config(fg=TEXT_PRIMARY, bg=ACCENT_BLUE)
        else:
            btn.config(fg=TEXT_SECONDARY, bg='#2d2d44')

for spd in speeds:
    btn = tk.Label(speed_frame, text=f"{spd}x", bg='#2d2d44' if spd != 1.0 else ACCENT_BLUE,
                   fg=TEXT_SECONDARY if spd != 1.0 else TEXT_PRIMARY,
                   font=("Segoe UI", 8), cursor="hand2", padx=6, pady=1)
    btn.pack(side='left', padx=1)
    btn.bind("<Button-1>", lambda e, s=spd: select_speed(s))
    speed_buttons.append(btn)

# Recording timer
recording_start_time = [0]

def update_timer():
    if dictation_active:
        elapsed = int(time.time() - recording_start_time[0])
        mins = elapsed // 60
        secs = elapsed % 60
        status_label.config(text=f"● {mins:02d}:{secs:02d}", fg='#ef4444')
        root.after(1000, update_timer)

# Update functions
def update_speak_button():
    try:
        if is_speaking:
            speak_btn.config(text="🛑 Stop", bg=GREEN_ACTIVE, fg=TEXT_PRIMARY)
            status_label.config(text="Playing...", fg=GREEN_ACTIVE)
        else:
            speak_btn.config(text="🔊 Speak Clipboard", bg='#2d2d44', fg=TEXT_SECONDARY)
            if not dictation_active:
                status_label.config(text="", fg=TEXT_SECONDARY)
        root.update()
    except:
        pass

def update_mic_button(active):
    try:
        if active:
            mic_label.config(fg=GREEN_ACTIVE)
            instruction_label.config(text="Listening...", fg=GREEN_ACTIVE)
            recording_start_time[0] = time.time()
            update_timer()
        else:
            mic_label.config(fg=GRAY_INACTIVE)
            instruction_label.config(text="Tap to dictate", fg=TEXT_SECONDARY)
            status_label.config(text="", fg=TEXT_SECONDARY)
        root.update()
    except:
        pass

root.mainloop()
pa.terminate()
