
# Ortographic sets
# All letter are converted to lowercase before transcription to SAMPA.
vowels = [
    "a",
    "e", 
    "i", 
    "o", 
    "u"
]

vowels_stressed = [
    "á",
    "é",
    "í",
    "ó",
    "ú"
]

consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']

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
    "v": "b",
    "w": "w",
    "z": "s"
}

#Consonants that trigger r -> rr

cons_r = ["l", "n", "r","s"]
cons_B = ["l", "r", "s"]
