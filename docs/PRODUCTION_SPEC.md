# PolyHeads Production Specification

Version 1.0

Use this document as the compact generation contract.

## Selection

1. Read `data/characters.json`.
2. Select the earliest `pending` subject.
3. Avoid the category used by the immediately previous approved run when another pending category exists.
4. Never select a subject marked `approved`, `generated`, `rejected_duplicate`, or `blocked`.
5. Record the chosen subject in `data/runs.json` before the next selection cycle.

## Render contract

- exactly one portrait
- 2048 × 1152, 16:9
- true transparent alpha PNG
- centered front-facing floating head
- visible silhouette height: 84–88% of canvas
- pitch 0°, yaw 0°, roll 0°
- no neck, shoulders, torso, collar, clothing, hands, body, pedestal, backdrop, shadow, gradient, vignette, text, logo, border, watermark, or effects

## Visual contract

- authentic PS2 / Dreamcast / GameCube-era low-poly asset
- approximately 1,500–3,500 triangles
- visible hard faceting
- low-resolution diffuse textures with a 256–512 px appearance
- matte materials
- no subdivision, PBR, normal maps, AO, SSS, bloom, glow, GI, cinematic lighting, painterly treatment, illustration outlines, or photorealism
- chunky solid-geometry hair
- simplified skin without pores or microdetail

## Lighting contract

- one frontal key light slightly above eye level
- one very subtle frontal fill
- no rim light or environment light

## Identity contract

Determine four to six unmistakable identity markers before rendering. Preserve unique age, silhouette, facial proportions, hair, mask, scars, makeup, eyewear, or iconic headgear. Never reuse a generic recurring face template.

## QC gate

Reject and regenerate when the output contains:

- duplicate or wrong identity
- generic recurring face
- neck, shoulders, clothing, or body
- wrong scale, crop, angle, or alignment
- opaque or fake-transparent background
- shadow, gradient, vignette, halo, or environment
- modern rendering or painterly appearance
- text, logo, border, watermark, or extra objects
- more than one head

Only accepted assets may be marked `approved` in `data/characters.json`.
