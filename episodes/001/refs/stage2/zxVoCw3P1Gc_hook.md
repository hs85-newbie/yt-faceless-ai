
# watch: video report

- **Source:** https://www.youtube.com/watch?v=zxVoCw3P1Gc (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 00:00–00:30)
- **Focus range:** 00:00 → 00:30
- **Gemini tokens:** 5930

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "0:00",
      "seconds": 0,
      "shot": "character_anim",
      "text_motion": "kinetic",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:08",
      "seconds": 8,
      "shot": "other",
      "text_motion": "kinetic",
      "camera": "zoom",
      "transition_in": "zoom"
    },
    {
      "t": "0:11",
      "seconds": 11,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:16",
      "seconds": 16,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:21",
      "seconds": 21,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:23",
      "seconds": 23,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:27",
      "seconds": 27,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:28",
      "seconds": 28,
      "shot": "chart",
      "text_motion": "kinetic",
      "camera": "static",
      "transition_in": "hard_cut"
    }
  ],
  "distinct_shot_types": 3,
  "distinct_transitions": 2,
  "avg_shot_seconds": 3.75,
  "reproducible_without_video_footage_pct": 100,
  "reproducibility_note": "The entire video consists of minimalist 2D vector animations, icons, and typography that can be reproduced purely via SVG and CSS/HTML animations without external footage.",
  "signature_device": "minimalist dark green stick figure character on an off-white textured background"
}
```
