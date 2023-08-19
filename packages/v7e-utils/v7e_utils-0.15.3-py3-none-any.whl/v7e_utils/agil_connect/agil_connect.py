from __future__ import annotations

import os
from typing import Dict
from urllib.parse import urljoin
from v7e_utils.agil_connect import token
import requests


class AgilConnection:
    __slots__ = ('gateway_url', 'api_endpoint', 'session')

    def __init__(self, url=None):
        self.gateway_url = os.environ.get('API_GATEWAY_URL', None)
        self.api_endpoint = None
        self.session = requests.Session()
        authorization = token.get_token()
        if authorization:
            self.session.headers.update({'Authorization': authorization})
        if url:
            self.gateway_url = url

    def set_api_endpoint(self, endpoint):
        self.api_endpoint = endpoint

    @staticmethod
    def ensure_forward_slash(path):
        if path.endswith('/'):
            return path
        return f"{path}/"

    def ensure_url(self, baseurl, path):
        if path.startswith('http') or path.startswith('https'):
            return path
        baseurl = self.ensure_forward_slash(baseurl)
        return self.ensure_forward_slash(urljoin(baseurl, path))

    def get_result(self, url, params=None, headers:Dict | None = None):
        response = self.session.get(url, params=params, headers=headers)
        return response.json()

    def post_data(self, url, data, headers:Dict | None = None):
        response = self.session.post(url, data=data, headers=headers)
        return response.json()

    def put_data(self, url, data, headers:Dict | None = None):
        response = self.session.put(url, json=data, headers=headers)
        return response.json()
