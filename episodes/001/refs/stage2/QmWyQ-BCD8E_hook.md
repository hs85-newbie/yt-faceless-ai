
# watch: video report

- **Source:** https://www.youtube.com/watch?v=QmWyQ-BCD8E (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 00:00–00:30)
- **Focus range:** 00:00 → 00:30
- **Gemini tokens:** 5144

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "0:00",
      "seconds": 0.0,
      "shot": "character_anim",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:01",
      "seconds": 0.8,
      "shot": "chart",
      "text_motion": "kinetic",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:07",
      "seconds": 6.8,
      "shot": "real_footage",
      "text_motion": "kinetic",
      "camera": "push",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:14",
      "seconds": 13.8,
      "shot": "collage",
      "text_motion": "kinetic",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:22",
      "seconds": 21.7,
      "shot": "chart",
      "text_motion": "kinetic",
      "camera": "push",
      "transition_in": "hard_cut"
    },
    {
      "t": "0:24",
      "seconds": 24.0,
      "shot": "chart",
      "text_motion": "kinetic",
      "camera": "static",
      "transition_in": "wipe"
    },
    {
      "t": "0:28",
      "seconds": 28.5,
      "shot": "chart",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "wipe"
    }
  ],
  "distinct_shot_types": 4,
  "distinct_transitions": 2,
  "avg_shot_seconds": 4.3,
  "reproducible_without_video_footage_pct": 77,
  "reproducibility_note": "Nearly everything consists of animated line charts, cutouts, and paper collages on digital boards, with only the Washington D.C. skyline shot requiring actual real-world footage.",
  "signature_device": "Green dollar-sign/question-mark avatar presenting animated FRED economic line charts mounted on physical-textured whiteboards."
}
```
