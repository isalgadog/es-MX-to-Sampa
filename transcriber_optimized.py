import resources
import itertools

plosives = resources.plosives
vowels = resources.vowels
map_unvar = resources.map_unvar

def transcriber(text):
    print(text)
    text = list(text.lower())
    output = []

    # PHONEMIC TRANSCRIPTION
    grave_endings = ["n", "s", "a", "e", "i", "o", "u"]
    word_ending = text[-1]
    
    # Define phonemic rules using a dictionary
    phonemic_rules = {
        "c": {"h": "tS", "e": "s", "i": "s", "default": "k"},
        "q": {"u": "k", "default": "k"},
        "s": {"h": "S", "default": "s"},
        "r": {"default": "r" if text[0] == "r" or word_ending == "r" or any(prev in ["n", "l", "s"] for prev in text[:-1]) else "4"},
        "l": {"l": "j", "default": "l" if text[0] != "l" else " "},
        "g": {"a": "g" if text[0] == "g" else "G", "o": "g" if text[0] == "g" else "G", "u": "g" if text[0] == "g" else "G", "e": "x", "i": "x", "default": "G" if any(prev in ["a", "e", "i", "o", "u"] and nxt in ["a", "e", "o"] for prev, nxt in zip(text[:-1], text[1:])) else "g"},
        "u": {"a": "w", "e": "w", "default": "w" if any(prev in ["a", "e", "o"] for prev in text[:-1]) else "u"},
        "i": {"a": "j", "e": "j", "o": "j", "á": "j", "é": "j", "ó": "j", "default": "j" if any(prev in ["a", "e", "o"] for prev in text[:-1]) else "i"},
        "n": {"default": "m" if any(nxt in ["b", "p", "f", "v"] for nxt in text[1:]) else "n"},
        "b": {"default": "B" if any(prev in vowels and nxt in vowels for prev, nxt in zip(text[:-1], text[1:])) else "b"},
        "v": {"default": "B" if any(prev in vowels and nxt in vowels for prev, nxt in zip(text[:-1], text[1:])) else "b"},
        "d": {"default": "D" if any(prev in vowels and nxt in vowels for prev, nxt in zip(text[:-1], text[1:])) else "d"},
        "á": {"default": "'a"},
        "é": {"default": "'e"},
        "í": {"default": "'i"},
        "ó": {"default": "'o"},
        "ú": {"default": "'u"}
    }

    # Apply phonemic rules
    for i, letter in enumerate(text):
        # Check if it's the last letter
        next_letter = text[i + 1] if i < len(text) - 1 else None
        previous_letter = text[i - 1] if i > 0 else None

        if letter in map_unvar:
            output.append(map_unvar[letter])
        elif letter == "r" and previous_letter == "r":
            continue  # Skip adding "4" after "r"
        elif letter == "u" and previous_letter in ["g", "q"] and next_letter in ["e", "i"]:
            continue
        elif letter == "h":
            continue
        elif letter in phonemic_rules:
            output.append(phonemic_rules[letter].get(next_letter, phonemic_rules[letter]["default"]))
        else:
            output.append(letter)
    
    phonemes = [char for char in output if char != " "]  # Remove spaces

    # SYLLABLE SEPARATION
    modified_phonemes = ["." if i > 0 and phoneme in plosives and i < len(phonemes) - 1 else phoneme for i, phoneme in enumerate(phonemes)]
    
    joint_phonemes = "".join(modified_phonemes)

    # Extract vowels
    vowel_list = [char for char in phonemes if char in vowels]

    # Determine stress
    stress = "acute" if "'" in text or any(x in text for x in "áéíóú") else "grave" if word_ending in grave_endings else "acute" if vowel_list[-1] in ["'a", "'e", "'i", "'o", "'u"] else "grave" if len(vowel_list) > 1 and vowel_list[-2] in ["'a", "'e", "'i", "'o", "'u"] else "paroxytone" if len(vowel_list) > 2 and vowel_list[-3] in ["'a", "'e", "'i", "'o", "'u"] else "grave"

    # Split into syllables
    syllable_list = ["".join(syllable) + "." for is_last, syllable in itertools.groupby(joint_phonemes, lambda x: x == ".") if not is_last]
    syllable_list[-1] = syllable_list[-1].rstrip(".")  # Remove the trailing dot

    # Insert stress marks
    for i, syllable in enumerate(syllable_list):
        if stress == "acute":
            syllable_list[-1] = syllable_list[-1].replace(".", "'")
        elif stress == "grave":
            syllable_list[-2] = syllable_list[-2].replace(".", "'")
        else:
            syllable_list[-3] = syllable_list[-3].replace(".", "'")

    final_transcription = "".join(syllable_list)
    print(final_transcription)

    return phonemes




transcriber("hola")
transcriber("chola")
transcriber("hache")
transcriber("cazo")
transcriber("cenar")
transcriber("cirio")
transcriber("cola")
transcriber("cultura")
transcriber("quesos")
transcriber("quilate")
transcriber("shampoo")
transcriber("coshan")
transcriber("rezar")
transcriber("llavero")
transcriber("allanar")
transcriber("rosa")
transcriber("rosario")
transcriber("ferrocarrilero")
transcriber("israel")
transcriber("enrique")
transcriber("alrato")
transcriber("auto")
transcriber("europa")
transcriber("cuarto")
transcriber("enviar")
transcriber("biombo")
transcriber("viejo")
transcriber("caigo")
transcriber("reino")
transcriber("Bebesaurio")
transcriber("dedicación")
transcriber("gato")
transcriber("aguileño")
transcriber("agachar")
transcriber("gelatina")
transcriber("gitano")
transcriber("gorda")
transcriber("gurú")
transcriber("Guerrero")
transcriber("guiño")
transcriber("Útica")