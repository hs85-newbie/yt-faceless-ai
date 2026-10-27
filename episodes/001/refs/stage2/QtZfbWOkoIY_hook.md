
# watch: video report

- **Source:** https://www.youtube.com/watch?v=QtZfbWOkoIY (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 00:00–00:30)
- **Focus range:** 00:00 → 00:30
- **Gemini tokens:** 4550

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "0:00",
      "seconds": 0.0,
      "shot": "collage",
      "text_motion": "kinetic",
      "camera": "pan",
      "transition_in": "none"
    },
    {
      "t": "0:13",
      "seconds": 13.5,
      "shot": "ui_mockup",
      "text_motion": "kinetic",
      "camera": "push",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:21",
      "seconds": 21.0,
      "shot": "chart",
      "text_motion": "kinetic",
      "camera": "push",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:25",
      "seconds": 25.0,
      "shot": "real_footage",
      "text_motion": "none",
      "camera": "pan",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:27",
      "seconds": 27.0,
      "shot": "ui_mockup",
      "text_motion": "none",
      "camera": "zoom",
      "transition_in": "zoom"
    }
  ],
  "distinct_shot_types": 4,
  "distinct_transitions": 2,
  "avg_shot_seconds": 6.0,
  "reproducible_without_video_footage_pct": 85,
  "reproducibility_note": "Almost the entire sequence consists of web UI screenshots, motion graphics maps, and 2D charts, with only a brief two-second stock aerial shot of Sydney.",
  "signature_device": "Browser window UI mockups overlaid with yellow highlighter Callouts and kinetic text"
}
```
