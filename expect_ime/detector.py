"""Japanese typo detection and correction ranking for ExpectIME.

This module is intentionally independent from a platform IME frontend. It can be
embedded behind a Mozc-compatible candidate pipeline or tested as a pure Python
ranking component while the native integration matures.
"""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable

from .dictionary import DEFAULT_WORDS
from .normalization import loose_kana_key, normalize_text

_CONFUSABLES: dict[str, set[str]] = {
    "は": {"わ"}, "わ": {"は"},
    "へ": {"え"}, "え": {"へ"},
    "を": {"お"}, "お": {"を"},
    "じ": {"ぢ"}, "ぢ": {"じ"},
    "ず": {"づ"}, "づ": {"ず"},
    "ゃ": {"や"}, "ゅ": {"ゆ"}, "ょ": {"よ"}, "っ": {"つ"},
}

@dataclass(frozen=True, slots=True)
class TypoCandidate:
    """A correction candidate with an explainable confidence score."""

    text: str
    score: float
    reason: str

@dataclass(frozen=True, slots=True)
class Detection:
    """Typo detection result for one input token."""

    original: str
    normalized: str
    is_known: bool
    candidates: tuple[TypoCandidate, ...]

class JapaneseTypoDetector:
    """Dictionary-backed typo detector tuned for Japanese IME candidates.

    Ranking combines exact normalization, kana-loose matching, weighted edit
    distance, and sequence similarity. The weights favor common Japanese errors
    such as particles, dakuten-adjacent kana, small-kana confusion, and long
    vowel mark omissions.
    """

    def __init__(self, words: Iterable[str] = DEFAULT_WORDS) -> None:
        normalized_words = {normalize_text(word) for word in words if normalize_text(word)}
        self._words = tuple(sorted(normalized_words))
        self._word_set = set(self._words)
        self._loose_index: dict[str, list[str]] = {}
        for word in self._words:
            self._loose_index.setdefault(loose_kana_key(word), []).append(word)

    def detect(self, text: str, *, limit: int = 5) -> Detection:
        """Detect likely typo candidates for *text*.

        Args:
            text: User input or an IME candidate token.
            limit: Maximum number of correction candidates to return.
        """
        normalized = normalize_text(text)
        if not normalized:
            return Detection(text, normalized, False, ())
        if normalized in self._word_set:
            return Detection(text, normalized, True, ())

        candidates: list[TypoCandidate] = []
        seen: set[str] = set()
        loose_key = loose_kana_key(normalized)
        for word in self._loose_index.get(loose_key, []):
            candidates.append(TypoCandidate(word, 0.98, "kana-size/prolonged-sound normalization match"))
            seen.add(word)

        for word in self._words:
            if word in seen:
                continue
            distance = _weighted_edit_distance(normalized, word)
            max_len = max(len(normalized), len(word), 1)
            similarity = SequenceMatcher(a=normalized, b=word).ratio()
            score = max(0.0, 1.0 - (distance / max_len)) * 0.7 + similarity * 0.3
            if score >= 0.58:
                candidates.append(TypoCandidate(word, round(score, 4), _reason_for(normalized, word)))

        ranked = tuple(sorted(candidates, key=lambda item: (-item.score, item.text))[:limit])
        return Detection(text, normalized, False, ranked)


def _weighted_edit_distance(source: str, target: str) -> float:
    previous = [float(index) for index in range(len(target) + 1)]
    for i, source_char in enumerate(source, start=1):
        current = [float(i)]
        for j, target_char in enumerate(target, start=1):
            substitution = previous[j - 1] + _substitution_cost(source_char, target_char)
            insertion = current[j - 1] + _insertion_cost(target_char)
            deletion = previous[j] + _insertion_cost(source_char)
            current.append(min(substitution, insertion, deletion))
        previous = current
    return previous[-1]


def _substitution_cost(left: str, right: str) -> float:
    if left == right:
        return 0.0
    if right in _CONFUSABLES.get(left, set()):
        return 0.25
    if loose_kana_key(left) == loose_kana_key(right):
        return 0.35
    return 1.0


def _insertion_cost(char: str) -> float:
    return 0.35 if char in "ーっッぁぃぅぇぉゃゅょァィゥェォャュョ" else 1.0


def _reason_for(source: str, target: str) -> str:
    if len(source) != len(target):
        return "possible insertion/deletion typo"
    if any(t in _CONFUSABLES.get(s, set()) for s, t in zip(source, target, strict=False)):
        return "common Japanese particle/kana confusion"
    return "high string similarity"
