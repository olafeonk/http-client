from __future__ import annotations
import re
from dataclasses import dataclass, field


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
    def parse(cls: Response, data: bytes) -> Response:
        response = data.decode("UTF-8")
        code = (re.search(r" \d* ", response)).group(0)
        protocol = (re.search(r'[\d.]* ', response)).group(0)
        head, body = response.split("\r\n\r\n")
        charset = "utf-8"
        headers = {}
        location = ""
        for string in head.split("\r\n"):
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
        return cls(
            body=body,
            charset=charset,
            code=int(code),
            location=location,
            protocol=float(protocol),
            headers=headers,
        )
