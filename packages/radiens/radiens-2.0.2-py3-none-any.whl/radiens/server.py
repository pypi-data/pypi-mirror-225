import logging
import os
import sys
import threading
import time
from concurrent import futures

import grpc
from radiens.exceptions.grpc_error import handle_grpc_error
import radiens.grpc_radiens.pyradiens_pb2_grpc as pyradiens_pb2_grpc
from radiens.grpc_radiens import (
    common_pb2, pyradiens_pb2)

_logger = logging.getLogger(__name__)
_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                      options=[
    ('grpc.max_send_message_length', 8 * 1024 * 1024),
    ('grpc.max_receive_message_length', 8 * 1024 * 1024)
]
)
PORT = -1

# SpikeServer is the python client API to the Go allegoserver SpikeWorker service
# The SpikeServer handles several python-side functions, including spike sorting,
# I/O to 2nd-class recording files (e.g., open ephys, plexon, neuralynx, etc.),
# and access to numpy & related core python packages for signal processing.


class PyRadiensServer(pyradiens_pb2_grpc.PyRadiensServicer):
    def __init__(self, port):
        _logger.info("Initializing")
        self._port = port

    @property
    def Port(self):
        return self._port

    # ====  life cycle functions
    def Close(self, request, context):
        _logger.info('Close request received')
        worker = threading.Thread(target=close, daemon=False)
        worker.start()
        return common_pb2.StandardReply()

    def Healthcheck(self, request, context):
        _logger.info("Healthcheck")
        return common_pb2.StandardReply()

    # ====  thinly-wrapped python functions
    # def IirFilterDesign(self, request, context):
    #     _logger.info("IIR filter design")
    #     try:
    #         return dsp.iir_design(request)
    #     except Exception as ex:
    #         _logger.error("IirFilterDesign (python) error : {}".format(ex))
    #         raise RuntimeError(ex)

    # ========================================
    # template functions
    # ========================================

    def StreamingRequest(self, request_iterator, context):
        _logger.info("Streaming Request")
        response = []
        for request in request_iterator:
            sum = 0
            for v in request.data:
                sum += v
            response.append(sum)
        return pyradiens_pb2.Reply(data=response)

    def StreamingReply(self, request, context):
        _logger.info("Streaming Reply")
        for v in request.data:
            yield pyradiens_pb2.Reply(data=[v*2])

    def StreamingBidirectional(self, request_iterator, context):
        _logger.info("Streaming Bidirectional")
        for request in request_iterator:
            response = []
            for v in request.data:
                response.append(v*2)
            yield pyradiens_pb2.Reply(data=response)


def close():
    time.sleep(0.1)
    if _server:
        _logger.info('Stopping pyradiens server and exiting its process')
        _server.stop(grace=None)
    sys.exit()


def serve(port):
    pyradiens_pb2_grpc.add_PyRadiensServicer_to_server(PyRadiensServer(port), _server)
    _server.add_insecure_port('[::]:{}'.format(port))
    _logger.info('starting pyradiens service on port %s', port)
    _server.start()
    _logger.info('pyradiens service ready')
    print('launched pyradiens service::{}/{}'.format(os.getpid(), port))
    _server.wait_for_termination()


def main():
    serve(sys.argv[1])


if __name__ == '__main__':
    main()
