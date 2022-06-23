from enum import Enum
from typing import Any


class Sender(Enum):
    USER = 1
    BOT = 2


class DataType(Enum):
    TEXT = 1
    AUDIO = 2
    STATUS = 3


class Data:
    def __init__(self, in_type: DataType, who: Sender = Sender.BOT, data: Any = None):
        self.type = in_type
        self.data = data
        self.who = who
