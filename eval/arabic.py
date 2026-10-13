"""Arabic text helpers for scoring speech recognition."""

import re

# Arabic diacritics (harakat, tanween, shadda, sukun), the dagger alef and tatweel.
_DIACRITICS = re.compile(r"[ً-ْٰـ]")


def strip_diacritics(text: str) -> str:
    """Remove Arabic diacritics and tatweel, leaving the letters unchanged."""
    return _DIACRITICS.sub("", text)
