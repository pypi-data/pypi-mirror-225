from grpc import (RpcError, StatusCode)


class RpcException(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.code_msg = ". Error code: {}".format(status_code.value[0])

    def __str__(self):
        return self.message + self.code_msg


def handle_grpc_error(ex: RpcError, client_name):
    status_code = ex.code()
    if status_code == StatusCode.UNAVAILABLE:
        raise RpcException("Confirm {} is running".format(client_name), status_code) from None
    if status_code == StatusCode.UNAUTHENTICATED:
        raise RpcException("Invalid authentication", status_code) from None
    if status_code == StatusCode.RESOURCE_EXHAUSTED:
        raise RpcException("Data too big. Try smaller chunks", status_code)
    else:
        raise RpcError(ex) from None
