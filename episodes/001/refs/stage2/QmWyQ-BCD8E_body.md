
# watch: video report

- **Source:** https://www.youtube.com/watch?v=QmWyQ-BCD8E (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 02:00–02:30)
- **Focus range:** 02:00 → 02:30
- **Gemini tokens:** 5840

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "02:00",
      "seconds": 0.9,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:01",
      "seconds": 1.2,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:02",
      "seconds": 2.3,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "pan",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:04",
      "seconds": 3.5,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:08",
      "seconds": 3.9,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:12",
      "seconds": 2.8,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:15",
      "seconds": 2.2,
      "shot": "chart",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:17",
      "seconds": 3.9,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:21",
      "seconds": 2.1,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:23",
      "seconds": 2.3,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:25",
      "seconds": 3.8,
      "shot": "real_footage",
      "text_motion": "none",
      "camera": "static",
      "transition_in": "hard_cut"
    },
    {
      "t": "02:29",
      "seconds": 1.1,
      "shot": "real_footage",
      "text_motion": "static",
      "camera": "static",
      "transition_in": "fade"
    }
  ],
  "distinct_shot_types": 2,
  "distinct_transitions": 2,
  "avg_shot_seconds": 2.5,
  "reproducible_without_video_footage_pct": 10,
  "reproducibility_note": "This sequence relies almost entirely on third-party cable news broadcast footage, press conferences, and military sea trials that cannot be replicated with HTML/CSS motion graphics alone.",
  "signature_device": "Rapid montage of televised financial news broadcasts with lower-third headline chyrons"
}
```
