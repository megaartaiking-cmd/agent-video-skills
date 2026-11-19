#!/usr/bin/env python3
"""clip.py — tiny offline video CLI for agent-video-skills.

Stdlib only. No dependencies, no network, no cloud.
Wraps ffmpeg / ffprobe when available, and always explains
what to do when they are missing.

Usage:
  python tools/clip.py check
  python tools/clip.py trim in.mp4 out.mp4 --start 10 --end 25
  python tools/clip.py shorts in.mp4 out.mp4 --start 30 --duration 30
  python tools/clip.py titles in.mp4 out.mp4 --text "Hello" --start 2 --end 6
  python tools/clip.py color in.mp4 out.mp4 --preset warm
  python tools/clip.py plan examples/edit-plan.json
  python tools/clip.py plan examples/edit-plan.json --run
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

PRESETS = {
    "warm": "eq=brightness=0.02:contrast=1.05:saturation=1.2",
    "cool": "eq=brightness=0.00:contrast=1.05:saturation=1.1,hue=h=10",
    "vivid": "eq=contrast=1.15:saturation=1.4",
    "bw": "hue=s=0",
    "soft": "eq=brightness=0.03:contrast=0.95:saturation=0.9",
}


def fail(msg):
    print(f"clip: error: {msg}", file=sys.stderr)
    return 2


def need_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("clip: ffmpeg not found.", file=sys.stderr)
        print("Install it, then run `python tools/clip.py check` again:", file=sys.stderr)
        print("  Windows: winget install ffmpeg  (or choco install ffmpeg)", file=sys.stderr)
        print("  macOS:   brew install ffmpeg", file=sys.stderr)
        print("  Linux:   sudo apt install ffmpeg", file=sys.stderr)
        return False
    return True


def run(cmd, dry=False):
    print(" ".join(cmd))
    if dry:
        return 0
    r = subprocess.run(cmd)
    return r.returncode


def check_in(path):
    if not os.path.isfile(path):
        print(f"clip: error: input not found: {path}", file=sys.stderr)
        return False
    return True


def cmd_check(_a):
    for tool in ("ffmpeg", "ffprobe"):
        p = shutil.which(tool)
        print(f"{tool}: {'found at ' + p if p else 'NOT FOUND'}")
        if p:
            try:
                out = subprocess.check_output([tool, "-version"], text=True, timeout=10)
                print("  " + out.splitlines()[0])
            except Exception as e:
                print(f"  could not run: {e}")
    if shutil.which("ffmpeg"):
        print("\nOK: ready to edit. Try: python tools/clip.py trim in.mp4 out.mp4 --start 10 --end 25")
        return 0
    print("\nInstall ffmpeg (see above) to enable trim / shorts / titles / color.")
    return 1


def cmd_trim(a):
    if not need_ffmpeg() or not check_in(a.input):
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(a.output)), exist_ok=True)
    if a.reencode:
        cmd = ["ffmpeg", "-y", "-ss", str(a.start), "-to", str(a.end),
               "-i", a.input, "-c:v", "libx264", "-preset", "veryfast",
               "-c:a", "aac", a.output]
    else:
        # Fast, lossless cut on keyframes. Use --reencode for frame-accurate cuts.
        cmd = ["ffmpeg", "-y", "-ss", str(a.start), "-to", str(a.end),
               "-i", a.input, "-c", "copy", a.output]
    rc = run(cmd, a.dry_run)
    if rc == 0 and not a.dry_run:
        print(f"Saved: {a.output}  ({a.start}s to {a.end}s)")
    return rc


def cmd_shorts(a):
    if not need_ffmpeg() or not check_in(a.input):
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(a.output)), exist_ok=True)
    # 9:16 vertical, 720x1280, centre-cropped. Works for Shorts / Reels / TikTok.
    vf = "crop=ih*9/16:ih,scale=720:1280"
    cmd = ["ffmpeg", "-y", "-ss", str(a.start), "-t", str(a.duration),
           "-i", a.input, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
           "-c:a", "aac", a.output]
    rc = run(cmd, a.dry_run)
    if rc == 0 and not a.dry_run:
        print(f"Saved: {a.output}  (vertical 720x1280, {a.duration}s from {a.start}s)")
    return rc


def cmd_titles(a):
    if not need_ffmpeg() or not check_in(a.input):
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(a.output)), exist_ok=True)
    text = a.text.replace("'", "").replace(":", "\\:")
    vf = (f"drawtext=text='{text}':fontsize={a.size}:fontcolor={a.color}:"
          f"x=(w-text_w)/2:y=h-120:enable='between(t,{a.start},{a.end})'")
    cmd = ["ffmpeg", "-y", "-i", a.input, "-vf", vf,
           "-c:v", "libx264", "-preset", "veryfast", "-c:a", "copy", a.output]
    rc = run(cmd, a.dry_run)
    if rc == 0 and not a.dry_run:
        print(f"Saved: {a.output}  (title '{a.text}' from {a.start}s to {a.end}s)")
    return rc


def cmd_color(a):
    if not need_ffmpeg() or not check_in(a.input):
        return 2
    if a.preset not in PRESETS:
        return fail(f"unknown preset '{a.preset}'. Choose: {', '.join(PRESETS)}")
    os.makedirs(os.path.dirname(os.path.abspath(a.output)), exist_ok=True)
    cmd = ["ffmpeg", "-y", "-i", a.input, "-vf", PRESETS[a.preset],
           "-c:v", "libx264", "-preset", "veryfast", "-c:a", "copy", a.output]
    rc = run(cmd, a.dry_run)
    if rc == 0 and not a.dry_run:
        print(f"Saved: {a.output}  (preset: {a.preset})")
    return rc


def cmd_plan(a):
    if not os.path.isfile(a.plan):
        return fail(f"plan not found: {a.plan}")
    with open(a.plan, encoding="utf-8") as f:
        plan = json.load(f)
    steps = plan.get("steps", [])
    print(f"Plan: {plan.get('name', a.plan)} — {len(steps)} step(s)")
    for i, s in enumerate(steps, 1):
        kind = s.get("op")
        print(f"\n{i}. {kind}: {s}")
        if a.run:
            # Reuse the same functions by building a fake namespace.
            ns = argparse.Namespace(dry_run=False, **{k: v for k, v in s.items() if k != "op"})
            fn = {"trim": cmd_trim, "shorts": cmd_shorts,
                  "titles": cmd_titles, "color": cmd_color}.get(kind)
            if fn is None:
                print(f"  unknown op: {kind}")
                continue
            # Fill defaults expected by each command.
            for k, v in {"start": 0, "end": 0, "duration": 30, "text": "",
                         "size": 48, "color": "white", "preset": "warm",
                         "reencode": False}.items():
                if not hasattr(ns, k):
                    setattr(ns, k, v)
            rc = fn(ns)
            if rc != 0:
                return rc
        else:
            print("   (dry run — add --run to execute)")
    if not a.run:
        print("\nDry run only. Nothing was written. Add --run to execute.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="clip", description="Tiny offline video CLI (stdlib only).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("check", help="Check ffmpeg / ffprobe are installed")
    s.set_defaults(fn=cmd_check)

    s = sub.add_parser("trim", help="Cut a clip: start to end seconds")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--start", type=float, required=True)
    s.add_argument("--end", type=float, required=True)
    s.add_argument("--reencode", action="store_true", help="Frame-accurate cut (slower)")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_trim)

    s = sub.add_parser("shorts", help="Make a vertical 9:16 Short / Reel / TikTok clip")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--start", type=float, default=0)
    s.add_argument("--duration", type=float, default=30)
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_shorts)

    s = sub.add_parser("titles", help="Burn a title onto the video for a time range")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--text", required=True)
    s.add_argument("--start", type=float, default=0)
    s.add_argument("--end", type=float, default=5)
    s.add_argument("--size", type=int, default=48)
    s.add_argument("--color", default="white")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_titles)

    s = sub.add_parser("color", help="Apply a colour preset: warm, cool, vivid, bw, soft")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--preset", default="warm", choices=list(PRESETS))
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_color)

    s = sub.add_parser("plan", help="Show (or run) an edit plan JSON file")
    s.add_argument("plan")
    s.add_argument("--run", action="store_true", help="Execute the plan steps")
    s.set_defaults(fn=cmd_plan)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
