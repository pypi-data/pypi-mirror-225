# Import standard libraries
# import os
# import sys
import logging
from typing import Text
# import requests

from msal import ConfidentialClientApplication

from wells_data_pipeline_cores.commons import EnvVariables
# from azure.identity import DefaultAzureCredential


class AzAuthzService(object):
    def __init__(self, env_vars:EnvVariables):
        self.env_vars = env_vars

    def get_sp_access_token(self,client_id:str, client_credential:str, tenant_name:str, scopes:list) -> Text:
        logging.info('Attempting to obtain an access token...')
        result = None
        app = ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_credential,
            authority=f"https://login.microsoftonline.com/{tenant_name}"
        )
        result = app.acquire_token_for_client(scopes=scopes)

        if "access_token" in result:
            logging.info('Access token successfully acquired')
            return result['access_token']
        else:
            logging.error('Unable to obtain access token')
            logging.error(f"Error was: {result['error']}")
            logging.error(f"Error description was: {result['error_description']}")
            logging.error(f"Error correlation_id was: {result['correlation_id']}")
            raise Exception('Failed to obtain access token')