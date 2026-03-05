import re
from typing import Optional
import resources

# Shared inventories and lookup tables live in resources.py.
# Keeping aliases here makes phonological rules easier to read.
plosives = resources.plosives
vowels = resources.vowels
map_unvar = resources.map_unvar
accented_vowels = resources.accented_vowels
vowel_or_accented = resources.vowel_or_accented
plain_vowels = resources.plain_vowels
stressed_vowel_phonemes = resources.stressed_vowel_phonemes
grave_endings = resources.grave_endings
stressed_like_phonemes = resources.stressed_like_phonemes
sonorant_breakers = resources.sonorant_breakers
x_word_overrides = resources.x_word_overrides

# Missing rules for "nsk4" and "sntr"
# Missing rules for "ps" belonging to two different syllables


def _normalize_input(text: str) -> str:
    """Normalize user text to a single lowercase Spanish token.

    The transcriber works at word level. We strip whitespace, lowercase,
    and remove anything that is not a Spanish letter (including accents/ü/ñ).
    """
    normalized_text = str(text).strip().lower()
    normalized_text = re.sub(r"[^a-záéíóúüñ]", "", normalized_text)
    return normalized_text


def _phonemic_rules(i: int, next_letter: Optional[str], previous_letter: Optional[str]) -> dict:
    """Return contextual grapheme→phoneme rules for the current position.

    Many Spanish letters are context-sensitive (e.g., c before e/i, intervocalic
    lenition for b/d/g, trilled vs tapped r). This helper centralizes those
    mappings so the main conversion loop stays linear and readable.
    """
    return {
        "c": {"h": "tS", "e": "s", "i": "s", "default": "k"},
        "q": {"u": "k", "default": "k"},
        "s": {"h": "S", "default": "s"},
        "r": {"default": "r" if i == 0 or next_letter == "r" or previous_letter in ["n", "l", "s"] else "4"},
        "l": {"l": "jj", "default": "l" if previous_letter != "l" else " "},
        "g": {
            "a": "g" if i == 0 else "G",
            "o": "g" if i == 0 else "G",
            "u": "g" if i == 0 else "G",
            "e": "x",
            "i": "x",
            "default": "G" if previous_letter in ["a", "e", "i", "o", "u"] and next_letter in ["a", "e", "o"] else "g",
        },
        "u": {
            "a": "w",
            "e": "w",
            "i": "w",
            "á": "w",
            "é": "w",
            "í": "w",
            "o": "w",
            "ó": "w",
            "default": "w" if previous_letter in ["a", "e", "o"] else "u",
        },
        "i": {
            "a": "j",
            "e": "j",
            "o": "j",
            "á": "j",
            "é": "j",
            "ó": "j",
            "default": "j" if previous_letter in ["a", "e", "o"] else "i",
        },
        "n": {"default": "m" if next_letter in ["b", "p", "f", "v"] else "n"},
        "b": {"default": "B" if next_letter in ["a", "e", "i", "o", "u"] and previous_letter in ["a", "e", "i", "o", "u"] else "b"},
        "v": {"default": "B" if next_letter in ["a", "e", "i", "o", "u"] and previous_letter in ["a", "e", "i", "o", "u"] else "b"},
        "d": {"default": "D" if next_letter in ["a", "e", "i", "o", "u"] and previous_letter in ["a", "e", "i", "o", "u"] else "d"},
        "á": {"default": "'a"},
        "é": {"default": "'e"},
        "í": {"default": "'i"},
        "ó": {"default": "'o"},
        "ú": {"default": "'u"},
        "ü": {"default": "w"},
        "y": {
            "default": "jj"
            if i == 0 or (previous_letter in vowel_or_accented and next_letter in vowel_or_accented)
            else "j"
        },
    }


def _graphemes_to_phonemes(text_chars: list[str]) -> list[str]:
    """Convert normalized letters into a linear phoneme sequence.

    The function applies:
    - invariant mappings (map_unvar),
    - special-case digraph/trigraph handling (e.g., x/ch patterns),
    - silent letters (h, orthographic u in gue/gui/que/qui),
    - and fallback contextual rules from _phonemic_rules.
    """
    output = []

    for i, letter in enumerate(text_chars):
        next_letter = text_chars[i + 1] if i < len(text_chars) - 1 else None
        next_next_letter = text_chars[i + 2] if i < len(text_chars) - 2 else None
        next_third_letter = text_chars[i + 3] if i < len(text_chars) - 3 else None
        previous_letter = text_chars[i - 1] if i > 0 else None
        phonemic_rules = _phonemic_rules(i, next_letter, previous_letter)

        if letter in map_unvar:
            output.append(map_unvar[letter])
        # x has several orthography-dependent realizations in this project.
        elif letter == "x" and next_letter in plain_vowels and next_next_letter == "c" and next_third_letter == "h":
            output.append("s")
        elif letter == "x" and next_letter == "c" and next_next_letter == "h":
            output.append("s")
        elif letter == "x" and next_letter in ["c", "t"]:
            output.extend(["k", "s"])
        elif letter == "x":
            output.append("S")
        # rr is represented by a single trill token; skip duplicated second r.
        elif letter == "r" and previous_letter == "r":
            continue
        # huV can surface as [gw] word-initially and [Gw] elsewhere.
        elif letter == "u" and previous_letter == "h" and i == 1 and next_letter in vowel_or_accented:
            output.extend(["g", "w"])
        elif letter == "u" and previous_letter == "h" and i > 1 and next_letter in vowel_or_accented:
            output.extend(["G", "w"])
        # Orthographic u in gue/gui/que/qui is silent unless explicitly diaerized.
        elif letter == "u" and previous_letter in ["g", "q"] and next_letter in ["e", "i"]:
            continue
        elif letter == "h":
            continue
        elif letter in phonemic_rules:
            output.append(phonemic_rules[letter].get(next_letter, phonemic_rules[letter]["default"]))
        else:
            output.append(letter)

    return [char for char in output if char != " "]


def _syllabify(phonemes: list[str]) -> str:
    """Insert syllable boundaries using onset-maximization heuristics.

    Strategy:
    1) Find vowel nuclei.
    2) For each inter-vocalic consonant cluster, decide how much attaches to
       the following syllable onset.
    3) Prefer legal Spanish onsets (allowed_onsets); otherwise split later.

    This is a practical heuristic syllabifier for stress placement, not a full
    phonological parser.
    """
    nucleus_tokens = set(plain_vowels + stressed_vowel_phonemes)
    allowed_onsets = {
        ("p", "4"), ("b", "4"), ("t", "4"), ("d", "4"), ("k", "4"), ("g", "4"), ("G", "4"), ("f", "4"),
        ("p", "l"), ("b", "l"), ("k", "l"), ("g", "l"), ("G", "l"), ("f", "l"), ("t", "l"),
        ("k", "w"), ("g", "w"), ("G", "w"),
        ("b", "j"), ("B", "j"), ("d", "j"), ("D", "j"), ("4", "j"), ("r", "j"), ("s", "j"),
        ("g", "ü"), ("G", "ü"), ("k", "ü"),
    }

    vowel_positions = [i for i, p in enumerate(phonemes) if p in nucleus_tokens]
    if len(vowel_positions) <= 1:
        return "".join(phonemes)

    starts = [0]

    for idx in range(len(vowel_positions) - 1):
        left_v = vowel_positions[idx]
        right_v = vowel_positions[idx + 1]
        cluster = phonemes[left_v + 1:right_v]
        cluster_len = len(cluster)

        # Decide where the next syllable starts based on inter-vocalic cluster size.
        if cluster_len == 0:
            next_start = right_v
        elif cluster_len == 1:
            next_start = right_v - 1
        elif cluster_len == 2:
            next_start = right_v - 2 if tuple(cluster) in allowed_onsets else right_v - 1
        else:
            last_two = tuple(cluster[-2:])
            next_start = right_v - 2 if last_two in allowed_onsets else right_v - 1

        if next_start > starts[-1]:
            starts.append(next_start)

    syllables = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(phonemes)
        syllables.append("".join(phonemes[start:end]))

    return ".".join(syllables)


def _compute_stress(text_chars: list[str], phonemes: list[str], word_ending: str) -> str:
    """Determine stress class (acute/grave/paroxytone).

    If written accents exist, they override default Spanish stress rules.
    Otherwise, infer stress from the canonical orthographic ending pattern.
    """
    vowel_list = [char for char in phonemes if char in plain_vowels + stressed_vowel_phonemes]

    if any(x in text_chars for x in accented_vowels):
        stress = "grave"
        if vowel_list and vowel_list[-1] in stressed_vowel_phonemes:
            stress = "acute"
        elif len(vowel_list) > 1 and vowel_list[-2] in stressed_vowel_phonemes:
            stress = "grave"
        elif len(vowel_list) > 2 and vowel_list[-3] in stressed_vowel_phonemes:
            stress = "paroxytone"
    else:
        stress = "grave" if word_ending in grave_endings else "acute"

    return stress


def _apply_stress_and_format(joint_phonemes: str, stress: str) -> str:
    """Insert stress marker into the selected syllable and rebuild output string."""
    syllable_list = [[]]
    i = 0

    for phoneme in joint_phonemes:
        # Ignore pre-existing accent markers from intermediate representation;
        # stress is re-applied consistently from the computed class.
        if phoneme == "'":
            continue
        if phoneme != ".":
            syllable_list[i].append(phoneme)
        else:
            syllable_list.append([])
            i += 1

    if stress == "acute":
        stress_index = -1
    elif stress == "grave":
        stress_index = -2 if len(syllable_list) >= 2 else -1
    else:
        stress_index = -3 if len(syllable_list) >= 3 else (-2 if len(syllable_list) >= 2 else -1)

    syllable_list[stress_index].insert(0, "'")

    final_transcription = []
    for syllable in syllable_list:
        final_transcription.append("".join(syllable))
        final_transcription.append(".")

    return "".join(final_transcription)[:-1]


def transcriber(text):
    """Transcribe a Spanish word into the project's SAMPA-like representation."""
    normalized_text = _normalize_input(text)
    if not normalized_text:
        return ""

    text_chars = list(normalized_text)
    word_ending = text_chars[-1]

    # Some x-initial/exceptional words are lexicalized to avoid overgeneralization.
    if normalized_text in x_word_overrides:
        phonemes = x_word_overrides[normalized_text]
    else:
        phonemes = _graphemes_to_phonemes(text_chars)
    joint_phonemes = _syllabify(phonemes)
    stress = _compute_stress(text_chars, phonemes, word_ending)

    return _apply_stress_and_format(joint_phonemes, stress)
