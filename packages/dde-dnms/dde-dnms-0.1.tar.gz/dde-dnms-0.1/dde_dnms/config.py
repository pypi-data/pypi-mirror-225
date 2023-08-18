import os

api_address = os.getenv('DDE_DNMS_ADDRESS', 'http://manager-system-openapi.dde-data-network-test.c237203db54a6422e81c7874785ad5852.cn-hongkong.alicontainer.com')
api_endpoint = os.getenv('DDE_DNMS_ENDPOINT', 'http://114.55.32.117')
api_http_in = api_endpoint + ':8081/'
api_http_interface = api_endpoint + ':8082/'

api_token = os.getenv('DDE_DNMS_API_TOKEN', '')
