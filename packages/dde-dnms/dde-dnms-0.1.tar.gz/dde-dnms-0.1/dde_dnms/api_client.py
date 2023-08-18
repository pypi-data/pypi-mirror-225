from .validators import validate_request_token, validate_data_address
from .config import api_http_interface
from urllib.parse import urljoin, urlencode

import requests
import json
import os


@validate_data_address('data_address')
@validate_request_token
def call_api(
        data_address: str,
        content_type: str = 'json',
        api_path: str = None,
        payload: dict = None
) -> any:
    """
    根据dataAddress请求获取api

    Args:
        data_address(必填): 请求的中枢资源唯一code->dataAddress
        content_type(可选): 提交的请求方式
        api_path(可选): 请求的用户的api_path
        payload(可选): 提交的参数,字典格式

    Returns:
        资源响应requests.response.text
    """
    assert content_type in ('json', 'path', 'form', 'params')
    call_headers = {'Token': os.getenv('DDE_DNMS_API_TOKEN'), 'Content-Type': 'application/{}'.format(content_type)}

    call_url = urljoin(api_http_interface, 'api/call/') + data_address
    if api_path:
        call_url = call_url + '/' + api_path

    call_data = json.dumps(payload) if payload and isinstance(payload, dict) and content_type == 'json' else payload

    response = requests.post(url=call_url, headers=call_headers, params=urlencode(payload)) \
        if content_type == 'params' \
        else requests.post(url=call_url, headers=call_headers, data=call_data)
    return response.text
