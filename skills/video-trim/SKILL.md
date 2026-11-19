---
name: video-trim
description: Cut a video to a start and end time, offline, with ffmpeg. Use when the user or agent wants to trim, cut, or extract a clip from a longer video.
---

# Video Trim

Cut a video to a time range. Fast by default, frame-accurate on request.
No cloud, no upload. Files stay local.

## When to use

- "Trim this video to 10–25 seconds"
- "Cut out the first minute"
- "Extract a clip for a Short"

## Workflow

1. Find the start and end times in seconds. Ask the user if they are unclear.
2. Check ffmpeg is installed:
   ```sh
   python tools/clip.py check
   ```
   If it is missing, tell the user how to install it (`winget install ffmpeg` on Windows, `brew install ffmpeg` on macOS, `sudo apt install ffmpeg` on Linux) and stop.
3. Trim — fast, lossless cut first:
   ```sh
   python tools/clip.py trim input.mp4 output.mp4 --start 10 --end 25
   ```
4. If the cut lands on the wrong frame, or the user needs an exact frame, re-encode:
   ```sh
   python tools/clip.py trim input.mp4 output.mp4 --start 10 --end 25 --reencode
   ```
5. Confirm the output file exists and report its path and duration. Never delete the original unless the user explicitly asks.

## Rules

- Never overwrite the input file. Always write to a new output file.
- Keep the original audio unless the user asks to remove it.
- For very low-memory PCs, prefer the fast cut (no `--reencode`) first.
- If the input is not a video file, say so and stop.
