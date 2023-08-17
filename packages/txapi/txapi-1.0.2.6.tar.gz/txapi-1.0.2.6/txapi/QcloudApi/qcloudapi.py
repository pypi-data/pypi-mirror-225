#! /usr/bin/env python
# -*- coding: utf-8 -*-

from txapi.QcloudApi.modules import base


class QcloudApi(object):
    def __init__(self, module, config):
        self.module = module
        self.config = config

    def _factory(self, module, config):
        config.setdefault("endpoint", module + '.api.qcloud.com')
        service = base.Base(config)

        return service

    def setSecretId(self, secretId):
        self.config['secretId'] = secretId

    def setSecretKey(self, secretKey):
        self.config['secretKey'] = secretKey

    def setRequestMethod(self, method):
        self.config['method'] = method

    def setRegion(self, region):
        self.config['Region'] = region

    def setSignatureMethod(self, SignatureMethod):
        self.config['SignatureMethod'] = SignatureMethod

    def generateUrl(self, action, params):
        service = self._factory(self.module, self.config)
        return service.generateUrl(action, params)

    def call(self, action, params, req_timeout=None, debug=False):
        """
        @type action: string
        @param action: action interface

        @type params: dict
        @param params: interface parameters

        @type req_timeout: int
        @param req_timeout: request timeout(seconds)

        @type debug: bool
        @param debug: debug switch
        """
        service = self._factory(self.module, self.config)
        if req_timeout is not None:
            service.set_req_timeout(req_timeout)
        if debug:
            service.open_debug()

        methods = dir(service)
        for method in methods:
            if (method == action):
                func = getattr(service, action)
                return func(params)

        return service.call(action, params)
