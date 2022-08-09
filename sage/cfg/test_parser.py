from sage.cfg.grammar import Calculator
from sage.cfg.parser import ResultParser, EqParser


def parse(txt: str, parser) -> (str, bool):
    cfg = Calculator(file="data/calc/grammar.cfg")
    tree, ok = cfg.parse(txt)
    if not ok:
        return "", False
    elif tree is None:
        return "", False
    return parser.parse(tree), True


def test_parse_simple():
    ok_test("skliaustai du plius keturi kart trys", "18")
    ok_test("skliaustai du minus keturi dalinti du", "-1")
    ok_test("dvi ketvirtosios", "0.5")
    ok_test("trys milijonai keturi šimtai tūkstančių šimtas dešimt", "3400110")
    ok_test("tūkstantis", "1000")
    ok_test("du tūkstančiai šimtas dešimt", "2110")
    ok_test("milijonas", "1000000")
    ok_test("du kablelis penki", "2.5")
    ok_test("šeši padalint iš dviejų", "3")
    ok_test("šeši padalint du", "3")
    ok_test("penki plius šeši padalint iš dviejų", "8")
    ok_test("penki plius šeši kart septyni", "47")
    ok_test("du šimtai dvidešimt vienas kart keturi", "884")
    ok_test("dvidešimt du plius trys", "25")
    ok_test("du plius trys", "5")
    ok_test("dešimt plius trys", "13")
    ok_test("dešimt minus trys", "7")


def ok_test(s, v):
    parser_test(ResultParser(), s, v)


def ok_eq_test(s, v):
    parser_test(EqParser(), s, v)


def parser_test(parser, s, v):
    res, ok = parse(s, parser)
    assert ok
    assert res == v


def test_eq_parse_simple():
    ok_eq_test("skliaustai du plius keturi dalinti du", "\\frac{\\left( 2 + 4 \\right)}{2}")
    ok_eq_test("du", "2")
    ok_eq_test("du plius trys", "2 + 3")
    ok_eq_test("tūkstantis", "1000")
    ok_eq_test("milijonas", "1000000")
    ok_eq_test("dešimt plius trys", "10 + 3")
    ok_eq_test("dvidešimt du plius trys", "22 + 3")
    ok_eq_test("dešimt minus trys", "10 - 3")
    ok_eq_test("du kablelis penki", "2.5")
    ok_eq_test("du kablelis penki plius keturi", "2.5 + 4")
    ok_eq_test("dvi ketvirtosios", "\\frac{2}{4}")
    ok_eq_test("du tūkstančiai šimtas dešimt", "2110")
    ok_eq_test("šeši padalint iš dviejų", "\\frac{6}{2}")
    ok_eq_test("šeši padalint du", "\\frac{6}{2}")
    ok_eq_test("penki plius šeši padalint iš dviejų", "5 + \\frac{6}{2}")
    ok_eq_test("trys milijonai keturi šimtai tūkstančių šimtas dešimt", "3400110")
    ok_eq_test("du šimtai dvidešimt vienas kart keturi", "221 \\cdot 4")
    ok_eq_test("penki plius šeši kart septyni", "5 + 6 \\cdot 7")

    ok_eq_test("skliaustai du minus keturi dalinti du", "\\frac{\\left( 2 - 4 \\right)}{2}")
    ok_eq_test("skliaustai du plius keturi kart trys", "\\left( 2 + 4 \\right) \\cdot 3")
