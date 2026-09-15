"""Audition the voices and pick one. Writes the choice Speak Anywhere reads."""
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sounddevice as sd
import voices

SAMPLE_LINE = ("Hey Matt. Divine Tribe order two zero five nine one two "
               "shipped this morning, and the tracking is in your inbox.")

BG = "#1a1a2e"
PANEL = "#2d2d44"
ACCENT = "#00d4ff"
TEXT = "#e8e8f0"
MUTED = "#9ca3af"

root = tk.Tk()
root.title("Speak Anywhere - Voices")
root.configure(bg=BG)
root.geometry("560x620")
try:
    root.iconbitmap(os.path.join(voices.RESOURCES_DIR, "SpeakAnywhere.ico"))
except Exception:
    pass

tk.Label(root, text="Pick a voice", bg=BG, fg=ACCENT,
         font=("Segoe UI", 18, "bold")).pack(pady=(18, 2))
tk.Label(root, text="Click one to hear it. The weak Kokoro voices are already filtered out.",
         bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(pady=(0, 12))

items = voices.catalog()
current = voices.load_choice()


def is_current(item, choice):
    if item["engine"] != choice.get("engine"):
        return False
    if item["engine"] == "kokoro":
        return item["id"] == choice.get("id")
    return item["file"] == choice.get("file")


list_frame = tk.Frame(root, bg=BG)
list_frame.pack(fill="both", expand=True, padx=18)

canvas = tk.Canvas(list_frame, bg=BG, highlightthickness=0)
scroll = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
inner = tk.Frame(canvas, bg=BG)
inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=inner, anchor="nw", width=500)
canvas.configure(yscrollcommand=scroll.set)
canvas.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))

selected = [next((i for i, it in enumerate(items) if is_current(it, current)), 0)]
rows = []
status = tk.StringVar(value="")
busy = [False]


def paint():
    for i, (frame, name_lbl, note_lbl) in enumerate(rows):
        on = i == selected[0]
        frame.configure(bg=ACCENT if on else PANEL)
        name_lbl.configure(bg=ACCENT if on else PANEL, fg="#10101c" if on else TEXT)
        note_lbl.configure(bg=ACCENT if on else PANEL, fg="#10101c" if on else MUTED)


def play(index):
    if busy[0]:
        return
    busy[0] = True
    selected[0] = index
    paint()
    item = items[index]
    status.set(f"synthesising {item['label'].split(' - ')[0]}...")

    def work():
        try:
            pcm, rate = voices.synthesize(SAMPLE_LINE, choice=item)
            arr = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768.0
            status.set(f"playing {item['label'].split(' - ')[0]}")
            sd.stop()
            sd.play(arr, samplerate=rate)
            sd.wait()
            status.set("")
        except Exception as e:
            status.set(f"failed: {e}")
        finally:
            busy[0] = False

    threading.Thread(target=work, daemon=True).start()


for i, item in enumerate(items):
    row = tk.Frame(inner, bg=PANEL, cursor="hand2")
    row.pack(fill="x", pady=3)
    name = tk.Label(row, text=item["label"], bg=PANEL, fg=TEXT,
                    font=("Segoe UI", 11), anchor="w", padx=12, pady=2)
    name.pack(fill="x")
    note = tk.Label(row, text=item["note"], bg=PANEL, fg=MUTED,
                    font=("Segoe UI", 8), anchor="w", padx=12)
    note.pack(fill="x", pady=(0, 4))
    for w in (row, name, note):
        w.bind("<Button-1>", lambda e, idx=i: play(idx))
    rows.append((row, name, note))

paint()

tk.Label(root, textvariable=status, bg=BG, fg=ACCENT,
         font=("Segoe UI", 9)).pack(pady=(8, 0))

saved = tk.StringVar(value="")


def use_it():
    item = items[selected[0]]
    choice = {"engine": item["engine"], "name": item["name"]}
    if item["engine"] == "kokoro":
        choice["id"] = item["id"]
    else:
        choice["file"] = item["file"]
    voices.save_choice(choice)
    saved.set(f"Saved. Restart Speak Anywhere to use {item['label'].split(' - ')[0]}.")


btn = tk.Label(root, text="Use this voice", bg=ACCENT, fg="#10101c",
               font=("Segoe UI", 11, "bold"), padx=18, pady=7, cursor="hand2")
btn.pack(pady=10)
btn.bind("<Button-1>", lambda e: use_it())

tk.Label(root, textvariable=saved, bg=BG, fg="#7ee787",
         font=("Segoe UI", 9)).pack(pady=(0, 12))

root.mainloop()
