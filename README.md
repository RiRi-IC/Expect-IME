# Expect-IME

ExpectIME is a Mozc-inspired Japanese IME project focused on high-precision
Japanese typo detection and correction ranking.

The current repository contains a tested Python prototype of the typo-detection
core. It is designed to be embedded behind a future Mozc-compatible candidate
pipeline while remaining easy to evaluate with dictionaries and regression
tests.

## Features

- Japanese text normalization with Unicode NFKC.
- Detection of common Japanese typing mistakes such as `は/わ`, `へ/え`,
  `を/お`, `ず/づ`, and `じ/ぢ`.
- Tolerance for small-kana and prolonged-sound mark mistakes.
- Explainable correction candidates with confidence scores and reasons.
- Pluggable dictionaries for domain-specific Japanese vocabulary.

## Quick start

```python
from expect_ime import JapaneseTypoDetector

detector = JapaneseTypoDetector()
result = detector.detect("こんにちわ")
print(result.candidates[0].text)  # こんにちは
```

## Run tests

```bash
python -m pytest
```

See [docs/design.md](docs/design.md) for the accuracy strategy and Mozc
integration path.
