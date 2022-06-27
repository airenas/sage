from sage.cfg.grammar import Calculator
from sage.cfg.parser import ResultParser


def parse(txt: str) -> (str, bool):
    cfg = Calculator(file="data/calc/grammar.cfg")
    parser = ResultParser()
    tree, ok = cfg.parse(txt)
    if not ok:
        return "", False
    elif tree is None:
        return "", False
    return parser.parse(tree), True


def test_parse_simple():
    ok_test("penki plius šeši kart septyni", "47")
    ok_test("du šimtai dvidešimt vienas kart keturi", "884")
    ok_test("dvidešimt du plius trys", "25")
    ok_test("du plius trys", "5")
    ok_test("dešimt plius trys", "13")
    ok_test("dešimt minus trys", "7")


def ok_test(s, v):
    res, ok = parse(s)
    assert ok
    assert res == v
