from __future__ import annotations

import sys
from client.methods import Method
from client import errors
from dataclasses import dataclass, field
from yarl import URL


@dataclass
class Request:
    current_path: str = '/'
    method: Method = Method.GET
    scheme: str = 'https'
    url: URL = URL('')
    paths: list = field(default_factory=list)
    protocol: str = 'HTTP/1.1'
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b''
    number_current_path = 0

    def __post_init__(self: Request) -> None:
        self.headers["Host"] = URL(self.url).host
        if "Connection" not in self.headers:
            self.headers["Connection"] = "close"
        if "Content-Length" not in self.headers:
            self.headers["Content-Length"] = str(len(self.body))

    def set_host(self: Request, host: str) -> None:
        self.url = URL(f'{self.scheme}://{host}{self.current_path}')
        self.headers["Host"] = host

    def set_url(self: Request, url: str) -> None:
        self.url = URL(url)
        self.headers["Host"] = URL(url).host
        self.scheme = URL(url).scheme
        self.paths = [URL(url).path]

    def set_headers(self: Request, headers: dict[str, str]) -> None:
        for header in headers.keys():
            self.headers[header] = headers.get(header)

    def set_header(self: Request, header: str, value: str) -> None:
        self.headers[header] = value

    def set_body(self: Request, body: str) -> None:
        self.body = body.encode()
        self.headers['Content-Length'] = str(len(body))

    def set_path(self: Request, paths: list[str]) -> None:
        self.paths = paths

    def set_method(self: Request, method: str) -> None:
        try:
            for req_type in Method:
                if req_type.value.lower() == method:
                    self.method = req_type
                    return
            raise errors.IncorrectMethodTypeError()
        except errors.IncorrectMethodTypeError as e:
            sys.stdout.write(e.message)
            exit(1)

    def set_current_path(self):
        if self.number_current_path < len(self.paths):
            self.current_path = self.paths[self.number_current_path]
        self.number_current_path += 1
        if self.number_current_path == len(self.paths):
            self.set_header('Connection', 'close')

    def __bytes__(self: Request) -> bytes:
        request = [f"{self.method.value} {self.current_path} {self.protocol}".encode()]
        for header, value in self.headers.items():
            request.append(f"{header}: {value}".encode())
        request.append(b"")
        request.append(self.body)
        return b"\r\n".join(request)

    @property
    def host(self: Request) -> str | None:
        return self.url.host
