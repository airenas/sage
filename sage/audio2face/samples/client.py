from __future__ import print_function

import grpc

from sage.audio2face.proto import audio2face_pb2_grpc, audio2face_pb2
from sage.logger import logger


def put_file(stub):
    logger.info("put_file")
    request = audio2face_pb2.PushAudioRequest()
    request.audio_data = "Olia, olia".encode('utf-8')
    request.samplerate = 16000
    request.instance_name = "G1"
    request.block_until_playback_is_finished = True
    print("Sending audio data...")
    response = stub.PushAudio(request)
    if response.success:
        print("SUCCESS")
    else:
        print(f"ERROR: {response.message}")


def pass_stream(stub):
    logger.info("put_file")

    def make_generator():
        start_marker = audio2face_pb2.PushAudioRequestStart(
            samplerate=16000,
            instance_name="G2",
            block_until_playback_is_finished=True,
        )
        # At first, we send a message with start_marker
        yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)
        # Then we send messages with audio_data
        for i in range(10):
            yield audio2face_pb2.PushAudioStreamRequest(audio_data=("Olia, OLia %d " % i).encode('utf-8'))

    request_generator = make_generator()
    print("Sending audio data...")
    response = stub.PushAudioStream(request_generator)
    if response.success:
        print("SUCCESS")
    else:
        print(f"ERROR: {response.message}")


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        try:
            stub = audio2face_pb2_grpc.Audio2FaceStub(channel)
            print("-------------- Put file --------------")
            put_file(stub)
            print("-------------- Pass stream --------------")
            pass_stream(stub)
        except BaseException as err:
            logger.error(err)


if __name__ == '__main__':
    logger.info("Starting fake A2F client")
    run()
