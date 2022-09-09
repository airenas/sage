import requests

from sage.logger import logger


class Replacer:
    def __init__(self, url: str):
        logger.info("Init replacer at %s" % (url))
        self.__url = url

    def convert(self, txt: str) -> str:
        in_data = {'num': txt}
        x = requests.get(self.__url, json=in_data, timeout=10)
        if x.status_code != 200:
            raise Exception("Can't invoke number replacer: " + x.text)
        data = x.json()
        res = data['text']
        logger.debug("replace %s -> %s" % (txt, res))
        return res
