import os
from woocommerce import API
from test_wooco.src.config.hosts_config import WC_API_HOST
from test_wooco.src.utilities.credentialUtils import CredentialUtils


class WoocoApiUtils:

    def __init__(self):
        self.env = os.environ.get('ENV', 'test')
        self.base_url = WC_API_HOST[self.env]
        credentials = CredentialUtils.get_wc_api_credentials()
        self.wcapi = API(url=self.base_url,
                         consumer_key=credentials['key'],
                         consumer_secret=credentials['secret'],
                         version="wc/v3"
                         )

    def validate_status_code(self, status_code, expected_status_code, response_json):
        assert status_code == expected_status_code, f"expected status code is {expected_status_code}, got {status_code}." \
                                                    f"response: {response_json}"

    def get(self, endpoint, expected_status_code=200):
        response = self.wcapi.get(endpoint)
        status_code = response.status_code
        response_json = response.json()
        self.validate_status_code(status_code, expected_status_code, response_json)
        return response_json

    def post(self, endpoint, data=None, expected_status_code=201):
        response = self.wcapi.post(endpoint=endpoint, data=data)
        status_code = response.status_code
        response_json = response.json()
        self.validate_status_code(status_code, expected_status_code, response_json)
        return response_json

    def put(self, endpoint, data=None, expected_status_code=200):
        response = self.wcapi.put(endpoint=endpoint, data=data)
        status_code = response.status_code
        response_json = response.json()
        self.validate_status_code(status_code, expected_status_code, response_json)
        return response_json