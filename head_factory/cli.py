from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import generate_candidate
from .review import approve, reject


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="head-factory")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("generate", help="Generate the next queued subject")

    approve_parser = sub.add_parser("approve", help="Approve a candidate PNG")
    approve_parser.add_argument("candidate", type=Path)

    reject_parser = sub.add_parser("reject", help="Reject a candidate PNG and return subject to queue")
    reject_parser.add_argument("candidate", type=Path)
    reject_parser.add_argument("--reason", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "generate":
        subject, candidate, failures = generate_candidate()
        print(f"Subject: {subject.name}")
        print(f"Candidate: {candidate}")
        if failures:
            print("Technical QC: FAIL")
            for failure in failures:
                print(f"- {failure}")
        else:
            print("Technical QC: PASS")
            print(f"Review the image, then run: head-factory approve \"{candidate}\"")
    elif args.command == "approve":
        destination = approve(args.candidate)
        print(f"Approved: {destination}")
    elif args.command == "reject":
        destination = reject(args.candidate, args.reason)
        print(f"Rejected: {destination}")


if __name__ == "__main__":
    main()
