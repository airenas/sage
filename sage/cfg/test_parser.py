import pytest

from sage.cfg.grammar import Calculator
from sage.cfg.parser import ResultParser, EqParser


@pytest.mark.parametrize("txt,exp",
                         [("du", "2"),
                          ("du penktuoju laipsniu", "32"),
                          ("du pakelta trečiuoju", "8"),
                          ("du minus penktuoju laipsniu", "0.03125"),
                          ("du penktuoju laipsniu", "32"),
                          ("du pakelta trečiuoju", "8"),
                          ("penki kvadratu", "25"),
                          ("minus du kubu", "-8"),
                          ("septyniolika plius devyniasdešimt", "107"),
                          ("vienuolika plius dvylika", "23"),
                          ("minus vienas", "-1"),
                          ("skliaustai du plius keturi kart trys", "18"),
                          ("skliaustai du minus keturi dalinti du", "-1"),
                          ("dvi ketvirtosios", "0.5"),
                          ("trys milijonai keturi šimtai tūkstančių šimtas dešimt", "3400110"),
                          ("tūkstantis", "1000"),
                          ("du tūkstančiai šimtas dešimt", "2110"),
                          ("milijonas", "1000000"),
                          ("du kablelis penki", "2.5"),
                          ("šeši padalint iš dviejų", "3"),
                          ("šeši padalint du", "3"),
                          ("penki plius šeši padalint iš dviejų", "8"),
                          ("penki plius šeši kart septyni", "47"),
                          ("du šimtai dvidešimt vienas kart keturi", "884"),
                          ("dvidešimt du plius trys", "25"),
                          ("du plius trys", "5"),
                          ("dešimt plius trys", "13"),
                          ("dešimt minus trys", "7"),
                          ("penki padalinta iš dviejų", "2.5"),
                          ("tūkstantis šešiasdešimt penki", "1065"),
                          ("du plius du kart penki", "12"),
                          ("skliausteliuose du plius du kart penki", "20"),
                          ("skliausteliuose trys minus du kart penki", "5"),
                          ("du plius du apskliausta kart penki", "20"),
                          ("du plius du kart penki visa tai apskliausta plius devyni kart du", "30"),
                          ("du pakelta šeštuoju kart penki", "320"),
                          ("ketvirtojo laipsnio šaknis iš dviejų šimtų penkiasdešimt šešių", "4"),
                          ("vienas sveikas viena antroji", "1.5"),
                          ("dvylika plius šešiasdešimt penki apskliausta pakelta trečiuoju", "456533"),
                          ("šaknis iš šešiolikos plius du", "6"),
                          ("šaknis iš dvylika plius keturi", "4"),
                          ("du dalinti iš du pakelti laipsniu penki", "0.0625")
                          ])
class TestResultParser:
    @classmethod
    def setup_class(cls):
        cls.cfg = Calculator(file="data/calc/grammar.cfg")
        cls.parser = ResultParser(leaves_map=cls.cfg.leaves_map())

    def test_parse(self, txt, exp):
        res, ok = parse(self.cfg, self.parser, txt)
        assert ok
        assert exp == res


@pytest.mark.parametrize("txt,exp",
                         [("du plius du kart penki visa tai apskliausta plius devyni kart du",
                           "\\left( 2 + 2 \\cdot 5 \\right) + 9 \\cdot 2"),
                          ("du minus penktuoju laipsniu", "2^{-5}"),
                          ("du minus penktuoju laipsniu", "2^{-5}"),
                          ("trys šimtuoju", "3^{100}"),
                          ("du pakelta trečiuoju", "2^{3}"),
                          ("penki kvadratu", "5^{2}"),
                          ("minus du kubu", "-2^{3}"),
                          ("du tūkstantuoju", "2^{1000}"),
                          ("du milijonu", "2^{1000000}"),
                          ("septyniolika plius devyniasdešimt", "17 + 90"),
                          ("minus skliaustai du plius keturi", "-\\left( 2 + 4 \\right)"),
                          ("minus vienas", "-1"),
                          ("skliaustai du plius keturi dalinti du", "\\frac{\\left( 2 + 4 \\right)}{2}"),
                          ("du", "2"),
                          ("du plius trys", "2 + 3"),
                          ("tūkstantis", "1000"),
                          ("milijonas", "1000000"),
                          ("dešimt plius trys", "10 + 3"),
                          ("dvidešimt du plius trys", "22 + 3"),
                          ("dešimt minus trys", "10 - 3"),
                          ("du kablelis penki", "2.5"),
                          ("du kablelis penki plius keturi", "2.5 + 4"),
                          ("dvi ketvirtosios", "\\frac{2}{4}"),
                          ("du tūkstančiai šimtas dešimt", "2110"),
                          ("šeši padalint iš dviejų", "\\frac{6}{2}"),
                          ("šeši padalint du", "\\frac{6}{2}"),
                          ("penki plius šeši padalint iš dviejų", "5 + \\frac{6}{2}"),
                          ("trys milijonai keturi šimtai tūkstančių šimtas dešimt", "3400110"),
                          ("du šimtai dvidešimt vienas kart keturi", "221 \\cdot 4"),
                          ("penki plius šeši kart septyni", "5 + 6 \\cdot 7"),
                          ("skliaustai du minus keturi dalinti du", "\\frac{\\left( 2 - 4 \\right)}{2}"),
                          ("skliaustai du plius keturi kart trys", "\\left( 2 + 4 \\right) \\cdot 3"),
                          ("skliausteliuose du plius du kart penki", "\\left( 2 + 2 \\right) \\cdot 5"),
                          ("du plius du apskliausta kart penki", "\\left( 2 + 2 \\right) \\cdot 5"),
                          ("du pakelta šeštuoju kart penki", "2^{6} \\cdot 5"),
                          ("ketvirtojo laipsnio šaknis iš keturiolikos", "\\sqrt[4]{14}"),
                          ("dvidešimt septintojo laipsnio šaknis iš septyniolikos", "\\sqrt[27]{17}"),
                          ("vienas sveikas viena antroji", "1 \\frac{1}{2}"),
                          ("dvylika plius šešiasdešimt penki apskliausta pakelta trečiuoju",
                           "\\left( 12 + 65 \\right)^{3}"),
                          ("šaknis iš dvylikos plius du", "\\sqrt{12} + 2"),
                          ("šaknis iš dvylika plius du", "\\sqrt{12 + 2}"),
                          ("šaknis iš tūkstančio", "\\sqrt{1000}"),
                          ("du sveiki keturios penktosios", "2 \\frac{4}{5}"),
                          ("du dalinti iš du pakelti laipsniu penki", "\\frac{2}{2^{5}}"),
                          ])
class TestEqParser:
    @classmethod
    def setup_class(cls):
        cls.cfg = Calculator(file="data/calc/grammar.cfg")
        cls.parser = EqParser(leaves_map=cls.cfg.leaves_map())

    def test_parse(self, txt, exp):
        res, ok = parse(self.cfg, self.parser, txt)
        assert ok
        assert res == exp


def parse(cfg, parser, txt: str) -> (str, bool):
    tree, ok = cfg.parse(txt)
    if not ok:
        return "", False
    elif tree is None:
        return "", False
    return parser.parse(tree), True
