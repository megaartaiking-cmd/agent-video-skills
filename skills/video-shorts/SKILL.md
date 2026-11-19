---
name: video-shorts
description: Turn a long horizontal video into a vertical 9:16 Short, Reel, or TikTok clip, offline. Use when the user wants a short vertical clip from a podcast, interview, lesson, or long video.
---

# Video Shorts

Make a vertical 9:16 clip for Shorts, Reels, and TikTok from a longer video.
Centre-cropped, 720x1280, with audio kept.

## When to use

- "Make a 30-second Short from this podcast"
- "Turn this interview into a Reel"
- "Cut a vertical clip for TikTok"

## Workflow

1. Ask which moment to use, or pick the clearest 15–60 second moment. Default is 30 seconds from the start if the user gives no time.
2. Check ffmpeg:
   ```sh
   python tools/clip.py check
   ```
3. Make the Short:
   ```sh
   python tools/clip.py shorts input.mp4 short.mp4 --start 30 --duration 30
   ```
   This crops to 9:16, scales to 720x1280, and keeps audio.
4. If the subject is off-centre, note that this version centre-crops. A custom crop is a follow-up, not a silent guess.
5. Report the output path, length, and resolution. Suggest a title and caption only if asked — do not invent a hook the user did not approve.

## Rules

- Keep Shorts to 15–60 seconds unless the user asks for longer.
- Never upscale a tiny source to 720x1280 and claim it is HD — say what the source was.
- Always write to a new file. Never overwrite the original.
- Works offline. No upload, no cloud render.
