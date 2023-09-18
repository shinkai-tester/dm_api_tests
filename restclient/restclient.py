import uuid
import requests.exceptions
import structlog
import curlify
from requests import session, Response


class Restclient:
    def __init__(self, host, headers=None, log_enabled=True):
        self.host = host
        self.session = session()
        if headers:
            self.session.headers.update(headers)
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='api')
        self.log_enabled = log_enabled

    def post(self, path: str, **kwargs) -> Response:
        return self._send_request('POST', path, **kwargs)

    def get(self, path: str, **kwargs) -> Response:
        return self._send_request('GET', path, **kwargs)

    def put(self, path: str, **kwargs) -> Response:
        return self._send_request('PUT', path, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        return self._send_request('DELETE', path, **kwargs)

    def _send_request(self, method, path, **kwargs):
        full_url = self.host + path
        log = self.log.bind(event_id=str(uuid.uuid4()))
        if self.log_enabled:
            log.msg(
                event='request',
                method=method,
                full_url=full_url,
                params=kwargs.get('params'),
                headers=kwargs.get('headers'),
                json=kwargs.get('json'),
                data=kwargs.get('data')
            )
        response = self.session.request(
            method=method,
            url=full_url,
            **kwargs
        )

        if self.log_enabled:
            curl = curlify.to_curl(response.request)
            print(curl)

            log.msg(
                event='response',
                status_code=response.status_code,
                headers=response.headers,
                json=self._get_json(response),
                text=response.text,
                content=response.content,
                curl=curl
            )

        return response

    @staticmethod
    def _get_json(response):
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return


def step(
        before_message: str = '',
        after_message: str = '',
        log_it=True
):
    def wrapper(function):
        def _wrap(*args, **kwargs):
            dynamic_before_message = before_message.format(**kwargs)
            dynamic_after_message = after_message.format(**kwargs)
            if log_it:
                print(f"\n{dynamic_before_message}")
            result = function(*args, **kwargs)
            if log_it:
                print(f"\n{dynamic_after_message}")
            return result

        return _wrap

    return wrapper
