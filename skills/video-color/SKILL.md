---
name: video-color
description: Colour-grade a video with a simple preset — warm, cool, vivid, black-and-white, or soft — offline. Use when the user wants a video to look warmer, cooler, more vivid, or graded.
---

# Video Colour

Apply a simple colour preset. No manual colour theory needed.

Presets:
- `warm` — slightly brighter, warmer, more saturated
- `cool` — cooler, slightly desaturated highlights
- `vivid` — higher contrast and saturation
- `bw` — black and white
- `soft` — slightly brighter, lower contrast, muted

## When to use

- "Make this video look warmer"
- "Colour-grade this clip"
- "Turn this black and white"

## Workflow

1. Ask which preset, or pick `warm` as a safe default and say so.
2. Check ffmpeg:
   ```sh
   python tools/clip.py check
   ```
3. Apply it:
   ```sh
   python tools/clip.py color input.mp4 output.mp4 --preset warm
   ```
4. Report the output path and preset. Offer to try another preset — do not stack presets silently.

## Rules

- One preset at a time. Do not chain presets unless the user asks.
- Always write to a new file. Never overwrite the original.
- If the user wants a precise look, use the LiteCut editor's colour sliders instead and report that.
