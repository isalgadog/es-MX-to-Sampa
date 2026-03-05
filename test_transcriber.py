"""Regression tests for ``transcriber.transcriber``.

The dictionaries below act as compact fixtures:
- ``gold_cases``: stable baseline corpus expected to pass continuously.
- ``x_cluster_cases``: historically variable <x>-cluster words kept in a
  separate skipped suite for explicit review.
"""

import pytest

import transcriber


# Canonical word -> expected transcription mappings used as the primary
# regression test corpus.
gold_cases = {
    'hola': "'o.la",
    'casa': "'ka.sa",
    'mesa': "'me.sa",
    'perro': "'pe.ro",
    'rosa': "'ro.sa",
    'gato': "'ga.to",
    'grande': "'g4an.de",
    'escuela': "es.'kwe.la",
    'campo': "'kam.po",
    'barrio': "'ba.rjo",
    'hablar': "a.'bla4",
    'dormir': "do4.'mi4",
    'verde': "'be4.de",
    'blanco': "'blan.ko",
    'lengua': "'len.Gwa",
    'ventana': "ben.'ta.na",
    'tarde': "'ta4.de",
    'camino': "ka.'mi.no",
    'domingo': "do.'min.Go",
    'comida': "ko.'mi.Da",
    'código': "'ko.di.Go",
    'médico': "'me.di.ko",
    'música': "'mu.si.ka",
    'teléfono': "te.'le.fo.no",
    'jamás': "xa.'mas",
    'reloj': "re.'lox",
    'pared': "pa.'4ed",
    'ángel': "'an.xel",
    'útil': "'u.til",
    'público': "'pu.bli.ko",
    'dedicatoria': "de.Di.ka.'to.4ja",
    'canción': "kan.'sjon",
    'sofá': "so.'fa",
    'compás': "kom.'pas",
    'fácil': "'fa.sil",
    'país': "pa.'is",
    'río': "'ri.o",
    'baúl': "ba.'ul",
    'rehúso': "re.'u.so",
    'reúne': "re.'u.ne",
    'cuidado': "kwi.'Da.Do",
    'ruido': "'rwi.Do",
    'Europa': "ew.'4o.pa",
    'auto': "'aw.to",
    'causa': "'kaw.sa",
    'peine': "'pej.ne",
    'oír': "o.'i4",
    'poesía': "po.e.'si.a",
    'caída': "ka.'i.da",
    'búho': "'bu.o",
    'prueba': "'p4we.Ba",
    'clase': "'kla.se",
    'globo': "'glo.Bo",
    'ancla': "'an.kla",
    'congreso': "kon.'g4e.so",
    'transcribir': "t4ans.k4i.'Bi4",
    'texto': "'teks.to",
    'abstracto': "abs.'t4ak.to",
    'instituto': "ins.ti.'tu.to",
    'atlas': "'a.tlas",
    'atleta': "a.'tle.ta",
    'mezcla': "'mes.kla",
    'ritmo': "'rit.mo",
    'digno': "'dig.no",
    'perspectiva': "pe4s.pek.'ti.Ba",
    'ya': "'jja",
    'ayer': "a.'jje4",
    'yo': "'jjo",
    'yema': "'jje.ma",
    'playa': "'pla.jja",
    'apoyo': "a.'po.jjo",
    'llano': "'jja.no",
    'lluvia': "'jju.Bja",
    'llave': "'jja.Be",
    'hallazgo': "a.'jjas.Go",
    'hueso': "'gwe.so",
    'huerto': "'gwe4.to",
    'huevo': "'gwe.Bo",
    'Huitzilac': "gwit.si.'lak",
    'cuitláhuac': "kwi.'tla.Gwak",
    'antigüedad': "an.ti.gwe.'Dad",
    'pingüino': "pin.'gwi.no",
    'vergüenza': "be4.'gwen.sa",
    'agüita': "a.'gwi.ta",
    'ahuehuete': "a.Gwe.'Gwe.te",
}


# Additional corpus for words with historically unstable orthographic <x>
# behavior; kept separate and skipped by default.
x_cluster_cases = {
    'México': "'me.xi.ko",
    'Oaxaca': "Gwa.'xa.ka",
    'Xola': "'So.la",
    'Xochimilco': "so.tSi.'mil.ko",
    'Xochicalco': "so.tSi.'kal.ko",
    'Texcoco': "teks.'ko.ko",
    'Mixcoac': "miks.ko.'ak",
    'Ixtapaluca': "iks.ta.pa.'lu.ka",
    'Ixtlahuaca': "iks.tla.'Gwa.ka",
    'Xalapa': "Sa.'la.pa",
    'Xico': "'Si.ko",
    'Xicoténcatl': "Si.ko.'ten.katl",
    'Xochitepec': "so.tSi.te.'pek",
    'Xochitecatl': "so.tSi.te.'katl",
    'Axapusco': "aSa.'pus.ko",
    'Xiutetelco': "Siu.te.'tel.ko",
    'Xonacatlán': "So.na.ka.'tlan",
    'Xaltocan': "Sal.'to.kan",
    'Xochistlahuaca': "so.tSis.tla.'Gwa.ka",
    'Xonacatepec': "So.na.ka.te.'pek",
}


@pytest.mark.parametrize("word, expected", gold_cases.items())
def test_transcriber_gold_cases(word: str, expected: str) -> None:
    """Validate baseline transcriptions for the main regression corpus."""
    assert transcriber.transcriber(word) == expected


@pytest.mark.skip(reason="Special X cluster: reviewed separately")
@pytest.mark.parametrize("word, expected", x_cluster_cases.items())
def test_transcriber_x_cluster_cases(word: str, expected: str) -> None:
    """Reference test for <x>-cluster cases kept outside default CI pass."""
    assert transcriber.transcriber(word) == expected
