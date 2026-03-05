import re
from typing import Optional
import resources

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

# Missing rules for "nsk4" and "sntr"
# Missing rules for "ps" belonging to two different syllables


def _normalize_input(text: str) -> str:
    normalized_text = str(text).strip().lower()
    normalized_text = re.sub(r"[^a-záéíóúüñ]", "", normalized_text)
    return normalized_text


def _phonemic_rules(i: int, next_letter: Optional[str], previous_letter: Optional[str]) -> dict:
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
        "y": {
            "default": "jj"
            if i == 0 or (previous_letter in vowel_or_accented and next_letter in vowel_or_accented)
            else "j"
        },
    }


def _graphemes_to_phonemes(text_chars: list[str]) -> list[str]:
    output = []

    for i, letter in enumerate(text_chars):
        next_letter = text_chars[i + 1] if i < len(text_chars) - 1 else None
        previous_letter = text_chars[i - 1] if i > 0 else None
        phonemic_rules = _phonemic_rules(i, next_letter, previous_letter)

        if letter in map_unvar:
            output.append(map_unvar[letter])
        elif letter == "r" and previous_letter == "r":
            continue
        elif letter == "u" and previous_letter == "h" and i == 1 and next_letter in vowel_or_accented:
            output.extend(["g", "w"])
        elif letter == "u" and previous_letter == "h" and i > 1 and next_letter in vowel_or_accented:
            output.extend(["G", "w"])
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
    modified_phonemes = []

    for i, phoneme in enumerate(phonemes):
        next_phoneme = phonemes[i + 1] if i < len(phonemes) - 1 else None
        previous_phoneme = phonemes[i - 1] if i > 0 else None

        if i > 0 and phoneme in plosives and i < len(phonemes) - 1 and not (phoneme == "t" and next_phoneme == "s"):
            modified_phonemes.append(".")
        elif i > 0 and phoneme == "s" and previous_phoneme == "t":
            modified_phonemes.append(".")
        elif i > 0 and phoneme in ["s", "n", "m"] and previous_phoneme in ["s", "n", "m", "l"]:
            modified_phonemes.append(".")
        elif (
            i > 0
            and next_phoneme is not None
            and phoneme in sonorant_breakers
            and (previous_phoneme in vowels or previous_phoneme in stressed_like_phonemes)
            and (next_phoneme in vowels or next_phoneme in stressed_like_phonemes)
        ):
            modified_phonemes.append(".")
        elif i > 0 and phoneme in ["a", "e", "o"] and previous_phoneme in ["a", "e", "o", "'i", "'u"]:
            modified_phonemes.append(".")
        elif i > 0 and phoneme in ["'i", "'u"] and previous_phoneme in ["a", "e", "o"]:
            modified_phonemes.append(".")

        modified_phonemes.append(phoneme)

    return "".join(modified_phonemes)


def _compute_stress(text_chars: list[str], phonemes: list[str], word_ending: str) -> str:
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
    syllable_list = [[]]
    i = 0

    for phoneme in joint_phonemes:
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
    normalized_text = _normalize_input(text)
    if not normalized_text:
        return ""

    text_chars = list(normalized_text)
    word_ending = text_chars[-1]

    phonemes = _graphemes_to_phonemes(text_chars)
    joint_phonemes = _syllabify(phonemes)
    stress = _compute_stress(text_chars, phonemes, word_ending)

    return _apply_stress_and_format(joint_phonemes, stress)
