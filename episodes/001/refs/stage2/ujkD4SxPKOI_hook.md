
# watch: video report

- **Source:** https://www.youtube.com/watch?v=ujkD4SxPKOI (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 00:00–00:30)
- **Focus range:** 00:00 → 00:30
- **Gemini tokens:** 5108

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "0:00",
      "seconds": 0.0,
      "shot": "kinetic_text",
      "text_motion": "kinetic",
      "camera": "push",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:03",
      "seconds": 2.8,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "pan",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:12",
      "seconds": 11.7,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "push",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:22",
      "seconds": 21.7,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "pan",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:28",
      "seconds": 27.5,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "pan",
      "transition_in": "hard_cut"
    }
  ],
  "distinct_shot_types": 2,
  "distinct_transitions": 1,
  "avg_shot_seconds": 6.0,
  "reproducible_without_video_footage_pct": 100,
  "reproducibility_note": "The sequence consists entirely of stylized 2D vector motion graphics and character animation with glowing gradients, fully reproducible via SVG/HTML/CSS without video footage.",
  "signature_device": "Vibrant flat 2D vector illustration with high-contrast neon glows and geometric character designs."
}
```
