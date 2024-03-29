from collections import OrderedDict
from typing import Dict, List, Any

import nltk

from sage.cfg.parser import ParseError
from sage.logger import logger


class UnknownWord(ParseError):
    """Raised when the word is unknown to the grammar"""

    def __init__(self, word):
        self.message = "Unknown word `%s`" % word
        self.word = word
        super().__init__(self.message)


def get_leaves(grammar):
    res = []
    productions = grammar.productions()
    for pr in productions:
        r = pr.rhs()
        for t in r:
            if isinstance(t, str):
                res.append(t)
    return res


def try_get_value(dic, leave):
    for v, k in dic.items():
        if leave.startswith(v):
            return k
    logger.debug("Unknown leave: %s" % leave)
    return 0


def extract_unknown_word(param: str) -> str | None:
    st = 'Grammar does not cover some of the input words'
    if param.startswith(st):
        res = param[len(st):]
        res = res.strip("\"'. :")
        return res
    return None


class Calculator:
    def __init__(self, file):
        self.grammar = nltk.data.load(file, format="cfg")
        logger.info("Init Grammar")
        self.__parser = nltk.ChartParser(grammar=self.grammar)

    def leaves_map(self) -> dict:
        prefixes = OrderedDict()
        add_to_dict(prefixes, ['dešimt'], 10)
        add_to_dict(prefixes, ['vienuolik'], 11)
        add_to_dict(prefixes, ['dvylik'], 12)
        add_to_dict(prefixes, ['trylik'], 13)
        add_to_dict(prefixes, ['keturiolik'], 14)
        add_to_dict(prefixes, ['penkiolik'], 15)
        add_to_dict(prefixes, ['šešiolik'], 16)
        add_to_dict(prefixes, ['septyniolik'], 17)
        add_to_dict(prefixes, ['aštuoniolik'], 18)
        add_to_dict(prefixes, ['devyniolik'], 19)
        add_to_dict(prefixes, ['dvidešimt'], 20)
        add_to_dict(prefixes, ['trisdešimt'], 30)
        add_to_dict(prefixes, ['keturiasdešimt'], 40)
        add_to_dict(prefixes, ['penkiasdešimt'], 50)
        add_to_dict(prefixes, ['šešiasdešimt'], 60)
        add_to_dict(prefixes, ['septyniasdešimt'], 70)
        add_to_dict(prefixes, ['aštuoniasdešimt'], 80)
        add_to_dict(prefixes, ['devyniasdešimt'], 90)
        add_to_dict(prefixes, ["šimt"], 100)
        add_to_dict(prefixes, ["tūkstan"], 1000)
        add_to_dict(prefixes, ["milijon"], 1000000)
        add_to_dict(prefixes, ['vien', 'pirm'], 1)
        add_to_dict(prefixes, ['du', 'dviej', 'dvi', 'kvadrat', 'antr'], 2)
        add_to_dict(prefixes, ['trys', 'tri', 'kubu', 'kubin', 'treč', 'trej'], 3)
        add_to_dict(prefixes, ['ketur', 'ketvirt'], 4)
        add_to_dict(prefixes, ['penk'], 5)
        add_to_dict(prefixes, ['šeš'], 6)
        add_to_dict(prefixes, ['septyn', 'septin'], 7)
        add_to_dict(prefixes, ['aštuon', 'aštunt'], 8)
        add_to_dict(prefixes, ['devyn', 'devin'], 9)

        res = dict()
        leaves = get_leaves(self.grammar)
        add_to_dict(res,
                    ["plius", 'pridėti', 'atimti', 'minus', 'dalint', 'dalinti', 'dalinta', 'padalint', 'padalinti',
                     'padalinta', 'dauginti', 'dauginta', 'padauginti', 'padauginta', 'kart',
                     "pakelta", 'pakelti', 'laipsniu', 'laipsnio',
                     "iš", "kablelis", "skliaustai", "skliausteliuose", "šaknis", "apskliausta", "sveikas",
                     "sveiki",
                     "vardiklyje", "skliaustuose", "skliausteliai", "atsidaro", "atsidarantys", "atviras",
                     "skliaustelis", "užsidaro", "uždaras", "apskliausti", "šaknies", "šaknys", "pošaknyje",
                     "trupmena", "skaitiklyje", "ir", "visa", "tai"], 0)
        for leave in leaves:
            if leave not in res:
                v = try_get_value(prefixes, leave)
                res[leave] = v
        return res

    def parse(self, txt: str):
        logger.debug("got %s " % txt)
        try:
            res = list(self.__parser.parse(txt.split()))
        except ValueError as err:
            w = extract_unknown_word(str(err))
            if w:
                raise UnknownWord(w)
            logger.critical(err, exc_info=True)
            return None, False
        except BaseException as err:
            logger.critical(err, exc_info=True)
            return None, False
        if len(res) > 0:
            return res[0], True
        return None, True


def add_to_dict(d: Dict, keys: List[str], val: Any):
    for s in keys:
        d[s] = val
