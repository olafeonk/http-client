from __future__ import annotations
import re
from dataclasses import dataclass, field

CRLF: str = '\r\n'


@dataclass
class Response:
    body: str = ''
    charset: str = ''
    code: int = -1
    location: str = None
    headers: dict[str, str] = field(default_factory=dict)
    protocol: float = 1.0

    def __bytes__(self: Response) -> bytes:
        response = [f"HTTP/{self.protocol} {self.code} OK"]
        for header, value in self.headers.items():
            response.append(f"{header}: {value}")
        return '\r\b'.join(response).encode()

    @classmethod
    def parse(cls: Response, data: bytes) -> list[Response]:
        response = data.decode("UTF-8")
        code = (re.search(r" \d* ", response)).group(0)
        protocol = (re.search(r'[\d.]* ', response)).group(0)
        head = response.split(f"{CRLF}{CRLF}")[0]

        charset = "utf-8"
        headers = {}
        location = ""
        for string in head.split(f"{CRLF}"):
            search_headers = re.search(r'(?P<header>[a-zA-Z-]*): '
                                       r'' r'(?P<value>[0-9\s\w,.;=/:-]*)', string)
            if search_headers is not None:
                headers[search_headers.group("header")] = search_headers.group("value")
                if search_headers.group("header") == "Content-Type" or search_headers.group("header") == "content-type":
                    search_charset = re.search(r"[a-zA-z/]*; " r"charset="
                                               r"(?P<charset>" r"[\w-]*)",
                                               search_headers.group("value"))
                    charset = 'utf-8' if search_charset is None else search_charset.group("charset")
                if search_headers.group("header") == "Location" or search_headers.group("header") == "location":
                    location = search_headers.group("value")
        if headers.get('Transfer-Encoding') != 'chunked':
            body = response[response.find(f'{CRLF}{CRLF}') + 4:].encode('utf-8')[:int(headers.get('Content-Length'))]
            curr_response = response[response.find(f'{CRLF}{CRLF}') + 4 + len(body.decode('utf-8')):].encode('utf-8')
            if curr_response:
                responses = [cls(
                    body=body.decode('utf-8'),
                    charset=charset,
                    code=int(code),
                    location=location,
                    protocol=float(protocol),
                    headers=headers,
                )]
                responses.extend(cls.parse(curr_response))
                return responses
            return [cls(
                body=body.decode('utf-8'),
                charset=charset,
                code=int(code),
                location=location,
                protocol=float(protocol),
                headers=headers,
            )]
        body = b''
        raw_body = response[response.find(f"{CRLF}{CRLF}") + 4:].encode('utf-8')
        ind = 0
        while True:
            chunk_length = int(raw_body[ind:ind + raw_body[ind:].find(CRLF.encode('utf-8'))], 16)
            ind += raw_body[ind:].find(CRLF.encode('utf-8')) + 2
            body += raw_body[ind: ind + chunk_length]
            ind += chunk_length
            ind += 2
            if chunk_length == 0:
                curr_response = raw_body[ind:]
                if curr_response:
                    responses = [cls(
                        body=body.decode('utf-8'),
                        charset=charset,
                        code=int(code),
                        location=location,
                        protocol=float(protocol),
                        headers=headers,
                    )]
                    responses.extend(cls.parse(curr_response.encode('utf-8')))
                    return responses
                return [cls(
                    body=body.decode('utf-8'),
                    charset=charset,
                    code=int(code),
                    location=location,
                    protocol=float(protocol),
                    headers=headers,
                )]
