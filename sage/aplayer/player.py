import queue

import pyaudio

from sage.logger import logger


class Player:
    def __init__(self, rate: int = 48000):
        self.__p = pyaudio.PyAudio()
        logger.info("Init Player. rate %d" % rate)
        # self.__stream = self.__p.open(format=pyaudio.paInt16, channels=1, rate=rate, output=True)
        self.__audio_queue: queue.Queue[bytes] = queue.Queue(maxsize=500)
        self.rate = rate
        self.f = open("foo.pcm", "wb")

    def add(self, data: bytes):
        logger.debug("add play data of len %d" % len(data))
        self.__audio_queue.put(data)

    def start(self):
        while True:
            self.__play(self.__audio_queue.get())

    def __play(self, data: bytes):
        try:
            self.f.write(data)
            logger.debug("play %d data array" % len(data))
            stream = self.__p.open(format=pyaudio.paInt16, channels=1, rate=self.rate, output=True)
            stream.write(data)
            stream.stop_stream();
            stream.close()
            logger.debug("play %d data array" % len(data))
        except BaseException as err:
            logger.error(err)

    def stop(self):
        self.__p.terminate()
