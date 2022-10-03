from client import errors
from client.request import Request
import socket
from ssl import SSLContext
from client.response import Response


def do_request(
    request: Request,
    timeout: float = 10,
    max_iterations: int = 10,
) -> list[Response]:
    while max_iterations >= 0:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if request.scheme == "https":
            sock = SSLContext().wrap_socket(sock)
        sock.settimeout(timeout)
        max_iterations -= 1
        sock.connect((
            request.host,
            80 if request.scheme == 'http' else 443
        ))
        if request.scheme == "https":
            sock.do_handshake()
        while request.number_current_path <= len(request.paths):
            sock.sendall(bytes(request))
            request.set_current_path()

        obtained_data = b''
        while True:
            data = sock.recv(1024)
            if not data:
                break
            obtained_data += data

        responses = Response.parse(obtained_data)
        sock.close()
        return responses
    raise errors.MaxDirectionsError()
