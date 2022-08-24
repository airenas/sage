import pytest


@pytest.mark.parametrize("txt,exp",
                         [
                             ("-1.00199", "minus 1.001"),
                             ("1.2222222222", "1.222"),
                             ("2", "2"),
                             ("100000000", "100000000"),
                             ("1.22", "1.22"),
                             ("1.2", "1.2"),
                             ("1.0", "1"),
                             ("2000000000", "labai didelis skaičius"),
                             ("-2000000000", "labai didelis neigiamas skaičius"),
                             ("0.001", "0.001"),
                             ("0.00049", "praktiškai nulis"),
                             ("-1.0", "minus 1"),
                             ("-1.00199", "minus 1.001"),
                             ("1.00199", "1.001"),
                         ])
class TestRound:
    def test_round(self, txt, exp):
        res = round_number(txt)
        assert res == exp


from sage.bot import round_number
