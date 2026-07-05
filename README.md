# Expect-IME

ExpectIME is a Mozc-inspired Japanese IME project focused on high-precision
Japanese typo detection and correction ranking.

The current release provides a packaged Python core for typo detection. It is
frontend-agnostic, so it can be evaluated independently and later embedded in a
Mozc-compatible candidate pipeline.

## Features

- Japanese text normalization with Unicode NFKC.
- Detection of common Japanese typing mistakes such as `は/わ`, `へ/え`,
  `を/お`, `ず/づ`, and `じ/ぢ`.
- Tolerance for small-kana and prolonged-sound mark mistakes.
- Explainable correction candidates with confidence scores and reasons.
- Pluggable dictionaries for domain-specific Japanese vocabulary.
- CLI support for plain text and JSON Lines output.

## Install from source

```bash
python -m pip install .
```

## Python usage

```python
from expect_ime import JapaneseTypoDetector

detector = JapaneseTypoDetector()
result = detector.detect("こんにちわ")
print(result.candidates[0].text)  # こんにちは
```

## CLI usage

```bash
expect-ime こんにちわ --json
```

Custom dictionaries are UTF-8 newline-delimited text files:

```bash
expect-ime --dictionary ./my_words.txt こんにちわ
```

## Run tests

```bash
python -m pytest
```

## Build a release package

```bash
python -m build
```

See [docs/design.md](docs/design.md) for the accuracy strategy and Mozc
integration path, and [RELEASE.md](RELEASE.md) for the release checklist.
