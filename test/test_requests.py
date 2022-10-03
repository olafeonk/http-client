from client.request import Request


def test_request():
    request = Request()
    expected_bytes_request: str = (
        'GET / HTTP/1.1\r\n'
        'Host: None\r\n'
        'Connection: close\r\n'
        'Content-Length: 0\r\n\r\n'
    )

    assert bytes(request).decode() == expected_bytes_request


def test_set_method_with_url():
    request = Request()
    request.set_url('https://vk.com/feed')
    request.set_body('Hello')
    request.set_headers({'Cookie': '1234',
                         'Reference': 'blablacar.com'})
    request.set_header(header='User-Agent', value='Yandex')
    request.set_method('post')
    request.set_current_path()

    expected_bytes_request: str = (
        'POST /feed HTTP/1.1\r\n'
        'Host: vk.com\r\n'
        'Connection: close\r\n'
        'Content-Length: 5\r\n'
        'Cookie: 1234\r\n'
        'Reference: blablacar.com\r\n'
        'User-Agent: Yandex\r\n\r\n'
        'Hello'
    )

    assert bytes(request).decode() == expected_bytes_request


def test_methods_with_host():
    request = Request()
    request.set_host('vk.com')
    request.set_path(['/feed/ru'])
    request.set_body('Hello')
    request.set_headers({'Cookie': '1234',
                         'Reference': 'blablacar.com'})
    request.set_header(header='User-Agent', value='Yandex')
    request.set_method('delete')
    request.set_current_path()

    expected_bytes_request: str = (
        'DELETE /feed/ru HTTP/1.1\r\n'
        'Host: vk.com\r\n'
        'Connection: close\r\n'
        'Content-Length: 5\r\n'
        'Cookie: 1234\r\n'
        'Reference: blablacar.com\r\n'
        'User-Agent: Yandex\r\n\r\n'
        'Hello'
    )

    assert bytes(request).decode() == expected_bytes_request
    assert request.host == 'vk.com'
