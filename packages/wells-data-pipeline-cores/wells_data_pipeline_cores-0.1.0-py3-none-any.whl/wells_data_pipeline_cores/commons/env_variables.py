import logging
from abc import ABC

from typing import Text, List, Literal
from wells_data_pipeline_cores.commons.key_vaults import SecretUtils

class SnowSchemaConf(object):
    def __init__(self, db_name:str = None, schema:str = None, warehouse:str = None, default_role:str = None, developer_role:str=None, loader_role:str = None, analyst_role:str = None, pipeline_role: str = None):
        self.db_name = db_name
        self.schema = schema
        self.warehouse = warehouse
        self.default_role = default_role
        # Developer Roles - Create, Delete, Insert and Select: Table, Dynamic Table, Function, Procedure, Sequence, Stage, Stream, View
        self.developer_role = developer_role
        # Loader - Service account role to DELETE, INSERT, SELECT: Table, Stage, Stream, Function
        self.loader_role = loader_role
        # Analyst - All READ to a schema and all sub-schemas
        self.analyst_role = analyst_role
        # Pipeline - Service account role to CREATE
        self.pipeline_role = pipeline_role

class AzBlobContainerConf(object):
    def __init__(self, conf_name:str = None, storage_account:str = None, container_name:str = None, mount_path:str = None):
        self.conf_name = conf_name
        self.storage_account = storage_account
        self.container_name = container_name
        self.mount_path = mount_path

class AzCosmosDBConf(object):
    def __init__(self, conf_name:str = None, account_uri:str = None, database_name:str = None, containers:dict = None):
        self.conf_name = conf_name
        self.account_uri = account_uri
        self.database_name = database_name
        self.containers = containers

class AzAdxConf(object):
    def __init__(self, conf_name:str = None, cluster:str = None, database_name:str = None, containers:dict = None):
        self.conf_name = conf_name
        self.cluster = cluster
        self.database_name = database_name
        self.containers = containers

class DbxAutoloaderConf(object):
    def __init__(self, conf_name:str = None, load_base_path:str = None, checkpoint_location:str = None):
        self.conf_name = conf_name
        self.load_base_path = load_base_path
        self.checkpoint_location = checkpoint_location

class CorvaApiConf(object):
    def __init__(self, conf_name:str = None, corva_host:str = None, corva_api_key:str = None):
        self.conf_name = conf_name
        self.corva_host = corva_host
        self.corva_api_key = corva_api_key

# mulesoft_emails
class MuleSoftEmailsConf(object):
    def __init__(self, smtp_api_appid:str = None, smtp_api_appid_secret:str = None,  smtp_api_scope:str = None, smtp_api_host:str = None, sender:str = None, to_recipients:str = None, subject:str = None, contents:dict = None):
        self.smtp_api_appid = smtp_api_appid
        self.smtp_api_appid_secret = smtp_api_appid_secret
        self.smtp_api_scope = smtp_api_scope
        self.smtp_api_host = smtp_api_host
        self.sender = sender
        self.subject = subject
        self.contents = contents

"""
EnvVariables class
"""
class EnvVariables(object):
    def __init__(self, dbutils = None, pyspark=None, conf = None, keyvault_name:Text = 'Wells.Databricks.KeyVault.Secrets'):
        # Keep Databricks dbutils & pyspark object instance for reference
        self.dbutils = dbutils
        self.pyspark = pyspark

        # Keep secret _utils and global configuration 
        self.secret_utils = SecretUtils(dbutils=dbutils, keyvault_name=keyvault_name)
        self.conf = conf

        # Keep application configurations
        self.az_app_conf = AzAppConf(secret_utils=self.secret_utils, conf=self.conf)

        self.azure_conf = AzureConf(secret_utils=self.secret_utils, conf=self.conf)

        self.kepler_conf = KeplerConf(secret_utils=self.secret_utils, conf=self.conf)

        self.dbx_conf = DbxConf(secret_utils=self.secret_utils, conf=self.conf)

        self.corva_conf = CorvaConf(secret_utils=self.secret_utils, conf=self.conf)

        self.mulesoft_conf = MuleSoftConf(secret_utils=self.secret_utils, conf=self.conf)

    @staticmethod
    def get_config_value(conf, key:str, default_value=""):
        """ get value in yaml configuraiton (dict object)
        Params:
        ----------
            - conf : it is dict object
            - key : format "a.b.c"
        Return:
        -----------
            - value for key in conf. Empty if can not find
        """
        if conf and key:
            try:
                key_tokens = key.split(".")
                len_key_tokens = len(key_tokens)
                if(len_key_tokens == 1):
                    return conf[key_tokens[0]]
                else:
                    conf_item_value = conf
                    for key_item in key_tokens:
                        conf_item_value = conf_item_value[key_item]
                    return conf_item_value
            except Exception as error:
                return default_value
        return default_value

    @staticmethod
    def get_secret_value(secret_utils:SecretUtils, secret_key:str):
        if secret_utils and secret_key:
            try:
                _value = secret_utils.get_secret(key_name=secret_key)
                if _value:
                    return _value
            except Exception as error:
                return ""
        return ""

    def _get_variable_value(self, conf_var_key:str=None, secret_key:str=None, default_value:str=None):
        """ this method will try to do
            - find secret key and return if having value
            - otherwise find in configuration file in conf/ folder
            - owtherwise return default value
        Params:
        -----------
            - conf_var_key: key name defined in conf/ folder with format "a.b.c"
            - secret_key: key defined in keyvaults
            - default_value: return if there is no value in conf/ or keyvaults
        Return:
        -----------
            - value of variable
        """
        if secret_key:
            _value = self.secret_utils.get_secret(key_name=secret_key)
            if _value:
                return _value
        
        if conf_var_key:
            _value = EnvVariables.get_config_value(conf=self.conf, key=conf_var_key)
            if _value:
                return _value

        return default_value

    ################## Azure Services Variables ############################################
    def get_tenant_name(self):
        return self._get_variable_value(conf_var_key="az_tenant_name")

    def get_version(self):
        return self._get_variable_value(conf_var_key="version")

    def get_environment(self):
        return self._get_variable_value(conf_var_key="environment")

    def check_env(self, env_name:Literal['dev', 'tst', 'prd']='dev') -> bool:
        _env = self.get_environment()
        if _env is not None:
            return env_name == _env
        return False

    def is_env_dev(self):
        return self.check_env(env_name='dev')

    def is_env_staging(self):
        return self.check_env(env_name='tst')

    def is_env_prod(self):
        return self.check_env(env_name='prd')

    def get_az_keyvault_name(self):
        return self._get_variable_value(conf_var_key="az_keyvault_name")

"""
Base App Configuration variables
"""
class _AppConf(ABC):
    def __init__(self, conf = None, secret_utils:SecretUtils = None):
        self.secret_utils = secret_utils
        self.conf = conf

############### Azure Application Configuration Class ################
class AzAppConf(_AppConf):
    def __init__(self, secret_utils:SecretUtils = None, conf = None):
        # Prototype initialization 3.x:
        super().__init__(secret_utils=secret_utils, conf=conf)

    def get_tenant_name(self):
        return EnvVariables.get_config_value(conf=self.conf, key="az_tenant_name")

    def get_client_id(self):
        return EnvVariables.get_config_value(conf=self.conf, key="az_application.app_client_id")

    def get_client_secret(self):
        client_secret_keyname = EnvVariables.get_config_value(conf=self.conf, key="az_application.app_client_secret_keyname")
        return EnvVariables.get_secret_value(secret_utils=self.secret_utils, secret_key=client_secret_keyname)

############### Azure Configuration Class ################
class AzureConf(_AppConf):
    def __init__(self, secret_utils:SecretUtils = None, conf = None):
        # Prototype initialization 3.x:
        super().__init__(secret_utils=secret_utils, conf=conf)

    ### Get blob container configuration
    def _get_az_blob_container(self, conf_name:str, blob_conf:dict) -> AzBlobContainerConf:
        if blob_conf is not None:
            try:
                return AzBlobContainerConf(
                    conf_name=conf_name,
                    storage_account=EnvVariables.get_config_value(conf=blob_conf, key="storage_account"),
                    container_name=EnvVariables.get_config_value(conf=blob_conf, key="container_name"),
                    mount_path=EnvVariables.get_config_value(conf=blob_conf, key="mount_path"),
                )
            except Exception as ex:
                logging.error("_get_az_blob_container() - conf_name: %s, Error: %s", conf_name, ex)
        return None

    def get_az_blob_containers(self) -> [AzBlobContainerConf]:
        _blob_containers = []
        try:
            items_conf =  EnvVariables.get_config_value(conf=self.conf, key="azure.az_blob_containers")
            if items_conf and isinstance(items_conf, dict):
                for key, item_conf in items_conf.items():
                    blob_container = self._get_az_blob_container(conf_name=key, blob_conf=item_conf)
                    if blob_container is not None:
                        _blob_containers.append(blob_container)
        except Exception as ex:
            logging.error("get_az_blob_containers() - Error: %s", ex)
        return _blob_containers

    def get_az_blob_container(self, conf_name:str) -> AzBlobContainerConf:
        try:
            items_conf =  EnvVariables.get_config_value(conf=self.conf, key="azure.az_blob_containers")

            if conf_name is not None and items_conf is not None:
                return self._get_az_blob_container(
                    conf_name=conf_name,
                    blob_conf= items_conf.get(conf_name, None)
                )
        except Exception as ex:
            logging.error("get_az_blob_container() - conf_name: %s, Error: %s", conf_name, ex)
        return None

    ### Get CosmosDB container configuration
    def get_az_cosmosdb(self, conf_name:str="default") -> AzCosmosDBConf:
        try:
            az_cosmos_conf =  EnvVariables.get_config_value(conf=self.conf, key="azure.az_cosmos")

            if conf_name is not None and az_cosmos_conf is not None:
                item_conf = az_cosmos_conf.get(conf_name, None)
                if item_conf is not None:
                    return AzCosmosDBConf(
                        conf_name = conf_name,
                        account_uri = EnvVariables.get_config_value(conf=item_conf, key="account_uri"),
                        database_name = EnvVariables.get_config_value(conf=item_conf, key="database_name"),
                        containers = EnvVariables.get_config_value(conf=item_conf, key="containers"),
                    )
        except Exception as ex:
            logging.error("get_az_cosmosdb() - conf_name: %s, Error: %s", conf_name, ex)
        return None

    ### Get CosmosDB container configuration
    def get_az_adx(self, conf_name:str="default") -> AzAdxConf:
        try:
            az_adx_conf =  EnvVariables.get_config_value(conf=self.conf, key="azure.az_adx")

            if conf_name is not None and az_adx_conf is not None:
                item_conf = az_adx_conf.get(conf_name, None)
                if item_conf is not None:
                    return AzAdxConf(
                        conf_name = conf_name,
                        cluster = EnvVariables.get_config_value(conf=item_conf, key="cluster"),
                        database_name = EnvVariables.get_config_value(conf=item_conf, key="database_name"),
                        containers = EnvVariables.get_config_value(conf=item_conf, key="containers"),
                    )
        except Exception as ex:
            logging.error("get_az_adx() - conf_name: %s, Error: %s", conf_name, ex)
        return None

############### MuleSoft Configuration Class ################
class MuleSoftConf(_AppConf):
    def __init__(self, secret_utils:SecretUtils = None, conf = None):
        # Prototype initialization 3.x:
        super().__init__(secret_utils=secret_utils, conf=conf)

    def get_email_conf(self) -> MuleSoftEmailsConf:
        try:
            item_conf = EnvVariables.get_config_value(conf=self.conf, key="mulesoft_emails")

            smtp_api_appid_keyname = EnvVariables.get_config_value(conf=item_conf, key="smtp_api_appid_keyname")
            smtp_api_appid_secret = EnvVariables.get_secret_value(secret_utils=self.secret_utils, secret_key=smtp_api_appid_keyname)

            return MuleSoftEmailsConf(
                smtp_api_appid = EnvVariables.get_config_value(conf=item_conf, key="smtp_api_appid"),
                smtp_api_appid_secret = smtp_api_appid_secret,
                smtp_api_scope = EnvVariables.get_config_value(conf=item_conf, key="smtp_api_scope"),
                smtp_api_host = EnvVariables.get_config_value(conf=item_conf, key="smtp_api_host"),
                sender = EnvVariables.get_config_value(conf=item_conf, key="sender"),
                subject = EnvVariables.get_config_value(conf=item_conf, key="subject"),
                contents = EnvVariables.get_config_value(conf=item_conf, key="contents", default_value={}),
            )
        except Exception as ex:
            logging.error("get_email_conf() - Error: %s", ex)

        return MuleSoftEmailsConf()

############### Databrick Configuration Class ################
class DbxConf(_AppConf):
    def __init__(self, secret_utils:SecretUtils = None, conf = None):
        # Prototype initialization 3.x:
        super().__init__(secret_utils=secret_utils, conf=conf)

    def get_mount_blob_containers(self) -> [AzBlobContainerConf]:
        _blob_containers = []
        try:
            items_conf =  EnvVariables.get_config_value(conf=self.conf, key="dbx.mount_blob_containers")
            if items_conf and isinstance(items_conf, dict):
                for key, item_conf in items_conf.items():
                    blob_container = AzBlobContainerConf(
                        conf_name=key,
                        storage_account=EnvVariables.get_config_value(conf=item_conf, key="storage_account"),
                        container_name=EnvVariables.get_config_value(conf=item_conf, key="container_name"),
                        mount_path=EnvVariables.get_config_value(conf=item_conf, key="mount_path")
                    )
                    _blob_containers.append(blob_container)
        except Exception as ex:
            logging.error("get_mount_blob_containers() - Error: %s", ex)
        return _blob_containers
    
    def get_autoloader(self, name:str) -> DbxAutoloaderConf:
        try:
            item_conf =  EnvVariables.get_config_value(conf=self.conf, key=f"dbx.autoloaders.{name}")
            if item_conf:
                return DbxAutoloaderConf(
                    conf_name=name,
                    load_base_path= EnvVariables.get_config_value(conf=item_conf, key="load_base_path"),
                    checkpoint_location=EnvVariables.get_config_value(conf=item_conf, key="checkpoint_location"),
                )
                
        except Exception as ex:
            logging.error("get_autoloader() - name: %s - Error: %s", name, ex)

        return None

############### Corva Configuration Class ################
class CorvaConf(_AppConf):
    def __init__(self, secret_utils:SecretUtils = None, conf = None):
        # Prototype initialization 3.x:
        super().__init__(secret_utils=secret_utils, conf=conf)

    def get_corva_api_conf(self, conf_name:str = "default") -> CorvaApiConf:
        if  conf_name:
            try:
                _corva_api_conf = EnvVariables.get_config_value(conf=self.conf, key=f"corva.{conf_name}")
                if _corva_api_conf:
                    _corva_api_keyname = EnvVariables.get_config_value(conf=self._corva_api_conf, key="corva_host")
                    return CorvaApiConf(
                        conf_name=conf_name,
                        corva_host=EnvVariables.get_config_value(conf=_corva_api_conf, key="db_name"),
                        corva_api_key=EnvVariables.get_secret_value(secret_utils=self.secret_utils, secret_key=_corva_api_keyname),
                    )
            except Exception as error:
                return CorvaApiConf()
        #return empty
        return CorvaApiConf()

############### Kepler Configuration Class ################
class KeplerConf(_AppConf):
    def __init__(self, secret_utils:SecretUtils = None, conf = None):
        # Prototype initialization 3.x:
        super().__init__(secret_utils=secret_utils, conf=conf)

    def get_snow_account(self):
        return EnvVariables.get_config_value(conf=self.conf, key="kepler.snow_account")

    def get_snow_sa_user(self):
        return EnvVariables.get_config_value(conf=self.conf, key="kepler.snow_sa_user")

    def get_snow_sa_pw(self):
        snow_sa_pw_keyname = EnvVariables.get_config_value(conf=self.conf, key="kepler.snow_sa_pw_keyname")
        return EnvVariables.get_secret_value(secret_utils=self.secret_utils, secret_key=snow_sa_pw_keyname)

    def get_snow_db_schema(self, schema_name:str = "default") -> SnowSchemaConf:
        if  schema_name:
            try:
                _schema_conf = EnvVariables.get_config_value(conf=self.conf, key=f"kepler.snow_dbs.schemas.{schema_name}")
                if _schema_conf:
                    return SnowSchemaConf(
                        db_name=EnvVariables.get_config_value(conf=_schema_conf, key="db_name"),
                        schema=EnvVariables.get_config_value(conf=_schema_conf, key="schema"),
                        warehouse=EnvVariables.get_config_value(conf=_schema_conf, key="warehouse"),
                        default_role=EnvVariables.get_config_value(conf=_schema_conf, key="default_role"),
                        developer_role=EnvVariables.get_config_value(conf=_schema_conf, key="developer_role"),
                        loader_role=EnvVariables.get_config_value(conf=_schema_conf, key="loader_role"),
                        analyst_role=EnvVariables.get_config_value(conf=_schema_conf, key="analyst_role"),
                        pipeline_role=EnvVariables.get_config_value(conf=_schema_conf, key="pipeline_role")
                    )
            except Exception as error:
                return SnowSchemaConf()

        #return empty
        return SnowSchemaConf()

    def get_snowpark_conn_params(self, schema_name:str = "default"):
        if schema_name:
            snow_schema_conf = self.get_snow_db_schema(schema_name=schema_name)
            return {
                "account": self.get_snow_account(),
                "user": self.get_snow_sa_user(),
                "password": self.get_snow_sa_pw(),
                "role": snow_schema_conf.default_role,
                "warehouse": snow_schema_conf.warehouse,
                "database": snow_schema_conf.db_name,
                "schema": snow_schema_conf.schema,
            }
        return {}


        