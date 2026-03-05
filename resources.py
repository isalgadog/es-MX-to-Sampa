# Unvariable transcription
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

plosives = ["p", "t", "k", "b", "d", "g", "B", "D", "G", "tS", "r", "J", "x", "f"]
vowels = ["a", "e", "i", "o", "u", "w", "j"]

accented_vowels = ["á", "é", "í", "ó", "ú"]
vowel_or_accented = ["a", "e", "i", "o", "u", "á", "é", "í", "ó", "ú"]
plain_vowels = ["a", "e", "i", "o", "u"]
stressed_vowel_phonemes = ["'a", "'e", "'i", "'o", "'u"]
grave_endings = ["n", "s", "a", "e", "i", "o", "u"]
stressed_like_phonemes = ["'i", "'u", "'e", "'a", "'o"]
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