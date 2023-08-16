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

from azure.cosmos import CosmosClient, ContainerProxy
from azure.cosmos.exceptions import CosmosHttpResponseError

from azure.identity import ClientSecretCredential, DefaultAzureCredential

from wells_data_pipeline_cores.commons import EnvVariables, Utils, AzCosmosDBConf

from abc import ABC, abstractmethod

# logger = logging.getLogger(__name__)

class AzCosmosPartitionKeyModel():
    def __init__(self) -> None:
        self.PartitionKey = ""
        self.TsSynced = 0

# Abstract class
#
# API documentation: https://learn.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos?preserve-view=true&view=azure-python
# Sample Code: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos/samples
# 
class AzCosmosDataService(ABC):
    """
    CosmosDataService is base service, it provides all common attributes and methods
    Class provides access to the following useful objects:
    * self.spark is a SparkSession
    * self.dbutils provides access to the DBUtils
    """
    
    def __init__(self, env_vars:EnvVariables, conf_name:str="default"):
        self.env_vars = env_vars
        self.dbutils = env_vars.secret_utils.dbutils
        self.cosmos_conf:AzCosmosDBConf = env_vars.azure_conf.get_az_cosmosdb(conf_name=conf_name)

    def get_cosmos_client(self) -> CosmosClient:
        try:
            app_conf = self.env_vars.az_app_conf
            # logging.info("get_cosmos_client - tenant_id: %s, client_id: %s", app_conf.get_tenant_name(), app_conf.get_client_id())
            # logging.info("get_cosmos_client - account_uri: %s", self.cosmos_conf.account_uri)

            # With this done, you can use your AAD service principal id and secret to create your ClientSecretCredential.
            aad_credentials = ClientSecretCredential(
                tenant_id=app_conf.get_tenant_name(),
                client_id=app_conf.get_client_id(),
                client_secret=app_conf.get_client_secret(),
            )

            # You can also utilize DefaultAzureCredential rather than directly passing in the id's and secrets.
            # This is the recommended method of authentication, and uses environment variables rather than in-code strings.
            # aad_credentials = DefaultAzureCredential()
            return CosmosClient(
                url=self.cosmos_conf.account_uri, 
                credential=aad_credentials,
                consistency_level='Session',
                logging_enable=True,
            )
        except Exception as ex:
            logging.error("get_cosmos_client() - conf_name: %s, Error: %s", self.cosmos_conf.conf_name, ex)
        return None

    def get_database_name(self) -> str:
        if self.cosmos_conf is not None:
            return self.cosmos_conf.database_name
        return ""

    def get_item(container:ContainerProxy, id:Text, partition_key:Text):
        if container is None or id is None or partition_key is None:
            return None
        
        return container.read_item(id=id, partition_key=partition_key)

    #######################################################################
    ######
    ###### Utility Methods
    ######
    #######################################################################
    def generate_id(self):
        # return uuid.uuid4().hex
        return uuid.uuid1().hex
    
    #######################################################################
    ######
    ###### Abstract Methods
    ######
    #######################################################################

    @abstractmethod
    def get_container_name(self):
        pass

    #######################################################################
    ######
    ###### Base Methods
    ######
    #######################################################################

    def list_partition_keys(self) -> dict[Text, AzCosmosPartitionKeyModel]:
        """
        SELECT DISTINCT c.partitionKey FROM c
        """
        try:
            client = self.get_cosmos_client()

            DATABASE_NAME = self.get_database_name()
            _database = client.get_database_client(DATABASE_NAME)

            CONTAINER_NAME = self.get_container_name()
            _container = _database.get_container_client(CONTAINER_NAME)
            
            #QUERY = f'SELECT DISTINCT c.partitionKey, Max(c.tsSynced) AS tsSynced FROM {CONTAINER_NAME} c GROUP BY c.partitionKey'
            QUERY = f'SELECT DISTINCT c.partitionKey FROM {CONTAINER_NAME} c'
            results = _container.query_items(
                query=QUERY, 
                enable_cross_partition_query=True
            )

            partition_keys = dict()
            
            for item in results:
                model = AzCosmosPartitionKeyModel()
                model.PartitionKey = Utils.get_dict_val(data=item, key='partitionKey', default='')
                model.TsSynced = Utils.get_dict_val(data=item, key='tsSynced', default=None)
                partition_keys.update({model.PartitionKey: model})
                
            return partition_keys
                
        except Exception as ex:
            logging.error("ERROR - list_partition_keys: %s", ex)

        return {}
    
    def get_item(self, id=Text, partition_key:Text=None) -> dict:
        try:
            client = self.get_cosmos_client()

            DATABASE_NAME = self.get_database_name()
            _database = client.get_database_client(DATABASE_NAME)

            CONTAINER_NAME = self.get_container_name()
            _container = _database.get_container_client(CONTAINER_NAME)
            
            if partition_key is not None:
                return self.cosmos_dao.get_item(container=_container, id=id, partition_key=partition_key)
            else:
                QUERY = f'SELECT * FROM {CONTAINER_NAME} c WHERE c.id=@Id'
                params = [dict(name="@Id", value=id)]
                results = _container.query_items(
                    query=QUERY, parameters=params, enable_cross_partition_query=True
                )
                return next(results, {})
        except Exception as ex:
            logging.error("ERROR - get_item: %s", ex)

        return {}

    def list_items_by_ts_synced(self, ts_synced=None, partition_key:Text=None, page_token=None, page_size=500) -> tuple((list[dict], Any)):
        """
        SELECT * FROM c
        WHERE c.tsSynced >= 584045800
        ORDER BY c.timeSynced ASC
        """
        try:
            client = self.get_cosmos_client()

            DATABASE_NAME = self.get_database_name()
            # logging.info("list_items_by_ts_synced - DATABASE_NAME: %s", DATABASE_NAME)
            _database = client.get_database_client(DATABASE_NAME)

            CONTAINER_NAME = self.get_container_name()
            # logging.info("list_items_by_ts_synced - CONTAINER_NAME: %s", CONTAINER_NAME)
            _container = _database.get_container_client(CONTAINER_NAME)
            
            
            if ts_synced is None:
                QUERY = f'SELECT * FROM {CONTAINER_NAME} c ORDER BY c.tsSynced ASC'
                PARAMS = None
            else:
                QUERY = f'SELECT * FROM {CONTAINER_NAME} c WHERE c.tsSynced > @tsSynced ORDER BY c.tsSynced ASC'
                PARAMS = [dict(name="@tsSynced", value=ts_synced)]

            if page_size < 1:
                page_size = 1

            enable_cross_partition_query = True
            if page_token is not None or partition_key is not None:
                enable_cross_partition_query = None

            query_iterable = _container.query_items(
                query=QUERY,
                partition_key=partition_key,
                parameters=PARAMS,
                enable_cross_partition_query=enable_cross_partition_query,
                max_item_count=page_size
            )

            if page_token is None:
                pager = query_iterable.by_page()
                list_items = list(pager.next())
                next_token = pager.continuation_token
                return (list_items, next_token)
            else:
                pager = query_iterable.by_page(page_token)
                list_items = list(pager.next())
                next_token = pager.continuation_token
                return (list_items, next_token)
        except CosmosHttpResponseError as err:
            logging.error("ERROR - list_items_by_ts_synced - %s", err)
        except Exception as ex:
            logging.error("ERROR - list_items_by_ts_synced - %s", ex)
            
        return ([], None)
