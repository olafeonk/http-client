from client.request import Request
from client.do_request import do_request


def test_do_request():
    request = Request()
    request.set_host('vk.com')

    response = do_request(request, 1000, 10)

    assert response.code == 200
    assert response.protocol == 1.1