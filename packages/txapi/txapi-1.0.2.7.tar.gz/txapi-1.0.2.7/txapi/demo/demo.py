# -*- coding:utf-8 -*-
from txapi import API

client = API.v3(
    api_domain="yunapi3.xxxxxx",
    region="test_region",
    secret_id="云API密钥id",
    secret_key="云API密钥key",
    debug=False,
    ssl=True)
"""
- api_domain: 云API请求的域名:
    默认为公有云域名, 也支持专有云(租户端+运营端)
    公有云: tencentcloudapi.com
    租户端api2: api2.环境主域名
    租户端api3: api3.环境主域名
    运营端api2: yunapi2.环境主域名
    运营端api3: yunapi3.环境主域名
- region: 地域名称
- secret_id, secret_key: 云API密钥
- ssl (是否开启https, 默认为True)
- debug(是否打印请求响应信息, 默认为False),
"""

cvm = client.get_client("cvm", "2017-03-12")

params = {
    "Limit": 20,
    "Offset": 1
}
print(cvm.request("DescribeInstances", params))