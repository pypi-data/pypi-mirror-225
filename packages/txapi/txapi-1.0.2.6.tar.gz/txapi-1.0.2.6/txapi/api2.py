# -*- coding: utf8 -*-
import json

from txapi.QcloudApi.modules import base
from txapi.QcloudApi.qcloudapi import QcloudApi


class Api2Client(object):

    def __init__(
            self,
            api_domain="tencentcloudapi.com",
            endpoint="",
            version="2017-03-12",
            region="ap-guangzhou",
            secret_id="",
            secret_key="",
            token=None,
            ssl=True,
            debug=False):
        self.endpoint = endpoint
        self.version = version
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.token = token
        self.region = region
        self.client = None
        self.ssl = ssl
        self.api_domain = api_domain
        self.debug = debug
        self.version = None

    def _factory(self, module, config):
        config.setdefault("endpoint", "{}.{}".format(module, self.api_domain))
        service = base.Base(config)
        return service

    def init_client(self, module="cvm"):
        # 云API的公共参数
        config = {
            'Region': self.region,
            'secretId': self.secret_id,
            'secretKey': self.secret_key,
            'method': 'GET',
            'SignatureMethod': 'HmacSHA1',
            # 只有cvm需要填写version，其他产品不需要
            'Version': '2017-03-12',
            'ssl': self.ssl
        }
        self.client = QcloudApi(module, config)
        self.client.config["endpoint"] = self.endpoint
        self.client._factory = self._factory
        # self.service = base.Base(self.config)

    def set_domain(self, domain):
        self.api_domain = domain

    def set_version(self, module, version):
        """ api2 没有version的概念，该函数仅用于保持与api3用法一致
        """
        self.version = version

    def set_region(self, region):
        self.region = region

    def set_secret(self, secret_id=None, secret_key=None, token=None):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.token = token

    def set_ssl(self, ssl):
        self.ssl = ssl

    def switch_module(self, module):
        self.module = module
        self.endpoint = "{}.{}".format(module, self.api_domain)

    def get_client(self, module=None, version=None):
        if version is not None:
            self.set_version(module, version)

        obj = Api2Client(
            api_domain=self.api_domain,
            endpoint=self.endpoint,
            version=self.version,
            region=self.region,
            secret_id=self.secret_id,
            secret_key=self.secret_key,
            token=self.token,
            ssl=self.ssl,
            debug=self.debug)
        if module is None:
            module = self.module
        obj.switch_module(module)
        return obj

    def request(self, action, params):
        self.init_client()
        try:
            if self.debug:
                print("[ENDPOINT] {}".format(self.endpoint))
                print("[REQUEST] {}".format(
                    self.client.generateUrl(action, params)))
                print("[SECRET_ID]  {}".format(self.secret_id))
                print("[SECRET_KEY]  {}".format(self.secret_key))
                print("[TOKEN]  {}".format(self.token))
            body = self.client.call(action, params)
            if isinstance(body, bytes) and not isinstance(body, str):
                body = str(body, encoding="utf-8")
            else:
                body = body.encode("utf-8")
            if self.debug:
                print("[RESPONSE] {}".format(body))
            response = json.loads(body)
            return response
        except Exception:
            import traceback
            print('traceback.format_exc():\n%s' % traceback.format_exc())


if __name__ == "__main__":
    api_domain = "api2.yf-m17.tcecqpoc.fsphere.cn"
    sid = ""
    skey = ""
    client = Api2Client()
    client.set_ssl(False)
    client.set_domain(api_domain)
    client.set_region("shanghai")
    client.set_secret(sid, skey)
    client.switch_module("cam")
    client.request("GetAllSubUser", {})
