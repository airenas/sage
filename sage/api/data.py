import uuid
from enum import Enum
from typing import Any


class Sender(Enum):
    USER = 1
    BOT = 2

    def to_str(self):
        if self == Sender.USER:
            return "USER"
        else:
            return "BOT"


class DataType(Enum):
    TEXT = 1
    AUDIO = 2
    STATUS = 3
    SVG = 4


class Data:
    def __init__(self, in_type: DataType, who: Sender = Sender.BOT, data: Any = None):
        self.type = in_type
        self.data = data
        self.who = who
        self.id = str(uuid.uuid1())
