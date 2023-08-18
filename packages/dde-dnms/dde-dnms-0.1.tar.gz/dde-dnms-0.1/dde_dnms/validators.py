from .config import api_address, api_http_in
from .exceptions import TokenNotExistException, TokenInvalidException, CreateTokenException, DataAddressException

from urllib.parse import urljoin
import requests
import json
import os


def create_ak_sk(account: str) -> dict:
    """
    根据账户获取数据网络管理系统的ak/sk
    """
    url = urljoin(api_address, '/openapi/account/credential/create')
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps({'account': account}))
    if response.json().get('data') is None:
        raise CreateTokenException('请求中枢获取ak/sk失败,请检查account或api_address是否正确')
    return response.json().get('data')


def create_token(ak: str, sk: str) -> str:
    """
    根据ak/sk获取中枢token
    """
    url = urljoin(api_http_in, '/api/central/token')
    params = {'accessKey': ak, 'secretKey': sk}
    response = requests.get(url, params=params)
    if response.json().get('data') is None:
        raise CreateTokenException('请求中枢获取token失败,请检查ak/sk是否正确')

    token = response.json().get('data').get('token')
    os.environ['DDE_DNMS_API_TOKEN'] = token
    return token


def validate_request_token(func):
    """token校验装饰器
    """
    def wrapper(*args, **kwargs):
        if os.getenv('DDE_DNMS_API_TOKEN') is None or os.getenv('DDE_DNMS_API_TOKEN') == '':
            raise TokenNotExistException('Token Not Exists')
        return func(*args, **kwargs)
    return wrapper


def validate_data_address(*required):
    """参数校验装饰器
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for param in required:
                if param not in kwargs or kwargs[param] == '' or kwargs[param] is None:
                    raise DataAddressException('DataAddress填写错误')
            return func(*args, **kwargs)
        return wrapper
    return decorator
