import logging
import re
import time
from typing import Callable
import uuid
from urllib.parse import urlparse

import requests


GLOBAL_ENDPOINT = ''
GLOBAL_TOKEN = ''


def set_global_endpoint(endpoint: str):
    global GLOBAL_ENDPOINT
    GLOBAL_ENDPOINT = endpoint


def set_global_token(token: str):
    global GLOBAL_TOKEN
    GLOBAL_TOKEN = token


class Wrap:
    def __init__(self, func: Callable, endpoint='', token='') -> None:
        self._func = func
        self._endpoint = endpoint if endpoint else GLOBAL_ENDPOINT
        self._token = (token if token else GLOBAL_TOKEN).strip()
        self._req_id = None
        self._result = None

        try:
            urlparse(self._endpoint)
        except Exception:
            raise ValueError(
                f'Invalid endpoint "{self._endpoint}". '
                'Please set to server URL prior to "rr" use.'
            )

    def __call__(self, *args, **kwargs):
        self._start_call(self._func, args, kwargs)

        try:
            self._result = self._func(*args, **kwargs)
            return self._result
        except Exception as e:
            raise e

    def __enter__(self):
        self._req_id = str(uuid.uuid4())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self._end_call_with_exception(f'{exc_type.__name__}: {exc_val}')
        else:
            self._end_call(self._result)

        self._req_id = None

    def _start_call(self, func: Callable, args: tuple, kwargs: dict):
        data = {
            'request_id': self._req_id,
            'state': 'start',
            'func': func.__name__,
            'args': str(args), 'kwargs': str(kwargs),
            'mac': self._get_unique_user_id(),
            'timestamp': time.time(),
        }

        self._send(data)

    def _get_unique_user_id(self):
        # This yields a MAC address. Might be too personal for most anonymity
        # conscience.
        # TODO: Consider replacing with hash of MAC.
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    def _end_call(self, result):
        data = {
            'request_id': self._req_id,
            'state': 'success',
            'result': str(result),
            'timestamp': time.time(),
        }

        self._send(data)

    def _end_call_with_exception(self, e):
        data = {
            'request_id': self._req_id,
            'state': 'error',
            'error': str(e),
            'timestamp': time.time(),
        }

        self._send(data)

    def _send(self, data):
        headers = {
            'Content-Type': 'application/json'
        }

        resp = requests.post(
            self._endpoint,
            json={**data, **{'token': self._token}},
            headers=headers,
        )

        if 200 <= resp.status_code < 300:
            return

        if 400 <= resp.status_code < 500:
            content = resp.content.decode()
            logging.warning(f'Unable to post {data["state"]} to endpoint: {content}')
            return

        if 500 <= resp.status_code:
            logging.warning('Result Reporter experienced an internal server error.')
            return
