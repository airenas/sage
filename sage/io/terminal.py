from sage.api.data import Data, DataType, Sender
from sage.logger import logger


class TerminalInput:
    def __init__(self, msg_func):
        logger.info("Init terminal input")
        self.msg_func = msg_func

    def start(self):
        while True:
            # print("You: ", end="")
            txt = input()
            self.msg_func(Data(in_type=DataType.TEXT, who=Sender.USER, data=txt))


class TerminalOutput:
    def __init__(self):
        logger.info("Init terminal output")

    def process(self, d: Data):
        if d.type == DataType.TEXT:
            print("%s: %s" % (d.who, d.data))
        elif d.type == DataType.STATUS:
            print("%s: %s" % (d.who, d.data))
        else:
            logger.warning("Don't know what to do with %s data" % d.type)
