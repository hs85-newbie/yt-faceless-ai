
# watch: video report

- **Source:** https://www.youtube.com/watch?v=QtZfbWOkoIY (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 02:00–02:30)
- **Focus range:** 02:00 → 02:30
- **Gemini tokens:** 4103

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "02:00",
      "seconds": 2.0,
      "shot": "collage",
      "text_motion": "kinetic",
      "camera": "pan",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:02",
      "seconds": 4.0,
      "shot": "real_footage",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "fade"
    },
    {
      "t": "02:06",
      "seconds": 3.0,
      "shot": "real_footage",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "fade"
    },
    {
      "t": "02:09",
      "seconds": 4.0,
      "shot": "real_footage",
      "text_motion": "none",
      "camera": "push",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:13",
      "seconds": 3.0,
      "shot": "real_footage",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:16",
      "seconds": 3.0,
      "shot": "real_footage",
      "text_motion": "none",
      "camera": "pan",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:19",
      "seconds": 5.0,
      "shot": "kinetic_text",
      "text_motion": "kinetic",
      "camera": "zoom",
      "transition_in": "fade"
    },
    {
      "t": "02:24",
      "seconds": 5.0,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "fade"
    },
    {
      "t": "02:29",
      "seconds": 1.0,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    }
  ],
  "distinct_shot_types": 3,
  "distinct_transitions": 2,
  "avg_shot_seconds": 3.33,
  "reproducible_without_video_footage_pct": 20,
  "reproducibility_note": "This section is predominantly live-action B-roll and sponsor storytelling footage, which cannot be accurately replicated using only code, charts, and still images.",
  "signature_device": "Torn crinkled paper card overlays highlighting chapter questions and themes"
}
```
