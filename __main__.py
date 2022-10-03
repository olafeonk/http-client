import socket

from client.request import Request
from client import errors
from client.do_request import do_request
import argparse
import sys
import base64

from client.response import Response

MAX: int = 10

parser = argparse.ArgumentParser(description="HTTP(S) - Client")
parser.add_argument("-d", "--data", type=str, help="data for request")
parser.add_argument("-m", "--method",
                    type=str,
                    help="choose request method:"
                         "GET|"
                         "POST|"
                         "PUT|"
                         "PATCH|"
                         "OPTIONS|"
                         "DELETE",
                    )
parser.add_argument("-u", "--url", type=str, help="Contains URL")
parser.add_argument("-c", "--cookie", type=str, help="add cookie")
parser.add_argument("-O", "--output", type=str, help="print answer in file")
parser.add_argument("-k", "--keepalive", action='store_true', help="support keepalive")
parser.add_argument(
    "-H",
    "--headers",
    type=str,
    nargs="+",
    help="add headers in request",
    dest="my_headers",
)
parser.add_argument("-U", "--user", help='basic authorization example --user user:password')
parser.add_argument("-t", "--timeout", type=int, default=5, help="reset timeout")
parser.add_argument("-l", "--host", type=str,
                    help="custom host, default value is None")
parser.add_argument(
    "-P",
    "--path",
    type=str,
    nargs='*',
    help="setup path, should start with </>, haven't default path",
)


def prepare_request(arguments: argparse.Namespace) -> Request:
    new_request = Request()
    if arguments.url is not None:
        new_request.set_url(arguments.url)
    elif arguments.host is not None:
        new_request.set_host(arguments.host)
    else:
        raise AttributeError
    if arguments.method:
        new_request.set_method(arguments.method)
    if arguments.path:
        new_request.set_path(arguments.path)
    if arguments.my_headers:
        headers = {}
        for header in arguments.my_headers:
            separator_ind = header.find(":")
            key = header[0:separator_ind]
            value = header[separator_ind + 1::].strip()
            headers[key] = value
        new_request.set_headers(headers)
    if arguments.cookie:
        new_request.set_header('Cookie', arguments.cookie)
    if arguments.keepalive:
        new_request.set_header('Connection', 'Keep-Alive')
        new_request.set_header('Keep-Alive', f'timeout={arguments.timeout}')
    if arguments.data:
        new_request.set_body(arguments.data)
    if arguments.user:
        new_request.set_header('Authorization', f'Basic {base64.b64decode(bytes(arguments.user))}')
    new_request.set_current_path()
    return new_request


def show_response(
    recipient_responses: list[Response],
    user_args: argparse.Namespace,
) -> None:
    for recipient_response in recipient_responses:
        if user_args.output:
            with open(args.output, 'bw') as file:
                file.write(recipient_response.body.encode(recipient_response.charset))
        else:
            answer = [
                recipient_response.body,
            ]
            sys.stdout.write("\r\n".join(answer))
        if user_args.output:
            file.write(b'\n')
        else:
            sys.stdout.write('\n')


args = parser.parse_args()
request = prepare_request(args)
try:
    response = do_request(request, args.timeout, 10)
    show_response(response, args)
except errors.MaxDirectionsError:
    sys.stdout.write(errors.MaxDirectionsError.message)
    exit(1)
except errors.HTTPSClientError:
    sys.stdout.write(errors.ConnectError.message)
    exit(1)
except socket.gaierror:
    sys.stdout.write(errors.ConnectError.message)
    exit(1)