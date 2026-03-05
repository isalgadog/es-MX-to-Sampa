"""Static linguistic resources used by the transcription pipeline.

All symbols and lists in this module are consumed by ``transcriber.py``.
This file contains no logic—only lexical/phonological inventories and
word-level overrides.
"""

# One-to-one grapheme mappings that do not depend on surrounding context.
map_unvar = {
    "a": "a",
    "e": "e",
    "o": "o",
    "f": "f",
    "j": "x",
    "k": "k",
    "m": "m",
    "ñ": "J",
    "p": "p",
    "t": "t",
    "w": "gw",
    "z": "s"
}

# Consonants that pattern as plosive/obstruent-like boundaries in syllabification
# and allophonic rules.
plosives = ["p", "t", "k", "b", "d", "g", "B", "D", "G", "tS", "r", "J", "x", "f"]

# Vowel-like nuclei recognized by the transcriber (including semivowels).
vowels = ["a", "e", "i", "o", "u", "w", "j"]

# Source-text accented vowels and helper groupings for stress logic.
accented_vowels = ["á", "é", "í", "ó", "ú"]
vowel_or_accented = ["a", "e", "i", "o", "u", "á", "é", "í", "ó", "ú"]
plain_vowels = ["a", "e", "i", "o", "u"]

# Target stressed vowel phonemes used by the output representation.
stressed_vowel_phonemes = ["'a", "'e", "'i", "'o", "'u"]

# Endings that trigger default grave stress placement in Spanish.
grave_endings = ["n", "s", "a", "e", "i", "o", "u"]

# Tokens treated as already stress-marked equivalents in downstream checks.
stressed_like_phonemes = ["'i", "'u", "'e", "'a", "'o"]

# Sonorant symbols that can influence syllable-break heuristics.
sonorant_breakers = ["4", "s", "n", "m", "l", "j", "jj", "w"]

# Whole-word overrides for unstable <x> behavior in Nahuatl-origin forms.
x_word_overrides = {
    "méxico": ["m", "'e", "x", "i", "k", "o"],
    "oaxaca": ["G", "w", "a", "x", "a", "k", "a"],
}

# Targeted linguistic syllabification overrides (final transcription string).
syllable_overrides = {
    "transcribir": "t4ans.'k4i.Bi4",
    "abstracto": "abs.'t4ak.to",
    "instituto": "ins.ti.'tu.to",
    "perspectiva": "pe4s.pek.'ti.Ba",
    "ritmo": "'rit.mo",
    "digno": "'dig.no",
}
