import grpc

from sage.audio2face.proto import audio2face_pb2_grpc, audio2face_pb2
from sage.logger import logger


class A2FPlayer:
    def __init__(self, url, face_name):
        logger.info("Init Audio2Face Player, URL=%s" % url)
        self.url = url
        self.face_name = face_name

    def play(self, audio_data):
        with grpc.insecure_channel(self.url) as channel:
            stub = audio2face_pb2_grpc.Audio2FaceStub(channel)
            try:
                self.pass_stream(stub, audio_data)
            except BaseException as err:
                logger.error(err)

    def pass_stream(self, stub, audio_data):
        logger.info("pass stream to audio2face")

        def make_generator():
            chunk_size = 10000  # bytes # audio_data.frame_rate // 10
            start_marker = audio2face_pb2.PushAudioRequestStart(
                samplerate=audio_data.frame_rate,
                instance_name=self.face_name,
                block_until_playback_is_finished=True,
            )
            # At first, we send a message with start_marker
            yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)

            data = audio_data.raw_data
            # Then we send messages with audio_data
            for i in range(len(data) // chunk_size + 1):
                # time.sleep(sleep_between_chunks)
                chunk = data[i * chunk_size: i * chunk_size + chunk_size]
                yield audio2face_pb2.PushAudioStreamRequest(audio_data=chunk)

        request_generator = make_generator()
        print("Sending audio data...")
        response = stub.PushAudioStream(request_generator)
        if response.success:
            logger.info("Audio send")
        else:
            logger.error(response.message)
