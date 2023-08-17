#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/1/13 23:47
@File  : api_client.py
'''

import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, headers=None, params=None, **kwargs):
        url = self.base_url + endpoint
        response = requests.get(url, headers=headers, params=params, **kwargs)
        return response

    def post(self, endpoint, headers=None, data=None, json=None, **kwargs):
        url = self.base_url + endpoint
        response = requests.post(url, headers=headers, data=data, json=json, **kwargs)
        return response

    def put(self, endpoint, headers=None, data=None, json=None, **kwargs):
        url = self.base_url + endpoint
        response = requests.put(url, headers=headers, data=data, json=json, **kwargs)
        return response

    def delete(self, endpoint, headers=None, **kwargs):
        url = self.base_url + endpoint
        response = requests.delete(url, headers=headers, **kwargs)
        return response

