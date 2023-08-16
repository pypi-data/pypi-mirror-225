import logging
from pathlib import Path
from decouple import config
from typing import Any, Text


class SecretUtils(object):
    def __init__(self, dbutils = None, keyvault_name: Text = ""):
        self.keyvault_name = keyvault_name
        self.dbutils = dbutils

    def get_secret(self, key_name: Text):
        try:
            if self.dbutils:
                logging.info(f"SecretUtils::get_secret - dbutils.secrets - scope:{self.keyvault_name} - key: {key_name}")
                return self.dbutils.secrets.get(scope=self.keyvault_name, key=key_name)
            else:
                return LocalSecretUtils.get_secret(key_name=key_name)
        except Exception as error:
            logging.error('SecretUtils - get_secret() Execution error: %s', error)
            return ""

class LocalSecretUtils(object):
    @staticmethod
    def get_secret(key_name: Text):
        contents = ""

        # If there is no key_value in .keyvaults folder, Try to load key_value from system environment
        try:
            # How does it work? - https://pypi.org/project/python-decouple/#toc-entry-12
            contents = config(key_name, default='')
        except Exception as error:
            logging.error('LocalSecretUtils - get_secret() Execution error: %s', error)
            contents = ""
                
        return contents