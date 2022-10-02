class HTTPSClientError(Exception):
    pass


class ConnectError(HTTPSClientError):
    message = "Не смог подсоединиться к серверу. Проверьте URL-ссылку"


class MaxDirectionsError(HTTPSClientError):
    message = "Закончились попытки на переадресацию"


class IncorrectMethodTypeError(HTTPSClientError):
    message = "Введённый тип запроса не существует. Посмотрите help"
