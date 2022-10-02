import socket

from client.request import Request
from client import errors
from client.do_request import do_request
import argparse
import sys

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
parser.add_argument(
    "-H",
    "--headers",
    type=str,
    nargs="+",
    help="add headers in request",
    dest="my_headers",
)
parser.add_argument("-t", "--timeout", type=str, help="reset timeout")
parser.add_argument("-l", "--host", type=str,
                    help="custom host, default value is None")
parser.add_argument(
    "-P",
    "--path",
    type=str,
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
    if arguments.data:
        new_request.set_body(arguments.data)
    return new_request


def show_response(
    recipient_response: Response,
    user_args: argparse.Namespace,
) -> None:
    if user_args.output:
        with open(args.output, 'bw') as file:
            file.write(response.body.encode(response.charset))
    else:
        answer = [
            f'{bytes(recipient_response).decode()}',
            '\r\n',
            recipient_response.body,
        ]
        sys.stdout.write("\r\n".join(answer))


args = parser.parse_args()
request = prepare_request(args)

try:
    response = do_request(request, 1000, 10)
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
