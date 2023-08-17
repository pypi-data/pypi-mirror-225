# -*- coding: utf-8 -*-
import json
import ssl

from txapi.tencentcloud.common import credential
from txapi.tencentcloud.common.abstract_client import AbstractClient
from txapi.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from txapi.tencentcloud.common.profile.client_profile import ClientProfile
from txapi.tencentcloud.common.profile.http_profile import HttpProfile
from txapi.version import VERSION_MAP

ssl._create_default_https_context = ssl._create_unverified_context


class Api3Client(AbstractClient):

    def __init__(
            self,
            api_domain="tencentcloudapi.com",
            endpoint="",
            version=None,
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
        self.version_map = VERSION_MAP
        self.api_domain = api_domain
        self.debug = debug
        self.sign_method = None

    def set_sign_method(self, sign_method):
        """ 设置加密算法，包括：("HmacSHA1", "HmacSHA256", "TC3-HMAC-SHA256")
        """
        self.sign_method = sign_method

    def init_client(self):
        httpProfile = HttpProfile()
        clientProfile = ClientProfile(signMethod=self.sign_method)
        clientProfile.httpProfile = httpProfile
        httpProfile.endpoint = self.endpoint
        cred = credential.Credential(
            self.secret_id, self.secret_key, self.token)
        self.client = AbstractClient(
            cred, self.region, clientProfile, self.ssl)
        self.client._apiVersion = self.version

    def set_region(self, region):
        self.region = region

    def set_ssl(self, ssl):
        self.ssl = ssl

    def set_secret(self, secret_id=None, secret_key=None, token=None):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.token = token

    def switch_module(self, module):
        self.module = module
        self.endpoint = "%s.%s" % (module, self.api_domain)
        if module not in self.version_map.keys():
            raise RuntimeError(
                "version of module `{}` not found".format(module))
        self.version = self.version_map[module]

    def get_client(self, module=None, version=None):
        if version is None:
            version = self.version
        else:
            self.set_version(module, version)

        obj = Api3Client(
            api_domain=self.api_domain,
            endpoint=self.endpoint,
            version=self.version,
            region=self.region,
            secret_id=self.secret_id,
            secret_key=self.secret_key,
            token=self.token,
            ssl=self.ssl,
            debug=self.debug)
        obj.version_map = self.version_map
        if module is None:
            module = self.module
        # print(module)
        obj.switch_module(module)
        return obj

    def set_version(self, module, version):
        self.version_map[module] = version

    def set_domain(self, domain):
        self.api_domain = domain

    def request(self, action, params):
        self.init_client()
        try:
            if self.debug:
                print("[ENDPOINT] {}".format(self.endpoint))
                print("[VERSION] {}".format(self.version))
                print("[ACTION] {}".format(action))
                print("[PARAMS] {}".format(json.dumps(params)))
                print("[SECRET_ID] {}".format(self.secret_id))
                print("[SECRET_KEY] {}".format(self.secret_key))
                print("[TOKEN] {}".format(self.token))
            body = self.client.call(action, params)
            if self.debug:
                print("[RESPONSE] {}".format(body.encode("utf-8")))
            response = json.loads(body)
            return response
            # if "Error" not in response["Response"]:
            #     return response
            # else:
            #     code = response["Response"]["Error"]["Code"]
            #     message = response["Response"]["Error"]["Message"]
            #     reqid = response["Response"]["RequestId"]
            #     raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            print(str(e))
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


if __name__ == "__main__":
    api_domain = "api3.main_domain"
    sid = ""
    skey = ""
    client = Api3Client()
    client.set_domain(api_domain)
    client.set_ssl(False)
    client.set_region("shanghai")
    client.set_secret(sid, skey)
    client.switch_module("cvm")
    client.request("DescribeInstances", {"Limit": 1})
