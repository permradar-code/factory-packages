# Visuals brief: "This Building Is Walking" (Strange But Real, Short ~12 s)

**Project id:** `sbr_walking_building_v1`.
**Deliver as an orphan branch** `pkg/sbr_walking_building_v1` in `permradar-code/factory-packages`, in the same format as `pkg/nitm_f106_flow_v1` (see "Package format" at the end).

**Your job is ONLY the visuals.** The montage chat does the voice, captions, music and editing.

**Report** in README.md: the Flow credits spent, and what was regenerated and why.

## How to generate

1. **Still images go in ChatGPT or Gemini, not Flow.** Flow has a daily image limit (~60).
   - Gemini needs the VPN on.
2. **Video goes in Google Flow:** Frames to Video, 9:16, 720p.
   - Model: the same one used for F-106 / Corinth (Omni Flash or Veo 3.1 Fast).
   - Generate one at a time, no batches.
3. Generate 2 variants only for the HOOK clip (A). Make one of everything else; regenerate only on a defect.
4. **Audio from Flow does not matter.** We replace it.

## The real story (for accuracy, do not put on screen)

- **Building:** Lagena Primary School, Shanghai, built 1935, about 7,600 tonnes.
- **The move:** In October 2020 engineers cut it from its foundation and lifted it on 198 hydraulic supports. They "walked" it 62 m and rotated it 21° in 18 days.
- **How it walks:** The supports work in two groups. One group holds the building, the other lifts, moves a step forward and sets down, then they swap.
- **Why:** To make room for a new commercial centre.

The real footage is slow. Our clips are a sped-up, time-lapse-style depiction. Keep everything physically plausible: **no fantasy creature legs and no humanoid robot legs.** The legs are industrial hydraulic jacks.

## Locks (paste into every prompt that shows these things)

**BUILDING LOCK:**
> a 1935 five-storey modernist school building with an irregular L-shaped plan, off-white / light grey stucco walls, rows of simple rectangular windows with dark frames, a flat roof, patches of dried brown climbing ivy on the side walls, weathered and old. No signs, no banners, no readable text.

**LEGS LOCK:**
> the whole building is cut free from its foundation and lifted about one metre off the ground on a dense grid of thick grey concrete beams, standing on hundreds of bright RED industrial hydraulic jacks with BLUE steel feet arranged in neat rows; clear daylight is visible through the gap under the building.

**SITE LOCK:**
> a flat cleared concrete construction site in central Shanghai, yellow tower cranes, yellow site fences, modern glass skyscrapers close behind, bright slightly overcast daylight, photorealistic, documentary drone/handheld photo look, vertical 9:16, no text, no watermark.

**Reject:**
- more than 5 floors;
- legs that look like animal or human legs;
- the building not lifted (no daylight gap);
- garbled text or Chinese characters anywhere;
- legs that are not red.

---

## Shots

### A. HOOK (CLIP, 6 s, 2 variants): the most important shot

The first frame must read in half a second as "a whole building is standing on legs and moving".

- **A_first (image):** low ground-level 3/4 view from near one corner.
  - The old building fills the middle 60% of the frame; the gap with the red jacks spans the bottom third.
  - Two construction workers in orange vests and white hard hats stand next to the jacks, tiny, for scale.
  - Keep the top ~20% of the frame plain sky / skyscrapers (captions go there).
  - Use BUILDING LOCK + LEGS LOCK + SITE LOCK.
- **Video prompt:**
  > Time-lapse style. The rows of red hydraulic jacks under the building work in two alternating groups: one group lifts slightly, shifts forward and sets down while the other holds the building, then they swap — a steady stepping rhythm like a centipede. The whole five-storey building visibly glides forward toward the camera-left side, slowly but clearly, perfectly level and rigid, nothing cracks or bends. The workers step aside. Clouds move fast in the sky (time-lapse). Static tripod camera. No text.
- **Must:** the building moves from frame 1; it stays rigid and level; it keeps 5 floors.

### B. BEFORE (IMG): the start of the "rewind"

- Same building, same angle as A_first, but standing normally ON the ground with no gap and no jacks.
- Excavators and yellow cranes all around, new skyscrapers towering right behind it: "it's in the way".
- Use BUILDING LOCK + SITE LOCK.

### C. THE ROUTE (CLIP, 6 s): drone top-down

- **C_first (image):** high drone shot looking straight down.
  - The L-shaped flat roof of the building sits on a cleared concrete site.
  - A long rectangle of fresh concrete runway (the path) stretches from the building toward the upper-right.
  - Yellow cranes, site huts, surrounding city blocks and skyscraper rooftops around it.
- **C_last (image):** identical drone shot, but the building is rotated about 21° clockwise and has moved along the runway to its far end (about a building-length further).
- **Video prompt:**
  > Time-lapse from a static drone looking straight down: the whole building slowly slides along the concrete runway and turns about 21 degrees as it goes, perfectly rigid. Shadows of cranes sweep across the ground, tiny workers and trucks move fast around it. No text.

### D. THE LEGS (CLIP, 4 s): close-up

- **D_first (image):** very low camera at ground level looking down a long row of the red hydraulic jacks with blue feet under the concrete beams of the building.
  - Daylight at the far end of the row; a worker's legs and boots in the background for scale.
  - Use LEGS LOCK.
- **Video prompt:**
  > The jacks alternate: every second jack retracts its foot, lifts off the ground, moves forward a short step and plants down again, while the others hold the weight; then they swap. Smooth, mechanical, slightly sped up. Hydraulic hiss. Camera static. No text.

### E. ARRIVED (IMG)

- Wide drone shot from the side and above: the old building at its new spot, back on the ground, tiny and old among gleaming new glass towers, golden late-afternoon light.
- Use BUILDING LOCK + SITE LOCK.

---

## Package format

```
visuals/video/A_hook_v1.mp4, A_hook_v2.mp4, C_route.mp4, D_legs.mp4
visuals/images/A_first.png, B_before.png, C_first.png, C_last.png, D_first.png, E_arrived.png
manifest.json
README.md
```

**manifest.json** (see below):
- `scenes[]` in the order A, B, C, D, E, each with `shot_id`, `video` or `image`, and a `note`;
- `voice` / `words` / `music` = null;
- `montage_ready` = false.

```json
{"project_id":"sbr_walking_building_v1","scenes":[{"shot_id":"A","video":"visuals/video/A_hook_v1.mp4","image":"visuals/images/A_first.png","note":"..."}],"voice":null,"words":null,"music":null,"montage_ready":false}
```

**README.md:**
- what was generated, in which tool;
- what failed and was regenerated;
- **Flow credits spent.**

**Check every frame against the locks before delivering:**
- 5 floors;
- red jacks;
- a visible gap under the building;
- no text.
