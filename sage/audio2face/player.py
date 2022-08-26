import grpc
import numpy as np
from pydub import AudioSegment

from sage.audio2face.proto import audio2face_pb2_grpc, audio2face_pb2
from sage.logger import logger


# from https://stackoverflow.com/a/66922265/701939
def pydub_to_np(audio: AudioSegment) -> (np.ndarray, int):
    """
    Converts pydub audio segment into np.float32 of shape [duration_in_seconds*sample_rate, channels],
    where each value is in range [-1.0, 1.0].
    Returns tuple (audio_np_array, sample_rate).
    """
    max_v = 1 << (8 * audio.sample_width - 1)
    return np.array(audio.get_array_of_samples(),
                    dtype=np.float32).reshape((-1, audio.channels)) / max_v, audio.frame_rate


class A2FPlayer:
    def __init__(self, url, face_name):
        logger.info("Init Audio2Face Player, URL=%s, name=%s" % (url, face_name))
        self.url = url
        self.face_name = face_name

    def play(self, audio_data):
        with grpc.insecure_channel(self.url) as channel:
            stub = audio2face_pb2_grpc.Audio2FaceStub(channel)
            try:
                self.pass_stream(stub, audio_data)
            except BaseException as err:
                logger.error(err)

    def pass_stream(self, stub, audio_data: AudioSegment):
        logger.debug("pass stream to audio2face")
        data, sample_rate = pydub_to_np(audio_data)

        def make_generator():
            chunk_size = sample_rate // 10
            start_marker = audio2face_pb2.PushAudioRequestStart(
                samplerate=sample_rate,
                instance_name=self.face_name,
                block_until_playback_is_finished=True,
            )
            # At first, we send a message with start_marker
            yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)

            for i in range(len(data) // chunk_size + 1):
                chunk = data[i * chunk_size: i * chunk_size + chunk_size]
                yield audio2face_pb2.PushAudioStreamRequest(audio_data=chunk.tobytes())

        request_generator = make_generator()
        response = stub.PushAudioStream(request_generator)
        if response.success:
            logger.info("audio was sent")
        else:
            logger.error(response.message)
