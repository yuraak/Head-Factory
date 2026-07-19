from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CHARACTERS_PATH = ROOT / "data" / "characters.json"
RUNS_PATH = ROOT / "data" / "runs.json"
SPEC_PATH = ROOT / "docs" / "PRODUCTION_SPEC.md"
WORK_DIR = ROOT / "assets" / "work"
TARGET_SIZE = (2048, 1152)
TARGET_HEAD_FRACTION = 0.86


@dataclass(frozen=True)
class Subject:
    id: str
    name: str
    category: str


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    temporary.replace(path)


def select_next_subject() -> Subject:
    characters = load_json(CHARACTERS_PATH)
    runs = load_json(RUNS_PATH).get("runs", [])
    recent_ids = {run.get("subject_id") for run in runs[-100:]}
    previous_category = runs[-1].get("category") if runs else None
    pending = [item for item in characters["subjects"] if item.get("status") == "pending" and item["id"] not in recent_ids]
    if not pending:
        raise RuntimeError("No pending subjects remain")
    alternate = [item for item in pending if item["category"] != previous_category]
    item = (alternate or pending)[0]
    return Subject(item["id"], item["name"], item["category"])


def build_prompt(subject: Subject) -> str:
    spec = SPEC_PATH.read_text(encoding="utf-8")
    return f"""Create exactly one PolyHeads production asset.

MANDATORY SUBJECT: {subject.name}
CATEGORY: {subject.category}
Do not change, substitute, or reinterpret the identity as a generic person. Preserve distinctive age, ethnicity, cranial silhouette, facial proportions, hairstyle, facial hair, scars, makeup, mask, eyewear, and identity-defining accessories.

{spec}

Return one isolated front-facing floating head on true transparent alpha. No neck, shoulders, torso, collar, clothing, pedestal, shadow, halo, gradient, vignette, text, logo, watermark, or border. Do not draw a checkerboard background.
"""


def generate_candidate() -> tuple[Subject, Path, list[str]]:
    load_dotenv(ROOT / ".env")
    subject = select_next_subject()
    model = os.getenv("HEAD_FACTORY_MODEL", "gpt-image-1")
    quality = os.getenv("HEAD_FACTORY_QUALITY", "high")
    result = OpenAI().images.generate(
        model=model,
        prompt=build_prompt(subject),
        size="1536x1024",
        quality=quality,
        background="transparent",
        output_format="png",
        n=1,
    )
    encoded = result.data[0].b64_json
    if not encoded:
        raise RuntimeError("Image API returned no image data")
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw = WORK_DIR / f"{subject.id}_{stamp}_raw.png"
    raw.write_bytes(base64.b64decode(encoded))
    candidate = normalize(raw)
    failures = technical_qc(candidate)
    record_run(subject, candidate, model, failures)
    return subject, candidate, failures


def normalize(source: Path) -> Path:
    with Image.open(source).convert("RGBA") as image:
        bbox = image.getchannel("A").getbbox()
        if bbox is None:
            raise RuntimeError("Generated image is fully transparent")
        isolated = image.crop(bbox)
        height = round(TARGET_SIZE[1] * TARGET_HEAD_FRACTION)
        scale = height / isolated.height
        width = round(isolated.width * scale)
        if width > round(TARGET_SIZE[0] * 0.92):
            scale = (TARGET_SIZE[0] * 0.92) / isolated.width
            width = round(isolated.width * scale)
            height = round(isolated.height * scale)
        isolated = isolated.resize((width, height), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", TARGET_SIZE, (0, 0, 0, 0))
        canvas.alpha_composite(isolated, ((TARGET_SIZE[0] - width) // 2, (TARGET_SIZE[1] - height) // 2))
        output = source.with_name(source.name.replace("_raw.png", "_candidate.png"))
        canvas.save(output, "PNG", optimize=True)
        return output


def technical_qc(path: Path) -> list[str]:
    failures: list[str] = []
    with Image.open(path).convert("RGBA") as image:
        if image.size != TARGET_SIZE:
            failures.append(f"wrong canvas size: {image.size}")
        alpha = image.getchannel("A")
        if alpha.getextrema() == (255, 255):
            failures.append("background is fully opaque")
        bbox = alpha.getbbox()
        if bbox is None:
            failures.append("image is fully transparent")
        else:
            fraction = (bbox[3] - bbox[1]) / TARGET_SIZE[1]
            if not 0.84 <= fraction <= 0.88:
                failures.append(f"head height fraction is {fraction:.3f}")
    return failures


def record_run(subject: Subject, candidate: Path, model: str, failures: list[str]) -> None:
    payload = load_json(RUNS_PATH)
    payload.setdefault("runs", []).append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subject_id": subject.id,
        "subject": subject.name,
        "category": subject.category,
        "model": model,
        "candidate": candidate.relative_to(ROOT).as_posix(),
        "status": "candidate" if not failures else "technical_reject",
        "technical_qc": {"passed": not failures, "failures": failures},
    })
    write_json(RUNS_PATH, payload)
