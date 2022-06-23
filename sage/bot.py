from sage.api.data import Data, DataType
from sage.logger import logger


class CalculatorBot:
    def __init__(self, cfg, out_func):
        self.cfg = cfg
        self.out_func = out_func
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
            self.out_func(Data(in_type=DataType.TEXT, data="Gavau: %d" % len(tree)))
        self.out_func(Data(in_type=DataType.STATUS, data="waiting"))
