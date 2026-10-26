
# watch: video report

- **Source:** https://www.youtube.com/watch?v=jPPzvuDIr1w (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 02:00–02:30)
- **Focus range:** 02:00 → 02:30
- **Gemini tokens:** 4270

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "02:00",
      "seconds": 12.5,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "none"
    },
    {
      "t": "02:12",
      "seconds": 7.5,
      "shot": "collage",
      "text_motion": "kinetic",
      "camera": "static",
      "transition_in": "zoom"
    },
    {
      "t": "02:20",
      "seconds": 10.0,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "pan",
      "transition_in": "hard_cut"
    }
  ],
  "distinct_shot_types": 2,
  "distinct_transitions": 2,
  "avg_shot_seconds": 10.0,
  "reproducible_without_video_footage_pct": 100,
  "reproducibility_note": "Can be completely recreated using 2D vector illustrations, SVG animations, and CSS motion paths without any external video footage.",
  "signature_device": "Corner avatar observer holding a telescope alongside 2D vector motion graphics."
}
```
