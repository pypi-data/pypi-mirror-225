import json
from copy import deepcopy
from pathlib import Path

from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_readinggrid.readinggrid import (
    ReadingGridProcessor,
    ReadingGridParameters, BooleanCondition,
)


def test_readinggrid():
    testdir = Path(__file__).parent / "data"
    json_file = testdir / "french.json"
    with json_file.open("r") as fin:
        doc = json.load(fin)
    doc = Document(**doc)
    nb_sents = len(doc.sentences)
    nb_annots = len(doc.annotations)
    parameters = ReadingGridParameters(separator="\u22ee")
    formatter = ReadingGridProcessor()
    docs = formatter.process([deepcopy(doc)], parameters)
    assert len(docs[0].sentences) < nb_sents
    assert len(docs[0].annotations) == nb_annots
    for sent in docs[0].sentences:
        stext = docs[0].text[sent.start: sent.end]
        assert "pas" not in stext
    sum_file = testdir / "french_grid.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)

    parameters = ReadingGridParameters(
        separator="\u22ee", as_altText="Grille de lecture"
    )
    docs = formatter.process([deepcopy(doc)], parameters)
    assert len(docs[0].sentences) == nb_sents
    assert len(docs[0].annotations) == nb_annots
    assert len(docs[0].text) > len(docs[0].altTexts[0].text)
    assert "pas" not in docs[0].altTexts[0].text
    sum_file = testdir / "french_grid_alt.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def test_readinggrid_keep():
    testdir = Path(__file__).parent / "data"
    json_file = testdir / "french.json"
    with json_file.open("r") as fin:
        jdoc = json.load(fin)
    doc = Document(**jdoc)
    parameters = ReadingGridParameters(keep=True, labels=["wiki1", "wiki3"], condition=BooleanCondition.OR)
    formatter = ReadingGridProcessor()
    docs = formatter.process([deepcopy(doc)], parameters)
    assert len(docs[0].sentences) == 2
    for sent in docs[0].sentences:
        stext = docs[0].text[sent.start: sent.end]
        assert "pas" not in stext
    assert len(docs[0].annotations) == 3
    for a in docs[0].annotations:
        assert a.labelName in ["wiki1", "wiki3"]

    doc = Document(**jdoc)
    parameters.condition = BooleanCondition.AND
    docs = formatter.process([deepcopy(doc)], parameters)
    assert len(docs[0].sentences) == 1
    for sent in docs[0].sentences:
        stext = docs[0].text[sent.start: sent.end]
        assert "pas" not in stext
    assert len(docs[0].annotations) == 2
    for a in docs[0].annotations:
        assert a.labelName in ["wiki1", "wiki3"]


def test_readinggrid_remove():
    testdir = Path(__file__).parent / "data"
    json_file = testdir / "french.json"
    with json_file.open("r") as fin:
        jdoc = json.load(fin)
    doc = Document(**jdoc)
    parameters = ReadingGridParameters(keep=False, labels=["wiki1", "wiki3"], condition=BooleanCondition.OR)
    formatter = ReadingGridProcessor()
    docs = formatter.process([deepcopy(doc)], parameters)
    assert len(docs[0].sentences) == 4
    assert len(docs[0].annotations) == 1
    for a in docs[0].annotations:
        assert a.labelName not in ["wiki1", "wiki3"]

    doc = Document(**jdoc)
    parameters.condition = BooleanCondition.AND
    docs = formatter.process([deepcopy(doc)], parameters)
    assert len(docs[0].sentences) == 5
