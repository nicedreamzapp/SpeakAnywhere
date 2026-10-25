# Contributing

Thanks for taking a look. Speak Anywhere runs on a lot of different Windows machines, microphones
and speakers, so a clear bug report is useful even if you never send code.

## Reporting a problem

Open an [issue](https://github.com/nicedreamzapp/SpeakAnywhere/issues/new/choose). The things
that make it quick to fix:

- your Windows version, CPU and RAM
- whether you ran the Windows download or `python speak_anywhere.py` from source
- the microphone and speaker you picked in the app
- the voice you were using (Kokoro or Piper, and which one)
- what you said or copied, what you expected, and what got typed or read instead
- for a first-run download problem, how far the progress bar got

## Running it locally

Needs Windows 10 or 11 and Python 3.11. The commands are bash, so run them in Git Bash.

```bash
git clone https://github.com/nicedreamzapp/SpeakAnywhere.git
cd SpeakAnywhere
pip install -r requirements.txt
python speak_anywhere.py
```

The first launch downloads about 3 GB of models into `_resources`. The README has the commands
to fetch them by hand instead. To try voices, run `python voice_picker.pyw`.

To build the Windows zip:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File build-windows.ps1
```

## Tests

There is no automated test suite. Before sending a change, check by hand that the window opens,
dictation types into another app (including after you stop), Speak Clipboard reads a long paste
without gaps, and Stop cuts it off quickly.

## Pull requests

Small and focused is easiest to review. For big changes, open an issue first so we can talk it
through. Say which Windows machine you tested on, and include before and after timings if the
change is about speed.

Please follow the [code of conduct](CODE_OF_CONDUCT.md).
