import json
import logging as logger
import os
import requests
from requests_oauthlib import OAuth1
from test_wooco.src.config.hosts_config import API_HOST
from test_wooco.src.utilities.credentialUtils import CredentialUtils


class RequestUtils(object):
    def __init__(self):
        self.credentials = CredentialUtils.get_wc_api_credentials()
        env = os.environ.get('ENV', 'test')
        wp_host = os.environ.get('WP_HOST')
        self.base_url = API_HOST[wp_host][env]
        self.auth = OAuth1(client_key=self.credentials['key'], client_secret=self.credentials['secret'])

    def validate_status_code(self, status_code, expected_status_code, url, response_json):
        assert status_code == expected_status_code, f"expected status_code is {expected_status_code}, got {status_code}." \
                                                    f"URL: {url}, response: {response_json}"

    def post(self, endpoint, payload=None, headers=None, expected_status_code=201):
        if not headers: headers = {'Content-Type': 'application/json'}
        url = self.base_url + endpoint
        response = requests.post(url=url, data=json.dumps(payload), headers=headers, auth=self.auth)
        status_code = response.status_code
        response_json = response.json()
        self.validate_status_code(status_code, expected_status_code, url, response_json)
        logger.debug(f"API POST response: {response_json}")
        return response_json

    def get(self, endpoint, payload=None, headers=None, expected_status_code=200):
        if not headers: headers = {'Content-Type': 'application/json'}
        url = self.base_url + endpoint
        response = requests.get(url=url, data=json.dumps(payload), headers=headers, auth=self.auth)
        status_code = response.status_code
        response_json = response.json()
        self.validate_status_code(status_code, expected_status_code, url, response_json)
        logger.debug(f"API GET response: {response_json}")
        return response_json
    
    
    def delete(self, endpoint, headers=None, expected_status_code=204):
        if not headers: headers = {'Content-Type': 'application/json'}
        url = self.base_url + endpoint
        response = requests.delete(url=url, headers=headers, auth=self.auth)
        status_code = response.status_code
        response_json = response.json()
        self.validate_status_code(status_code, expected_status_code, url, response_json)
        logger.debug(f"API GET response: {response_json}")
        return response_json
