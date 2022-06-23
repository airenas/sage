import io

from pydub import AudioSegment
from pydub.playback import play

from sage.api.data import Data, DataType
from sage.logger import logger


class VoiceOutput:
    def __init__(self, tts):
        logger.info("Init voice output")
        self.tts = tts

    def process(self, d: Data):
        if d.type == DataType.TEXT:
            try:
                res = self.tts.convert(d.data)
                song = AudioSegment.from_file(io.BytesIO(res), format="mp3")
                play(song)
            except BaseException as err:
                logger.error(err)
        elif d.type == DataType.STATUS:
            pass
        else:
            logger.warning("Don't know what to do with %s data" % d.type)
