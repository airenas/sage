import pytest

from sage.cfg.grammar import extract_unknown_word, Calculator, UnknownWord


def test_unknown_word():
    assert extract_unknown_word("Olia") is None
    assert "olia" == extract_unknown_word('Grammar does not cover some of the input words: "\'olia\'".')


def test_parse():
    cfg = Calculator(file="data/calc/grammar.cfg")
    tree, ok = cfg.parse("du")
    assert ok
    assert tree is not None

    tree, ok = cfg.parse("du plius")
    assert ok
    assert tree is None


def test_raise_error():
    cfg = Calculator(file="data/calc/grammar.cfg")
    with pytest.raises(UnknownWord) as exc_info:
        cfg.parse("olia")
    assert exc_info.value.word == 'olia'
