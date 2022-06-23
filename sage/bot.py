from sage.api.data import Data, DataType
from sage.logger import logger


class CalculatorBot:
    def __init__(self, out_func):
        logger.info("Init CalculateBot")
        self.out_func = out_func

    def process(self, txt: str):
        logger.debug("got %s " % txt)
        self.out_func(Data(in_type=DataType.STATUS, data="thinking"))
        self.out_func(Data(in_type=DataType.TEXT, data="Gavau: " + txt))
        self.out_func(Data(in_type=DataType.STATUS, data="waiting"))
