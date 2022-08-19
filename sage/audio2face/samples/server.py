from concurrent import futures

import grpc

from sage.audio2face.proto import audio2face_pb2_grpc, audio2face_pb2
from sage.logger import logger


class FakeServicer(audio2face_pb2_grpc.Audio2FaceServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        logger.info("Init servicer")

    def PushAudio(self, request, context):
        instance_name = request.instance_name
        samplerate = request.samplerate
        block_until_playback_is_finished = request.block_until_playback_is_finished
        audio_data = str(request.audio_data)
        logger.info("data: %d, rate: %d" % (audio_data, samplerate))
        return audio2face_pb2.PushAudioResponse(success=True, message="")

    def PushAudioStream(self, request_iterator, context):
        first_item = next(request_iterator)
        if not first_item.HasField("start_marker"):
            return audio2face_pb2.PushAudioResponse(
                success=False, message="First item in the request should containt start_marker"
            )
        instance_name = first_item.start_marker.instance_name
        samplerate = first_item.start_marker.samplerate
        block_until_playback_is_finished = first_item.start_marker.block_until_playback_is_finished
        logger.info("PushAudioStream request: [instance_name = {} ; samplerate = {}]".format(instance_name, samplerate))

        for item in request_iterator:
            audio_data = item.audio_data
            logger.info(
                "Got data len %d" % len(audio_data))

        logger.info("PushAudioStream request -- DONE")
        return audio2face_pb2.PushAudioResponse(success=True, message="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio2face_pb2_grpc.add_Audio2FaceServicer_to_server(
        FakeServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("Started")
    server.wait_for_termination()


if __name__ == '__main__':
    logger.info("Starting fake A2F simple server")
    serve()
