import os

import urllib.parse

from datetime import datetime
from typing import (
    Text,
    Any,
    Sequence,
)

import logging
import uuid
import pandas as pd

import json

from azure.kusto.data import KustoClient, KustoConnectionStringBuilder

from wells_data_pipeline_cores.commons import EnvVariables, Utils, AzAdxConf

from abc import ABC, abstractmethod

# logger = logging.getLogger(__name__)

class AzCosmosPartitionKeyModel():
    def __init__(self) -> None:
        self.PartitionKey = ""
        self.TsSynced = 0

# Abstract class
#
# API documentation: https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/
# KQL quick reference: https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/kql-quick-reference
# Query best practices: https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/best-practices
# SQL to Kusto Query Language cheat sheet: https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/sqlcheatsheet
# 
class AzAdxDataService(ABC):
    
    def __init__(self, env_vars:EnvVariables, conf_name:str="default"):
        self.env_vars = env_vars
        self.dbutils = env_vars.secret_utils.dbutils
        self.adx_conf:AzAdxConf = env_vars.azure_conf.get_az_adx(conf_name=conf_name)

    def get_kusto_client(self) -> KustoClient:
        try:
            app_conf = self.env_vars.az_app_conf
            kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                connection_string=self.adx_conf.cluster,
                aad_app_id=app_conf.get_client_id(),
                app_key=app_conf.get_client_secret(), 
                authority_id=app_conf.get_tenant_name()
            )
            return KustoClient(kcsb)
        except Exception as ex:
            logging.error("get_kusto_client() - conf_name: %s, Error: %s", self.adx_conf.conf_name, ex)
        return None

    def get_database_name(self) -> str:
        if self.adx_conf is not None:
            return self.adx_conf.database_name
        return ""

