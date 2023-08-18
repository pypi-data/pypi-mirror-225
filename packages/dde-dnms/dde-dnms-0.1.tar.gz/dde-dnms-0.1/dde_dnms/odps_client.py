from dde_dnms.validators import validate_request_token, validate_data_address
from .config import api_http_interface
from urllib.parse import urljoin
from typing import Dict

import requests
import json
import time
import pandas


@validate_data_address('data_address', 'sql')
@validate_request_token
def call_result(
        data_address: str = '',
        sql: str = '',
        sqlHints: Dict[str, str] = None
) -> any:
    task_id = __create_sql_task(data_address=data_address, sql=sql, sqlHints=sqlHints)
    status = __query_task_status(data_address=data_address, task_id=task_id)
    while status != 'Terminated':
        time.sleep(2)
        status = __query_task_status(data_address=data_address, task_id=task_id)
    return __download_task_result(data_address=data_address, task_id=task_id)


@validate_data_address('data_address', 'sql')
@validate_request_token
def call_result_dataframe(
        data_address: str = '',
        sql: str = '',
        sqlHints: Dict[str, str] = None
) -> pandas.DataFrame:
    """
    结果以dataframe的格式返回
    """
    result = call_result(data_address=data_address, sql=sql, sqlHints=sqlHints)
    if len(result) == 0:
        return pandas.DataFrame([])
    src = [row.split(';') for row in result[1:]]
    return pandas.DataFrame(src, columns=result[0].split(';'))


@validate_data_address('data_address', 'sql')
@validate_request_token
def async_call(
        data_address: str = '',
        sql: str = '',
        sqlHints: Dict[str, str] = None
) -> str:
    """
    调用odps返回任务id
    """
    return __create_sql_task(data_address=data_address, sql=sql, sqlHints=sqlHints)


@validate_data_address('data_address', 'sql')
@validate_request_token
def call_task_status(data_address: str, task_id: str) -> str:
    """
    根据task_id查询任务状态
    """
    status = __query_task_status(data_address=data_address, task_id=task_id)
    return status


@validate_data_address('data_address', 'sql')
@validate_request_token
def async_call_result(data_address: str, task_id: str) -> any:
    """
    根据task_id获取返回结果
    """
    return __download_task_result(data_address=data_address, task_id=task_id)


@validate_data_address('data_address', 'sql')
@validate_request_token
def async_call(
        data_address: str = '',
        sql: str = '',
        sqlHints: Dict[str, str] = None
) -> str:
    """
    调用odps返回任务id
    """
    return __create_sql_task(data_address=data_address, sql=sql, sqlHints=sqlHints)


def __download_task_result(data_address: str, task_id: str) -> list[str]:
    call_url = urljoin(api_http_interface, 'api/call/')
    reqBody = {"dpAddress": data_address, 'payload': json.dumps({'payload': task_id, 'action': 'TASK_DownloadResult'})}
    resp = requests.post(url=call_url, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    strList = json.loads(result['data'])
    return strList


def __query_task_status(data_address: str, task_id: str) -> str:
    call_url = urljoin(api_http_interface, 'api/call/')
    reqBody = {"dpAddress": data_address, 'payload': json.dumps({'payload': task_id, 'action': 'TASK_QueryStatus'})}
    resp = requests.post(url=call_url, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    return result['data']


def __create_sql_task(data_address: str, sql: str, sqlHints: Dict[str, str]) -> str:
    if sqlHints is not None:
        reqBody = {'dpAddress': data_address,'payload': json.dumps({'payload': sql, 'action':'TASK_Create', 'settings':sqlHints})}
    else:
        reqBody = {'dpAddress': data_address,'payload': json.dumps({'payload': sql, 'action':'TASK_Create'})}

    call_url = urljoin(api_http_interface, 'api/call/')
    resp = requests.post(url=call_url, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    return result['data']
