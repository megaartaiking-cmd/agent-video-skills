---
name: video-titles
description: Burn a title or subtitle onto a video for a time range, offline. Use when the user wants text on screen — a title, a name, or a caption.
---

# Video Titles

Burn text onto a video for a chosen time range. The text is part of the
video afterwards, so it works in any player.

## When to use

- "Add the title 'My Trip' for the first 5 seconds"
- "Put subtitles on this clip"
- "Add a name caption at 10 seconds"

## Workflow

1. Get the exact text, start, and end times. Use the user's exact wording — do not rewrite it.
2. Check ffmpeg:
   ```sh
   python tools/clip.py check
   ```
3. Add the title:
   ```sh
   python tools/clip.py titles input.mp4 output.mp4 --text "My Trip" --start 0 --end 5
   ```
   Optional: `--size 48` (default), `--color white`.
4. Report the output path and the time range. If the text is long, suggest splitting it into two shorter titles instead of shrinking it silently.

## Rules

- Keep titles short — one line if possible, two at most.
- Do not add text the user did not ask for.
- Always write to a new file. Never overwrite the original.
- If ffmpeg's font is missing on the PC, say so and suggest using the LiteCut editor (LiteCutPro.html) to add titles visually instead.
