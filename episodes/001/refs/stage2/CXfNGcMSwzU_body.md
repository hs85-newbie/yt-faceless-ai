
# watch: video report

- **Source:** https://www.youtube.com/watch?v=CXfNGcMSwzU (URL sent to Google)
- **Engine:** gemini-3.7-flash (static clip 02:00–02:30)
- **Focus range:** 02:00 → 02:30
- **Gemini tokens:** 3792

## Answer (from Gemini)

_These are Gemini's observations of the video, not frames you viewed yourself. Relay them as such; rerun with `--engine local` to inspect frames directly._

```json
{
  "cuts": [
    {
      "t": "02:00",
      "seconds": 120.0,
      "shot": "chart",
      "text_motion": "kinetic",
      "camera": "pan",
      "transition_in": "hard_cut"
    }
  ],
  "distinct_shot_types": 1,
  "distinct_transitions": 1,
  "avg_shot_seconds": 30.0,
  "reproducible_without_video_footage_pct": 100,
  "reproducibility_note": "This sequence is entirely 3D motion graphic data visualizations on a red background and can be built completely using WebGL, Three.js, or HTML/CSS 3D transforms.",
  "signature_device": "Isometric 3D bar graphs and data tables rendered in perspective across a continuous deep red dimensional surface"
}
```
