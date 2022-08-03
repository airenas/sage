from sage.api.data import Data, DataType, Sender
from sage.cfg.parser import UnknownLeave
from sage.logger import logger


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
                self.__out_func(Data(in_type=DataType.SVG, data=eq_svg, who=Sender.BOT))
                self.__out_func(Data(in_type=DataType.TEXT, data=res, who=Sender.BOT))
        except UnknownLeave as err:
            logger.error(err)
            self.__out_func(Data(in_type=DataType.TEXT, data="Nežinau žodžio %s" % err.string, who=Sender.BOT))
        except BaseException as err:
            logger.error(err)
            self.__out_func(Data(in_type=DataType.TEXT, data="Deja, kažokia klaida!", who=Sender.BOT))

        self.__out_func(Data(in_type=DataType.STATUS, data="waiting"))
