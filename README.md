# Head Factory

A controlled collection of consistent retro-console floating-head portrait assets.

## Production target

- 2048 × 1152 PNG
- transparent alpha background
- front-facing floating head only
- no neck, shoulders, torso, clothing, text, border, shadow, or environment
- authentic PS2 / Dreamcast / GameCube-era low-poly rendering
- identical camera, framing, lighting, texture density, and scale across the collection
- subject identity is the only intentional variable

## Repository structure

- `docs/ART_BIBLE.md` — canonical visual direction
- `docs/PRODUCTION_SPEC.md` — compact generation rules
- `data/characters.json` — queue and completion index
- `data/runs.json` — generation history
- `CHANGELOG.md` — specification changes
- `assets/approved/` — approved transparent PNG files
- `assets/rejected/` — failed or duplicate outputs retained for audit

## Local workflow

After changes are made remotely:

```powershell
git pull
```

After adding approved images locally:

```powershell
git add .
git commit -m "Add approved PolyHeads assets"
git push
```
