import math

from sage.api.data import Data, DataType, Sender
from sage.cfg.parser import UnknownLeave
from sage.logger import logger


def round_number(num):
    value = float(num)
    if value == round(value):
        if value > 1000000000:
            return "labai didelis skaičius"
        if value < -1000000000:
            return "labai didelis neigiamas skaičius"
        if value < 0:
            return "minus %s" % str(round(-value))
        return str(round(value))
    if abs(value) < 0.001:
        return "praktiškai nulis"

    # truncate last number after comma
    def truncate(num):
        res = str(num)
        dp = res.find('.')
        if dp > -1 and len(res) > dp + 4:
            res = res[:dp + 4]
        return res.rstrip("0")

    if value < 0:
        return "minus %s" % truncate(-value)
    return truncate(value)


class CalculatorBot:
    def __init__(self, cfg, parser, eq_maker, eq_parser, out_func):
        self.__eq_parser = eq_parser
        self.__cfg = cfg
        self.__out_func = out_func
        self.__parser = parser
        self.__eq_maker = eq_maker
        logger.info("Init CalculateBot")

    def process(self, txt: str):
        logger.debug("got %s " % txt)
        self.__out_func(Data(in_type=DataType.STATUS, data="thinking"))
        ## resend input to user
        self.__out_func(Data(in_type=DataType.TEXT, data=txt, who=Sender.USER))
        try:
            tree, ok = self.__cfg.parse(txt)
            if not ok:
                self.__out_func(Data(in_type=DataType.STATUS, data="saying"))
                self.__out_func(Data(in_type=DataType.TEXT, data="Nesuprantu"))
            elif tree is None:
                self.__out_func(Data(in_type=DataType.STATUS, data="saying"))
                self.__out_func(Data(in_type=DataType.TEXT, data="Pabaikite išraišką"))
            else:
                res = self.__parser.parse(tree)
                eq_res = self.__eq_parser.parse(tree)
                eq_svg = self.__eq_maker.prepare(eq_res)
                self.__out_func(Data(in_type=DataType.STATUS, data="saying"))
                self.__out_func(Data(in_type=DataType.SVG, data=eq_svg, who=Sender.BOT, data2=res))
                self.__out_func(Data(in_type=DataType.TEXT_RESULT, data=round_number(res), who=Sender.BOT))
        except UnknownLeave as err:
            logger.error(err)
            self.__out_func(Data(in_type=DataType.TEXT, data="Nežinau žodžio %s" % err.string, who=Sender.BOT))
        except BaseException as err:
            logger.error(err)
            self.__out_func(Data(in_type=DataType.TEXT, data="Deja, kažkokia klaida!", who=Sender.BOT))

        self.__out_func(Data(in_type=DataType.STATUS, data="waiting"))
