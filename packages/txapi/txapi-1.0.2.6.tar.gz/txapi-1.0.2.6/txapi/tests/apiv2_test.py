from txapi import API
from txapi.QcloudApi.qcloudapi import QcloudApi

test_api = API.v2


class TestApi(object):

    def test_create_apiv2(self):
        api = test_api(
            api_domain="domain1",
            endpoint="endpoint1",
            version="222",
            region="ap-guangzhou",
            secret_id="xxx",
            secret_key="xxx",
            token=None,
            ssl=True,
            debug=False)
        assert api.api_domain == "domain1"
        assert api.ssl

    def test_init_client(self):
        api = test_api()
        assert api.client is None
        api.init_client()
        assert isinstance(api.client, QcloudApi)

    def test_set_domain(self):
        api = test_api()
        assert api.api_domain == "tencentcloudapi.com"
        api.set_domain("test.domain")
        assert api.api_domain == "test.domain"
