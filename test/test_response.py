from client.response import Response
import pytest


@pytest.fixture
def data():
    return (
        'HTTP/1.1 400 OK\r\n'
        'Server: kittenx\r\n'
        'Date: Sat, 26 Dec 2020 11:48:21 GMT\r\n'
        'Content_Type: text/html\r\n'
        'Content-Length: 152\r\n'
        'Connection: close\r\n'
        'X-Frontend: front213218\r\n'
        'Location: blablacar.com\r\n'
        'Access-Control-Expose-Headers: X-Frontend\r\n'
        '\r\n'
        '<html>\r\n'
        '<head><title>400 Bad Request</title></head>\r\n'
        '<body>\r\n'
        '<center><h1>400 Bad Request</h1></center>\r\n'
        '<hr><center>kittenx</center>\r\n'
        '</body>\r\n'
        '</html\r\n>'.encode()
    )


def test_response_parse(data):
    response = Response().parse(data)[0]

    assert response.body == (
        '<html>\r\n'
        '<head><title>400 Bad Request</title></head>\r\n'
        '<body>\r\n'
        '<center><h1>400 Bad Request</h1></center>\r\n'
        '<hr><center>kittenx</center>\r\n'
        '</body>\r\n'
        '</html\r\n>'
    )
    assert response.code == 400
    assert response.location == 'blablacar.com'
    assert response.protocol == 1.1
    assert response.charset == "utf-8"
