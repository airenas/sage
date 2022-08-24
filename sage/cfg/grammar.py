import nltk

from sage.logger import logger


class Calculator:
    def __init__(self, file):
        grammar = nltk.data.load(file, format="cfg")
        logger.info("Init Grammar")
        self.__parser = nltk.ChartParser(grammar=grammar)

    def parse(self, txt: str):
        logger.debug("got %s " % txt)
        try:
            res = list(self.__parser.parse(txt.split()))
        except BaseException as err:
            logger.critical(err, exc_info=True)
            return None, False
        if len(res) > 0:
            return res[0], True
        return None, True
