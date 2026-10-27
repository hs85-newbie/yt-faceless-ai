
# watch: video report

- **Source:** https://www.youtube.com/watch?v=CXfNGcMSwzU (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 00:00–00:30)
- **Focus range:** 00:00 → 00:30
- **Gemini tokens:** 4971

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "0:00",
      "seconds": 0.0,
      "shot": "real_footage",
      "text_motion": "none",
      "camera": "pan",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:06",
      "seconds": 6.5,
      "shot": "real_footage",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:07",
      "seconds": 7.6,
      "shot": "real_footage",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:10",
      "seconds": 9.8,
      "shot": "map",
      "text_motion": "kinetic",
      "camera": "pan",
      "transition_in": "fade"
    },
    {
      "t": "0:22",
      "seconds": 21.8,
      "shot": "map",
      "text_motion": "kinetic",
      "camera": "pan",
      "transition_in": "hard_cut"
    }
  ],
  "distinct_shot_types": 2,
  "distinct_transitions": 2,
  "avg_shot_seconds": 6.0,
  "reproducible_without_video_footage_pct": 67,
  "reproducibility_note": "The opening historical archival footage cannot be replicated without source video clips, but the dark 3D Earth globe visualizations can be reproduced using WebGL/Three.js.",
  "signature_device": "Dark topographic 3D globe with neon green tracking labels and dotted trajectory paths"
}
```
