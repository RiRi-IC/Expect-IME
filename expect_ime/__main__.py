"""Command line interface for ExpectIME typo detection."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

from . import __version__
from .detector import Detection, JapaneseTypoDetector


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="expect-ime",
        description="Detect and rank Japanese typo-correction candidates.",
    )
    parser.add_argument("text", nargs="*", help="Japanese text tokens to check.")
    parser.add_argument(
        "--dictionary",
        "-d",
        action="append",
        type=Path,
        default=[],
        help="UTF-8 newline-delimited dictionary file. Can be passed multiple times.",
    )
    parser.add_argument("--limit", type=int, default=5, help="Maximum candidates per token.")
    parser.add_argument("--json", action="store_true", help="Emit JSON Lines instead of text.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    words = _load_words(args.dictionary)
    detector = JapaneseTypoDetector(words) if words else JapaneseTypoDetector()
    tokens = args.text or [line.strip() for line in sys.stdin if line.strip()]

    for token in tokens:
        detection = detector.detect(token, limit=args.limit)
        if args.json:
            print(json.dumps(_to_dict(detection), ensure_ascii=False))
        else:
            print(_format_text(detection))
    return 0


def _load_words(paths: Iterable[Path]) -> list[str]:
    words: list[str] = []
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            words.extend(line.strip() for line in handle if line.strip() and not line.startswith("#"))
    return words


def _to_dict(detection: Detection) -> dict[str, object]:
    return {
        "original": detection.original,
        "normalized": detection.normalized,
        "is_known": detection.is_known,
        "candidates": [
            {"text": candidate.text, "score": candidate.score, "reason": candidate.reason}
            for candidate in detection.candidates
        ],
    }


def _format_text(detection: Detection) -> str:
    if detection.is_known:
        return f"{detection.original}: known"
    if not detection.candidates:
        return f"{detection.original}: no candidates"
    candidates = ", ".join(
        f"{candidate.text} ({candidate.score:.2f}; {candidate.reason})"
        for candidate in detection.candidates
    )
    return f"{detection.original}: {candidates}"


if __name__ == "__main__":
    raise SystemExit(main())
