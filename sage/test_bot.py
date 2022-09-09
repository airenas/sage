import pytest

from sage.bot import round_number


@pytest.mark.parametrize("txt,exp,exp_change",
                         [
                             ("-1.00199", "-1.001", True),
                             ("1.2222222222", "1.222", True),
                             ("2", "2", True),
                             ("100000000", "100000000", True),
                             ("1.22", "1.22", True),
                             ("1.2", "1.2", True),
                             ("1.0", "1", True),
                             ("2000000000", "labai didelis skaičius", False),
                             ("-2000000000", "labai didelis neigiamas skaičius", False),
                             ("0.001", "0.001", True),
                             ("0.00049", "praktiškai nulis", False),
                             ("-1.0", "-1", True),
                             ("-1.00199", "-1.001", True),
                             ("1.00199", "1.001", True),
                         ])
class TestRound:
    def test_round(self, txt, exp, exp_change):
        res, change = round_number(txt)
        assert res == exp
        assert change == exp_change
