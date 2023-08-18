#!/usr/bin/env python

import sys
import logging
import base64
import json
import requests
import botocore.session
from botocore.awsrequest import create_request_object
from retry import retry
from cloudutils.vault import Vault
import json

log = logging.getLogger(__name__)


class VaultEKS(Vault):

    def __init__(self, vault_server, vault_role,  **kwargs):
        self.vault_server = vault_server
        self.token = None
        self.login(provider='aws', login_payload=self.generate_vault_auth_payload(
            vault_role=vault_role))

    def headers_to_go_style(self, headers, **kwargs):
        retval = {}
        for k, v in headers.items():
            if type(v) == bytes:
                retval[k] = [v.decode()]
            else:
                retval[k] = [v]
        return retval

    @retry(tries=3)
    def generate_vault_auth_payload(self, vault_role, **kwargs):
        '''
        Generate request payload for Vault login
        '''
        try:
            session = botocore.session.get_session()
            client = session.create_client('sts')
            endpoint = client._endpoint
            operation_model = client._service_model.operation_model('GetCallerIdentity')
            request_dict = client._convert_to_request_dict({}, operation_model)
            request_dict['headers']['X-Vault-AWS-IAM-Server-ID'] = self.vault_server
            request = endpoint.create_request(request_dict, operation_model)

            headers = json.dumps(self.headers_to_go_style(dict(request.headers)))

            return {
                'role': vault_role,
                'iam_http_request_method': request.method,
                'iam_request_url':         base64.b64encode(bytes(request.url, 'utf-8')).decode(),
                'iam_request_body':        base64.b64encode(bytes(request.body, 'utf-8')).decode(),
                'iam_request_headers':     base64.b64encode(bytes(headers, 'utf-8')).decode(),
            }
        except Exception as e:
            log.error('Failed to generate auth payload! %s: %s' % (type(e).__name__, e))
            raise
