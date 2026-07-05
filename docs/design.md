# ExpectIME Japanese Typo Detection Design

ExpectIME is planned as a Mozc-inspired Japanese IME that separates the native
IME frontend from a correction-ranking core. The first implementation in this
repository provides the ranking core as a pure Python module so accuracy rules
can be tested before platform-specific Mozc-compatible integration is added.

## Accuracy strategy

1. Normalize input with Unicode NFKC so full-width ASCII, half-width kana, and
   compatibility forms map to stable dictionary keys.
2. Build a loose kana key that tolerates small-kana mistakes and omitted long
   vowel marks.
3. Rank correction candidates with weighted edit distance instead of plain
   Levenshtein distance. Japanese-specific mistakes such as `は/わ`, `へ/え`,
   `を/お`, `ず/づ`, and `じ/ぢ` receive a lower substitution penalty.
4. Combine weighted edit distance with sequence similarity to keep suggestions
   stable for short tokens while still finding likely corrections for longer
   words.
5. Allow callers to pass an expanded domain dictionary. This mirrors Mozc-style
   dictionary candidate generation and lets deployments add medical, legal,
   product, or organization-specific vocabulary.

## Mozc integration path

The detector is frontend-agnostic. A Mozc-based candidate pipeline can call the
ranking core after dictionary lookup and before presenting candidates, using the
returned score and reason to boost or annotate typo-correction candidates.
