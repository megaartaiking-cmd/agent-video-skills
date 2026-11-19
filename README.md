# agent-video-skills

> **Agent Skills that let AI coding agents edit video offline — trim, make Shorts, add titles, and colour-grade. No Premiere, no cloud, no upload. Works on low-end PCs.**

**4 skills · 1 CLI · 0 dependencies · 100% offline**

[![GitHub stars](https://img.shields.io/github/stars/megaartaiking-cmd/agent-video-skills?style=social)](https://github.com/megaartaiking-cmd/agent-video-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](tools/clip.py)

AI agents are great at code, but video editing still means Premiere, a cloud render, or a heavy app. This repo fixes that gap: a small bundle of Agent Skills (SKILL.md) plus a tiny Python CLI that wraps ffmpeg, so an agent can do the common video jobs — in the terminal, on the user's own PC.

Works with Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI, and any agent that reads SKILL.md files.

## Why this exists

The top trending repos on GitHub today (19 Nov 2026) are almost all Agent Skills — bug-hunting skills, dev-methodology skills, diagram skills, research skills. Video is the missing one. No trending skill bundle edits video, and no video editor is agent-native, offline, and light enough for an old PC.

This one is:

- **Agent-native** — skills in the open SKILL.md format, composable, one job per skill
- **Offline** — no upload, no cloud render, files never leave the PC
- **Lightweight** — stdlib-only Python, no npm install, no 150 MB Chromium
- **Low-end friendly** — fast cuts first, 480p / 720p defaults, built for the same PCs as LiteCut Pro (512 MB RAM, single-core)

## Skills

| Skill | What it does | Command |
|---|---|---|
| `video-trim` | Cut a clip to start–end seconds | `clip.py trim` |
| `video-shorts` | Make a vertical 9:16 Short / Reel / TikTok | `clip.py shorts` |
| `video-titles` | Burn a title / subtitle on screen | `clip.py titles` |
| `video-color` | Colour-grade: warm, cool, vivid, bw, soft | `clip.py color` |

Each skill lives in `skills/<name>/SKILL.md` — copy that folder into your agent's skills folder, or point your agent at this repo.

## Quick start

```sh
git clone https://github.com/megaartaiking-cmd/agent-video-skills.git
cd agent-video-skills

# 1. Check ffmpeg is installed
python tools/clip.py check

# 2. Trim a clip
python tools/clip.py trim input.mp4 clip.mp4 --start 10 --end 25

# 3. Make a Short from it
python tools/clip.py shorts input.mp4 short.mp4 --start 30 --duration 30
```

No ffmpeg yet? Install it once:

- Windows: `winget install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

## Usage

```sh
# Trim 10–25s (fast, lossless cut)
python tools/clip.py trim input.mp4 clip.mp4 --start 10 --end 25

# Frame-accurate trim (slower, re-encodes)
python tools/clip.py trim input.mp4 clip.mp4 --start 10 --end 25 --reencode

# Vertical 9:16 Short, 720x1280, 30s
python tools/clip.py shorts input.mp4 short.mp4 --start 30 --duration 30

# Title for the first 5 seconds
python tools/clip.py titles input.mp4 titled.mp4 --text "My Trip" --start 0 --end 5

# Warm colour grade
python tools/clip.py color input.mp4 graded.mp4 --preset warm

# Run an edit plan (dry run first, then --run)
python tools/clip.py plan examples/edit-plan.json
python tools/clip.py plan examples/edit-plan.json --run
```

See [examples/commands.md](examples/commands.md) for all commands, and [examples/edit-plan.json](examples/edit-plan.json) for a plan file.

## How it works

1. You (or your agent) describe the edit in plain words: "trim 10–25s, then make it warm".
2. The matching skill in `skills/` tells the agent the exact workflow, the command to run, and the rules — never overwrite the original, always write to a new file.
3. `tools/clip.py` (stdlib-only Python) runs ffmpeg locally and reports the output path.
4. Nothing is uploaded. The edit happens on your PC.

For visual editing, pair this with [LiteCut Pro](https://github.com/megaartaiking-cmd/LIGHT-CUT-VIDEO-EDITOR) — the same offline, low-end video editor, with a timeline, titles, and filters in the browser.

## Works with

- Claude Code
- Cursor
- GitHub Copilot
- Codex
- Gemini CLI
- Any agent that reads Agent Skills (SKILL.md)

Copy `skills/video-trim/` (or all of `skills/`) into your agent's skills directory, or ask your agent to read the SKILL.md files in this repo directly.

## FAQ

**Does it need the internet?**
No. After `git clone`, everything runs offline. ffmpeg runs locally.

**Does it need Premiere?**
No. It uses ffmpeg, which is free and far lighter.

**Will it run on an old PC?**
Yes — that is the point. Fast cuts avoid re-encoding, Shorts default to 720p, and there is no Electron / Chromium app to load. A 512 MB PC can run the CLI; use 480p exports if playback stutters.

**What formats?**
Input: MP4 and anything ffmpeg reads. Output: MP4 (H.264 + AAC).

**Can I add a skill?**
Yes — copy `skills/video-trim/` as a template, write a SKILL.md with a clear name, description, workflow, and rules, and open a pull request.

## Contributing

Issues and pull requests are welcome. Keep skills small, one job per skill, with a tested command in `tools/clip.py`. Please do not add dependencies — stdlib only.

## License

MIT — see [LICENSE](LICENSE).

## More Agent Skills

More offline Agent Skills by the same author — one focused skill per repo:

- [agent-audio-skills](https://github.com/megaartaiking-cmd/agent-audio-skills) — Trim podcasts, normalize volume, extract audio from video
- [agent-csv-skills](https://github.com/megaartaiking-cmd/agent-csv-skills) — Clean, filter, summarize CSVs; convert to JSON and Markdown
- [agent-json-skills](https://github.com/megaartaiking-cmd/agent-json-skills) — Validate, format, flatten, query, and diff JSON
- [agent-markdown-skills](https://github.com/megaartaiking-cmd/agent-markdown-skills) — Markdown to HTML, table of contents, link check, word count
- [agent-git-skills](https://github.com/megaartaiking-cmd/agent-git-skills) — Commit messages, changelogs, repo health, branch cleanup
- [agent-text-skills](https://github.com/megaartaiking-cmd/agent-text-skills) — Summarize text, extract keywords, readability, dedupe
- [agent-file-skills](https://github.com/megaartaiking-cmd/agent-file-skills) — Organize folders, find duplicates, batch rename
- [agent-sql-skills](https://github.com/megaartaiking-cmd/agent-sql-skills) — Explore SQLite, run queries, export to CSV
- [LiteCut Pro](https://github.com/megaartaiking-cmd/LIGHT-CUT-VIDEO-EDITOR) — lightweight offline video editor for Windows 10

---

**Keywords:** agent skills, AI agent video editing, video editing skills, Claude Code skills, Cursor skills, offline video editor, ffmpeg CLI, video Shorts maker, lightweight video editor, low-end PC video editing
