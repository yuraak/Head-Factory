from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .pipeline import CHARACTERS_PATH, ROOT, RUNS_PATH, load_json, write_json


def _subject_id(candidate: Path) -> str:
    return candidate.name.split("_", 1)[0]


def _set_subject_status(subject_id: str, status: str) -> None:
    payload = load_json(CHARACTERS_PATH)
    for item in payload["subjects"]:
        if item["id"] == subject_id:
            item["status"] = status
            break
    else:
        raise KeyError(f"Unknown subject id: {subject_id}")
    payload["updated_at"] = datetime.now(timezone.utc).date().isoformat()
    write_json(CHARACTERS_PATH, payload)


def _update_run(candidate: Path, status: str, asset: Path, reason: str | None = None) -> None:
    payload = load_json(RUNS_PATH)
    relative_candidate = candidate.resolve().relative_to(ROOT).as_posix()
    for run in reversed(payload.get("runs", [])):
        if run.get("candidate") == relative_candidate:
            run["status"] = status
            run["asset"] = asset.resolve().relative_to(ROOT).as_posix()
            if reason:
                run["reason"] = reason
            break
    write_json(RUNS_PATH, payload)


def approve(candidate: Path) -> Path:
    candidate = candidate.resolve()
    subject_id = _subject_id(candidate)
    destination = ROOT / "assets" / "approved" / f"{subject_id}.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(candidate.read_bytes())
    _set_subject_status(subject_id, "approved")
    _update_run(candidate, "approved", destination)
    return destination


def reject(candidate: Path, reason: str) -> Path:
    candidate = candidate.resolve()
    subject_id = _subject_id(candidate)
    destination = ROOT / "assets" / "rejected" / candidate.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(candidate.read_bytes())
    _set_subject_status(subject_id, "pending")
    _update_run(candidate, "rejected", destination, reason)
    return destination
