#!/usr/bin/env python

import sys
import logging
import json
import requests
from retry import retry
from cloudutils.vault import Vault
import json
from hvac import aws_utils
from base64 import b64encode

log = logging.getLogger(__name__)
EC2_METADATA_URL_BASE = 'http://169.254.169.254'

class VaultEC2(Vault):

    def __init__(self, vault_server, instance_object,  **kwargs):
        self.vault_server = vault_server
        self.token = None
        self.login(provider='aws', login_payload=self.generate_vault_auth_payload(
            instance_object=instance_object))

    @retry(tries=3)
    def generate_vault_auth_payload(self, instance_object, **kwargs):
        '''
        Generate request payload for Vault login
        '''
        try:

            request = aws_utils.generate_sigv4_auth_request(header_value='X-Vault-AWS-IAM-Server-ID')
            
            credentials = self.load_aws_ec2_role_iam_credentials(role_name=self.get_instance_role(
                instance_object=instance_object))
            
            auth = aws_utils.SigV4Auth(credentials['AccessKeyId'], credentials['SecretAccessKey'], credentials['Token'])
            auth.add_auth(request)

            headers = json.dumps({k: [request.headers[k]] for k in request.headers})

            role_with_environment = ["development","staging","pre-prod"]

            if instance_object.tags['environment'] in role_with_environment:
                role = "{service}-{environment}-{region}".format(
                    service=instance_object.tags['service'],
                    environment=instance_object.tags['environment'],
                    region=instance_object.region,
                )
            else:
                role = "{service}-{region}".format(
                    service=instance_object.tags['service'],
                    region=instance_object.region,
                )

            return {
                "iam_http_request_method": request.method,
                "iam_request_url": b64encode(request.url.encode("utf-8")).decode("utf-8"),
                "iam_request_headers": b64encode(headers.encode("utf-8")).decode("utf-8"),
                "iam_request_body": b64encode(request.body.encode("utf-8")).decode("utf-8"),
                "role": role,
            }
        except Exception as e:
            log.error('Failed to generate auth payload! %s: %s' % (type(e).__name__, e))
            raise

    def load_aws_ec2_role_iam_credentials(self, role_name, metadata_url_base=EC2_METADATA_URL_BASE):
        """
        Requests an ec2 instance's IAM security credentials from the EC2 metadata service.
        :param role_name: Name of the instance's role.
        :param metadata_url_base: IP address for the EC2 metadata service.
        :return: dict, unmarshalled JSON response of the instance's security credentials
        """
        metadata_pkcs7_url = '{base}/latest/meta-data/iam/security-credentials/{role}'.format(
            base=metadata_url_base,
            role=role_name,
        )
        log.debug("load_aws_ec2_role_iam_credentials connecting to %s" % metadata_pkcs7_url)
        response = requests.get(url=metadata_pkcs7_url)
        response.raise_for_status()
        security_credentials = response.json()
        return security_credentials

    def get_instance_role(self, instance_object, **kwargs):
        instance_role = "role_{service}".format(
            service=instance_object.tags['service'],
        )

        return instance_role