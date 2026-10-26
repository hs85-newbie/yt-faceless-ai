
# watch: video report

- **Source:** https://www.youtube.com/watch?v=zxVoCw3P1Gc (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 02:00–02:30)
- **Focus range:** 02:00 → 02:30
- **Gemini tokens:** 5379

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "02:00",
      "seconds": 120,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:02",
      "seconds": 122,
      "shot": "character_anim",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:06",
      "seconds": 126,
      "shot": "character_anim",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:09",
      "seconds": 129,
      "shot": "character_anim",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:17",
      "seconds": 137,
      "shot": "character_anim",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:20",
      "seconds": 140,
      "shot": "character_anim",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:27",
      "seconds": 147,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    }
  ],
  "distinct_shot_types": 1,
  "distinct_transitions": 1,
  "avg_shot_seconds": 4.3,
  "reproducible_without_video_footage_pct": 100,
  "reproducibility_note": "The sequence consists entirely of 2D vector character animations and graphic icons on a paper-textured background, easily reproduced using SVG and CSS animation.",
  "signature_device": "Stylized 2D teal-and-white line-art character animation set against a textured parchment background."
}
```
