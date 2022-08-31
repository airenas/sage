import io

from pydub import AudioSegment
from pydub.playback import play

from sage.api.data import Data, DataType, Sender
from sage.logger import logger


class PCPlayer:
    def __init__(self):
        logger.info("Init PC audio player")

    def play(self, audio_data):
        play(audio_data)


class VoiceOutput:
    def __init__(self, tts, player):
        logger.info("Init voice output")
        self.tts = tts
        self.player = player

    def process(self, d: Data):
        if d.type == DataType.TEXT or d.type == DataType.TEXT_RESULT:
            if d.who == Sender.BOT:
                try:
                    res = self.tts.convert(d.data)
                    song = AudioSegment.from_file(io.BytesIO(res), format="mp3")
                    self.player.play(song)
                except BaseException as err:
                    logger.error(err)
        elif d.type == DataType.STATUS or d.type == DataType.SVG or d.who == Sender.RECOGNIZER:
            pass
        else:
            logger.warning("Don't know what to do with %s - %s" % (d.type, d.data))
