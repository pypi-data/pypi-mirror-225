# -*- coding:utf-8 -*-
from txapi import API
import pytest
from txapi.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException


class config(object):
    api_domain = "tencentcloudapi.com"
    sid = "xxx"
    skey = "xxx"
    region = "ap-chongqing"
    is_debug = True
    is_ssl = True


def test_send_with_error_aksk():
    client = API.v3(
        api_domain=config.api_domain,
        region=config.region,
        secret_id=config.sid,
        secret_key=config.skey,
        debug=config.is_debug,
        ssl=config.is_ssl)

    cvm = client.get_client("cvm", "2017-03-12")

    params = {
        "Limit": 20,
        "Offset": 1
    }
    rsp = cvm.request("DescribeInstances", params)
    assert "Error" in rsp["Response"]
    assert rsp["Response"]["Error"]["Code"] == "AuthFailure.SecretIdNotFound"
