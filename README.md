# Head Factory

A controlled collection and Python production pipeline for consistent retro-console floating-head portrait assets.

## Production target

- final asset: 2048 × 1152 PNG
- true transparent alpha background
- front-facing floating head only
- no neck, shoulders, torso, clothing, text, border, shadow, or environment
- authentic PS2 / Dreamcast / GameCube-era low-poly rendering
- fixed camera, framing, lighting, texture density, and scale
- subject identity is the only intentional variable

## What the Python project does

1. Reads `data/characters.json`.
2. Selects the next pending subject while avoiding the previous category and the last 100 run IDs.
3. Builds the prompt from `docs/PRODUCTION_SPEC.md`.
4. Generates a transparent image with the OpenAI Images API.
5. Normalizes it onto an exact 2048 × 1152 transparent canvas with the visible alpha silhouette at 86% canvas height.
6. Runs deterministic technical checks.
7. Records the attempt in `data/runs.json`.
8. Waits for manual approval or rejection before changing the queue.

The Images API currently generates a supported landscape size first; Pillow then performs the exact, repeatable 2048 × 1152 framing pass.

## Windows setup

From `C:\Users\Yura\Head-Factory`:

```powershell
git pull
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
Copy-Item .env.example .env
notepad .env
```

Put your API key in `.env`:

```text
OPENAI_API_KEY=your_key_here
HEAD_FACTORY_MODEL=gpt-image-1
HEAD_FACTORY_QUALITY=high
```

Do not commit `.env`.

## Generate the next queued head

```powershell
head-factory generate
```

The candidate appears under `assets/work/`. Open it and inspect identity, neck/shoulders, transparency, framing, and style.

Approve it:

```powershell
head-factory approve "assets\work\subject_timestamp_candidate.png"
```

Reject it and return the subject to the queue:

```powershell
head-factory reject "assets\work\subject_timestamp_candidate.png" --reason "wrong identity and visible neck"
```

Approved assets are copied to `assets/approved/<subject-id>.png`. Rejected assets go to `assets/rejected/`. Both actions update `data/characters.json` and `data/runs.json`.

## Commit an approved run

```powershell
git add data assets\approved assets\rejected
git commit -m "Approve PolyHead: subject name"
git push
```

## Repository structure

- `head_factory/` — Python package and CLI
- `docs/ART_BIBLE.md` — canonical visual direction
- `docs/PRODUCTION_SPEC.md` — prompt rules consumed by the generator
- `data/characters.json` — queue and completion index
- `data/runs.json` — auditable generation history
- `assets/work/` — untracked candidates
- `assets/approved/` — approved transparent PNG assets
- `assets/rejected/` — retained failed outputs
- `CHANGELOG.md` — specification changes

## Current limitation

Technical QC can verify alpha, resolution, and normalized framing. Identity accuracy, unwanted neck anatomy, and visual style still require human review. A vision-based semantic QC stage can be added after the basic pipeline is proven stable.
