import pytest

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
    'llavero': "jja.'Be.4o",
    'allanar': "a.jja.'na4",
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
    'cuitláhuac': "kwi.'tla.Gwak",
    'salud': "sa.'lud",
    'búho': "'bu.o",
    'código': "'ko.di.Go",
    'aguacate': "a.Gwa.'ka.te",
    'Huitzilac': "gwit.si.'lak",
    'entréguennos': "en.'t4e.Gen.nos",
    'alzado': "al.'sa.Do",
    'encima': "en.'si.ma",
    'ya': "'jja",
    'ayer': "a.'jje4",
    'país': "pa.'is",
    'río': "'ri.o",
    'rehúso': "re.'u.so",
    'atlante': "a.'tlan.te",
    'tlaco': "'tla.ko",
    'hueso': "'gwe.so",
    'robot': "ro.'Bot",
    'prueba': "'p4we.Ba",
    'cráneo': "'k4a.ne.o",
    'frase': "'f4a.se",
    'globo': "'glo.Bo",
    'clase': "'kla.se",
    'prohíbe': "p4o.'i.be",
    'ancla': "'an.kla",
    'congreso': "kon.'g4e.so",
    'reúne': "re.'u.ne",
}

# Proposed Nahuatl-origin toponyms/loans with <x> for manual review.
# Kept separate because <x> is intentionally unstable and under active rule design.
nahuatl_x_review_cases = {
    'México': "'me.xi.ko",
    'Oaxaca': "Gwa.'xa.ka",
    'Xochimilco': "so.tSi.'mil.ko",
    'Xochicalco': "so.tSi.'kal.ko",
    'Texcoco': "teks.'ko.ko",
    'Mixcoac': "miks.ko.'ak",
    'Ixtapaluca': "iks.ta.pa.'lu.ka",
    'Ixtlahuaca': "iks.tla.'Gwa.ka",
    'Xola': "'So.la",
}


@pytest.mark.parametrize("word, expected", gold_cases.items())
def test_transcriber_gold_cases(word: str, expected: str) -> None:
    assert transcriber.transcriber(word) == expected


@pytest.mark.skip(reason="Manual review set: Nahuatl <x> behavior is still being defined")
@pytest.mark.parametrize("word, expected", nahuatl_x_review_cases.items())
def test_transcriber_nahuatl_x_review_cases(word: str, expected: str) -> None:
    assert transcriber.transcriber(word) == expected
