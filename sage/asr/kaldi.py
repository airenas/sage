import datetime as dt
import queue
import threading
from random import randrange
from time import sleep

from sage.api.data import Data, DataType, Sender
from sage.logger import logger


class Kaldi:
    def __init__(self, msg_func):
        logger.info("Init Kaldi wrapper")
        self.__audio_queue: queue.Queue[bytes] = queue.Queue(maxsize=500)
        self.__txt_queue: queue.Queue[str] = queue.Queue(maxsize=500)

        self.recognized_value = ""
        self.working = False
        self.last_gen_type = 0
        self.msg_func = msg_func
        self.next = None

    def add(self, data: bytes):
        logger.debug("add play data of len %d" % len(data))
        self.__audio_queue.put(data)

    def event(self, data: str):
        if data == "AUDIO_START":
            self.last_gen_type = 0
            self.recognized_value = ""
            self.working = True
            self.next = dt.datetime.now() + dt.timedelta(milliseconds=200)
        else:
            self.working = False

    def start(self):
        threading.Thread(target=self.__recognized, daemon=True).start()
        while True:
            self.__process(self.__audio_queue.get())

    def __recognized(self):
        while True:
            self.__process_recognized(self.__txt_queue.get())

    def __process(self, data: bytes):
        now = dt.datetime.now()
        if self.next > now:
            return
        self.next = dt.datetime.now() + dt.timedelta(milliseconds=500)
        arr_num = ["du", "trys", "penki", "šimtas", "milijonas"]

        arr_op = ["kart", "plius", "minus", "minus", "dalint"]
        if self.last_gen_type % 2 == 0:
            self.last_gen_type = 1
            i = randrange(0, len(arr_num))
            self.recognized_value = (self.recognized_value + " " + arr_num[i]).strip()
        else:
            self.last_gen_type = 0
            i = randrange(0, len(arr_op))
            self.recognized_value = (self.recognized_value + " " + arr_op[i]).strip()
        if self.working:
            a = self.recognized_value + "..."
        else:
            a = self.recognized_value
        self.__txt_queue.put(a)

    def __process_recognized(self, data: str):
        self.msg_func(Data(in_type=DataType.TEXT, who=Sender.RECOGNIZER, data=data))

    def stop(self):
        pass
