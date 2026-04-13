"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import json
import requests
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('fortinet-fortiguard-socaas')


class SOCaaS:
    def __init__(self, config):
        self.username = config.get("username")
        self.password = config.get("password")
        self.client_id = config.get("client_id")
        self.verify_ssl = config.get('verify_ssl')
        self.host = config.get("server")
        if not self.host.startswith('https://'):
            self.host = f"https://{self.host}"
        self._auth_token = None

    def _generate_token(self):
        return self._acquire_token()

    def _acquire_token(self):
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            data = {
                "username": self.username,
                "password": self.password,
                "client_id": self.client_id,
                "grant_type": "password"
            }
            logger.debug(f"Payload: {data}")
            endpoint = 'https://customerapiauth.fortinet.com/api/v1/oauth/token/'
            logger.debug(f"Endpoint: {endpoint}")
            response = requests.post(endpoint, data=json.dumps(data), headers=headers, verify=self.verify_ssl,
                                     timeout=60)
            logger.debug(f"Response: {response}")

            if response.status_code in [200, 204, 201]:
                token_data = response.json()
                return {"accessToken": token_data.get("access_token")}
            else:
                error_msg = f'Response {response.status_code}: {response.reason}'
                if response.text:
                    error_msg += f'\nError Message: {response.text}'
                raise ConnectorError(error_msg)

        except Exception as err:
            logger.error(f"Error acquiring token: {str(err)}")
            raise ConnectorError(f"Error acquiring token: {str(err)}")

    def _get_auth_token(self):
        if not self._auth_token:            
            token_resp = self._generate_token()
            self._auth_token = f"Bearer {token_resp['accessToken']}"            
        return self._auth_token

    def make_rest_call(self, endpoint, method, data=None, params=None):
        try:
            url = self.host + endpoint
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': self._get_auth_token()
            }

            response = requests.request(method, url, headers=headers, verify=self.verify_ssl, data=data, params=params)
            if response.status_code in [200, 201, 204]:
                if response.text != "":
                    if (response.json()).get('result').get('status') == 0:
                        return (response.json()).get('result').get('data')
                    else:
                        return response.json()
                else:
                    return {}
            elif response.status_code == 404:
                return response.json()
            else:
                raise ConnectorError(f"{response.status_code}: {response.text}")
        except Exception as err:
            raise ConnectorError(str(err))


def check(config):
    try:
        co = SOCaaS(config)
        # You might want to add a simple API call here to verify the token works
        # For example:
        # result = co.make_rest_call("/some-endpoint", "GET")
        # return True if result is as expected
        service = co.make_rest_call("/resource-api/v2/security/services/HTTP", "GET")
        # check that service.result.data is list
        if service and isinstance(service.get('result').get('data', []), list):
            return True

        return False
    except Exception as err:
        raise ConnectorError(str(err))
