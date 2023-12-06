import resources

plosives = resources.plosives
vowels = resources.vowels
map_unvar = resources.map_unvar

# Missing rules for "nsk4" and "sntr"
# Missing rules for "ps" belonging to two different syllables 

def transcriber(text):
    text = list(text.lower())
    output = []
    #PHONEMIC TRANSCRIPTION
    
    grave_endings = ["n", "s", "a", "e", "i", "o", "u"]
    word_ending = text[-1]
            
    for i, letter in enumerate(text):
        global phonemes
        # Check if it's the last letter
        next_letter = text[i + 1] if i < len(text) - 1 else None
        previous_letter = text[i - 1] if i > 0 else None        

        # Define phonemic rules using a dictionary
        phonemic_rules = {
            "c": {"h": "tS", 
                  "e": "s", 
                  "i": "s", 
                  "default": "k"},
            "q": {"u": "k", 
                  "default": "k"},
            "s": {"h": "S", 
                  "default": "s"},
            "r": {"default": "r" if i == 0 or next_letter == "r" or previous_letter in ["n", "l", "s"] else "4"},
            "l": {"l": "j", 
                  "default": "l" if previous_letter != "l" else " "},
            "g": {"a": "g" if i == 0 else "G", 
                  "o":"g" if i == 0 else "G", 
                  "u":"g" if i == 0 else "G", 
                  "e": "x", 
                  "i": "x", 
                  "default":"G" if previous_letter in ["a", "e", "i", "o", "u"] and next_letter in ["a", "e", "o"] else "g"},
            "u": {"a" : "w", 
                  "e": "w",
                  "default": "w" if previous_letter in ["a", "e", "o"] else "u"
                  },
            "i": {"a":"j", 
                  "e":"j", 
                  "o":"j",
                  "á":"j", 
                  "é":"j", 
                  "ó":"j",
                  "default": "j" if previous_letter in ["a", "e", "o"] else "i"},
            "n": {"default":"m" if next_letter in ["b", "p", "f", "v"] else "n"},
            "b": {"default": "B" if next_letter in ["a", "e", "i", "o", "u"] and previous_letter in ["a", "e", "i", "o", "u"] else "b"},
            "v": {"default": "B" if next_letter in ["a", "e", "i", "o", "u"] and previous_letter in ["a", "e", "i", "o", "u"] else "b"},
            "d": {"default": "D" if next_letter in ["a", "e", "i", "o", "u"] and previous_letter in ["a", "e", "i", "o", "u"] else "d"},
            "á": {"default": "'a"},
            "é": {"default": "'e"},
            "í": {"default": "'i"},
            "ó": {"default": "'o"},
            "ú": {"default": "'u"}
        }

        #Apply phonemic rules
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

    #SYLLABLE SEPARATION
    modified_phonemes = []
    for i, phoneme in enumerate(phonemes):
        # Check if it's the last phoneme
        next_phoneme = phonemes[i + 1] if i < len(phonemes) - 1 else None
        previous_phoneme = phonemes[i - 1] if i > 0 else None

        if i == len(phonemes):
            modified_phonemes.append(phoneme)
        elif i > 0 and phoneme in plosives and i < len(phonemes)-1:
            modified_phonemes.append(".")
        elif i > 0 and phoneme in ["s", "n", "m"] and previous_phoneme in ["s", "n", "m", "l"]:
            modified_phonemes.append(".")
        elif i > 0 and phoneme in ["4", "s", "n", "m", "l", "j", "w"] and (previous_phoneme in vowels or previous_phoneme in ["'i", "'u", "'e", "'a", "'o"]) and (next_phoneme in vowels or next_phoneme in ["'i", "'u", "'e", "'a", "'o"]):
            modified_phonemes.append(".")
        elif i > 0 and phoneme in ["a", "e", "o"] and previous_phoneme in ["a", "e", "o", "'i", "'u"]:
            modified_phonemes.append(".")
        elif i > 0 and phoneme in ["'i", "'u"] and previous_phoneme in ["a", "e", "o"]:
            modified_phonemes.append(".")
        modified_phonemes.append(phoneme)

    joint_phonemes = "".join(modified_phonemes)


    vowel_list = [char for char in phonemes if char in ["a", "e", "i", "o", "u", "'a", "'e", "'i", "'o", "'u"]]  # List comprehension to extract vowels

    if any(x in text for x in "áéíóú"):
        stress = "grave"
        if vowel_list[-1] in ["'a", "'e", "'i", "'o", "'u"]:
            stress = "acute"
        elif len(vowel_list) > 1 and vowel_list[-2] in ["'a", "'e", "'i", "'o", "'u"]:
            stress = "grave"

        elif len(vowel_list) > 2 and vowel_list[-3] in ["'a", "'e", "'i", "'o", "'u"]:
            stress = "paroxytone"
    else:
        if word_ending in grave_endings:
            stress = "grave"
        else:
            stress = "acute"


    
    syllable_list = [[]]
    i = 0
    for phoneme in joint_phonemes:
        if phoneme == "'":
            continue
        elif phoneme != ".":
            syllable_list[i].append(phoneme)
        else:
            syllable_list.append([])
            i +=1 

    if stress == "acute":
        syllable_list[-1].insert(0,"'") 
    elif stress == "grave":
        syllable_list[-2].insert(0,"'")
    else:
        syllable_list[-3].insert(0,"'")


    final_transcription = []
    for syllable in syllable_list:
        flat_syllable = "".join(syllable)
        final_transcription.append(flat_syllable)
        final_transcription.append(".")
    
    final_transcription = "".join(final_transcription)
    final_transcription = final_transcription[:-1]
    return final_transcription  