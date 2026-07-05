"""ExpectIME Japanese typo detection toolkit."""

from .detector import Detection, JapaneseTypoDetector, TypoCandidate

__version__ = "0.1.0"

__all__ = ["Detection", "JapaneseTypoDetector", "TypoCandidate", "__version__"]
