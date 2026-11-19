# Example commands

```sh
# Check ffmpeg is ready
python tools/clip.py check

# Trim 10–25s
python tools/clip.py trim input.mp4 clip.mp4 --start 10 --end 25

# Make a 30s vertical Short from 30s in
python tools/clip.py shorts input.mp4 short.mp4 --start 30 --duration 30

# Add a title for the first 5 seconds
python tools/clip.py titles input.mp4 titled.mp4 --text "My Trip" --start 0 --end 5

# Warm colour grade
python tools/clip.py color input.mp4 graded.mp4 --preset warm

# Show an edit plan without running it
python tools/clip.py plan examples/edit-plan.json

# Run the edit plan
python tools/clip.py plan examples/edit-plan.json --run
```
