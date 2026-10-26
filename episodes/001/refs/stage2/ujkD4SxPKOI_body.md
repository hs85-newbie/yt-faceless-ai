
# watch: video report

- **Source:** https://www.youtube.com/watch?v=ujkD4SxPKOI (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 02:00–02:30)
- **Focus range:** 02:00 → 02:30
- **Gemini tokens:** 5014

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "2:00",
      "seconds": 120,
      "shot": "chart",
      "text_motion": "kinetic",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "2:04",
      "seconds": 124,
      "shot": "other",
      "text_motion": "none",
      "camera": "push",
      "transition_in": "fade"
    },
    {
      "t": "2:19",
      "seconds": 129,
      "shot": "character_anim",
      "text_motion": "kinetic",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "2:22",
      "seconds": 132,
      "shot": "character_anim",
      "text_motion": "kinetic",
      "camera": "static",
      "transition_in": "hard_cut"
    }
  ],
  "distinct_shot_types": 3,
  "distinct_transitions": 2,
  "avg_shot_seconds": 7.5,
  "reproducible_without_video_footage_pct": 100,
  "reproducibility_note": "The entire sequence consists of stylized 2D vector animations, node graphs, and UI illustrations against a dark background, fully replicable via SVG and CSS/canvas motion graphics.",
  "signature_device": "Vibrant neon-on-dark vector illustrations featuring stylized purple hands interacting with abstract computational concepts"
}
```
