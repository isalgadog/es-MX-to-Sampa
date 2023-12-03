import transcriber

gold_cases = {
    'hola': "'o.la",
    'chola': "'tSo.la",
    'hache': "'a.tSe",
    'cazo': "'ka.so",
    'cola': "'ko.la",
    'cultura': "kul.'tu.4a",
    'quesos': "'ke.sos",
    'quilate': "ki.'la.te",
    'llavero': "ja.'Be.4o",
    'allanar': "a.ja.'na4",
    'rosa': "'ro.sa",
    'rosario': "ro.'sa.4jo",
    'ferrocarrilero': "fe.ro.ka.ri.'le.4o",
    'israel': "is.ra.'el",
    'enrique': "en.'ri.ke",
    'alrato': "al.'ra.to",
    'auto': "'aw.to",
    'europa': "ew.'4o.pa",
    'cuarto': "'kwa4.to",
    'enviar': "em.'bja4",
    'biombo': "'bjom.bo",
    'viejo': "'bje.xo",
    'caigo': "'kaj.Go",
    'reino': "'rej.no",
    'Bebesaurio': "be.Be.'saw.4jo",
    'dedicación': "de.Di.ka.'sjon",
    'gato': "'ga.to",
    'aguileño': "a.Gi.'le.Jo",
    'agachar': "a.Ga.'tSa4",
    'gelatina': "xe.la.'ti.na",
    'gitano': "xi.'ta.no",
    'gorda': "'go4.da",
    'gurú': "gu.'4u",
    'Guerrero': "ge.'re.4o",
    'guiño': "'gi.Jo",
    'Útica': "'u.ti.ka",
    'broca': "'b4o.ka",
    'hablar': "a.'bla4",
    'aurora': "aw.'4o.4a",
    'ángel': "'an.xel",
    'habladurías': "a.bla.Du.'4i.as",
    'baúl': "ba.'ul",
    'sofreír': "so.f4e.'i4",
    'cuauhtémoc': "kwaw.'te.mok",
    'cuitláhuac': "kui.'tla.Gwak",
    'salud': "sa.'lud",
    'búho': "'bu.o",
    'código': "'ko.di.Go",
    'aguacate': "a.Gwa.'ka.te",
    'Huitzilac': "gwit.si.'lak",
    'entréguennos': "en.'t4e.Gen.nos",
    'alzado': "al.'sa.Do",
    'encima': "en.'si.ma"
}

test_cases = {key: '' for key in gold_cases}

def test():
    for word in gold_cases:
        print(word)
        transcription = transcriber.transcriber(word)
        test_cases[word] = transcription
        print(transcription)

print(test_cases)


test()
print("GOLD: " + str(gold_cases))
print("TEST: " + str(test_cases))

differing_values = {}

for key in gold_cases:
    if gold_cases[key] != test_cases[key]:
        differing_values[key] = (gold_cases[key], test_cases[key])

print("ERRORS: " + str(differing_values))