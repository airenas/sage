from sage.api.data import Data, DataType, Sender
from sage.logger import logger


class CalculatorBot:
    def __init__(self, cfg, parser, out_func):
        self.cfg = cfg
        self.out_func = out_func
        self.__parser = parser
        logger.info("Init CalculateBot")

    def process(self, txt: str):
        logger.debug("got %s " % txt)
        self.out_func(Data(in_type=DataType.STATUS, data="thinking"))
        tree, ok = self.cfg.parse(txt)
        if not ok:
            self.out_func(Data(in_type=DataType.TEXT, data="Nesuprantu"))
        elif tree is None:
            self.out_func(Data(in_type=DataType.TEXT, data="Pabaikite išraišką"))
        else:
            res = self.__parser.parse(tree)
            self.out_func(Data(in_type=DataType.TEXT, data=res, who=Sender.BOT))
        self.out_func(Data(in_type=DataType.STATUS, data="waiting"))
