# Security policy

## Reporting a vulnerability

Please do not open a public issue for security problems.

Report them privately through GitHub: go to the **Security** tab of this repo and click **Report a vulnerability** ([direct link](https://github.com/nicedreamzapp/SpeakAnywhere/security/advisories/new)). Only the maintainer sees the report.

Helpful details: what you found, how to reproduce it, which release or commit, your Windows version, and whether you ran the Windows download or the source.

I aim to reply within 3 days and to ship a fix or a clear plan within 30 days, depending on severity. You will be credited in the advisory unless you ask not to be.

## Supported versions

Fixes go into the latest release on `main` and the latest Windows download on the Releases page. Please update before reporting if you are on an older version.

## What matters most here

The parts where a mistake could hurt someone:

- the first-run model download in `models.py`, which fetches about 3 GB over the internet and unpacks a `.tar.bz2` archive into the models folder
- dictation in `speak_anywhere.py`, which types into whatever window has focus and presses Enter for "new line"
- Speak Clipboard in `speak_anywhere.py`, which reads whatever is on the clipboard
- the Windows build from `speak_anywhere.spec` and `build-windows.ps1`, which is not code-signed
