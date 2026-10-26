
# watch: video report

- **Source:** https://www.youtube.com/watch?v=jPPzvuDIr1w (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 00:00–00:30)
- **Focus range:** 00:00 → 00:30
- **Gemini tokens:** 6107

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "0:00",
      "seconds": 0.0,
      "shot": "collage",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:03",
      "seconds": 2.8,
      "shot": "collage",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "wipe"
    },
    {
      "t": "0:09",
      "seconds": 8.8,
      "shot": "collage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "other"
    },
    {
      "t": "0:13",
      "seconds": 12.6,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "other"
    },
    {
      "t": "0:15",
      "seconds": 15.5,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "pan",
      "transition_in": "other"
    },
    {
      "t": "0:18",
      "seconds": 17.8,
      "shot": "chart",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "other"
    },
    {
      "t": "0:20",
      "seconds": 20.5,
      "shot": "collage",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "other"
    },
    {
      "t": "0:23",
      "seconds": 22.8,
      "shot": "character_anim",
      "text_motion": "kinetic",
      "camera": "zoom",
      "transition_in": "zoom"
    }
  ],
  "distinct_shot_types": 3,
  "distinct_transitions": 4,
  "avg_shot_seconds": 3.8,
  "reproducible_without_video_footage_pct": 100,
  "reproducibility_note": "The entire sequence consists of flat 2D vector illustrations, animated assets, charts, and image cutouts composited with motion graphics.",
  "signature_device": "Circular avatar in the lower-left corner sipping from a mug alongside clean 2D vector motion graphics."
}
```
