"""Japanese text normalization helpers for typo detection."""

from __future__ import annotations

import unicodedata

_SMALL_KANA = str.maketrans({
    "ぁ": "あ", "ぃ": "い", "ぅ": "う", "ぇ": "え", "ぉ": "お",
    "ゃ": "や", "ゅ": "ゆ", "ょ": "よ", "っ": "つ", "ゎ": "わ",
    "ァ": "ア", "ィ": "イ", "ゥ": "ウ", "ェ": "エ", "ォ": "オ",
    "ャ": "ヤ", "ュ": "ユ", "ョ": "ヨ", "ッ": "ツ", "ヮ": "ワ",
})


def normalize_text(text: str) -> str:
    """Return an NFKC-normalized string suitable for dictionary lookup."""
    return unicodedata.normalize("NFKC", text).strip()


def loose_kana_key(text: str) -> str:
    """Return a key that tolerates common kana-size and prolonged-sound errors."""
    normalized = normalize_text(text).translate(_SMALL_KANA)
    return normalized.replace("ー", "").replace("-", "")
