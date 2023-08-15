import logging

from typing import Text

from wells_data_pipeline_cores.commons import EnvVariables

logger = logging.getLogger(__name__)

class AzStorageAccountService(object):
    """ Mount ADLS Gen2 or Blob Storage with ABFS
        https://learn.microsoft.com/en-us/azure/databricks/dbfs/mounts
    """
    def __init__(self, env_vars:EnvVariables):
        self.env_vars = env_vars
        self.dbutils = env_vars.secret_utils.dbutils

    def mount_container(self, mount_path: Text, container_name: Text, storage_account: Text) -> bool:
        """ Mount a container to mount_path

        Params:
        -----------
            - mount_path: mount path of a container
            - container_name: azure container name
            - storage_account: azure storage account

        Return:
        -----------
            - True - mount container successfully otherwise False
        """
        logger.info("mount_container() - container_name: %s - storage_account: %s - mount_path: %s", container_name, storage_account, mount_path)
        if self.dbutils and mount_path and container_name and storage_account:
            if not any(mount.mountPoint == mount_path for mount in self.dbutils.fs.mounts()):
                try:
                    app_conf = self.env_vars.az_app_conf

                    configs = {
                        "fs.azure.account.auth.type": "OAuth",
                        "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
                        "fs.azure.account.oauth2.client.id": app_conf.get_client_id(),
                        "fs.azure.account.oauth2.client.secret": app_conf.get_client_secret(),
                        "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{app_conf.get_tenant_name()}/oauth2/token"
                    }
                    logger.info("mount_container() - configs: %s", configs)
                    self.dbutils.fs.mount(
                        source=f"abfss://{container_name}@{storage_account}.dfs.core.windows.net/",
                        mount_point=mount_path,
                        extra_configs=configs)
                    return True
                except Exception as ex:
                    logger.warning("mount_container() - mount_path: %s - error: %s", mount_path, ex)
        return False

    def unmount_container(self, mount_path: Text) -> bool:
        """ UnMount existing container

        Params:
        -----------
            - mount_path: mounted path of a container

        Return:
        -----------
            - True - unmount container successfully otherwise False
        """
        if self.dbutils and mount_path:
            if any(mount.mountPoint == mount_path for mount in self.dbutils.fs.mounts()):
                try:
                    self.dbutils.fs.unmount(mount_path)
                    return True
                except Exception as ex:
                    logger.warning("unmount_container() - mount_path: %s - error: %s", mount_path, ex)
        return False

    def mount_az_containers(self):
        """ Mount oboreport containers for data files and checkpoint
        """
        if self.env_vars:
            blob_container_confs = self.env_vars.dbx_conf.get_mount_blob_containers()
            for item in blob_container_confs:
                logger.info("mount_az_containers - map name: %s, storage_account: %s, container_name: %s", item.conf_name, item.storage_account, item.container_name)
                _mount_status = self.mount_container(
                    mount_path=item.mount_path,
                    container_name=item.container_name,
                    storage_account=item.storage_account,
                )
                logger.warning("mount_az_containers() - status: %s - mount_path: %s", _mount_status, item.mount_path)


    def unmount_az_containers(self):
        """ Unmount containers for data files and checkpoint
        """
        if self.env_vars:
            blob_container_confs = self.env_vars.dbx_conf.get_mount_blob_containers()
            for item in blob_container_confs:
                logger.info("unmount_az_containers() - mount_path: %s", item.mount_path)
                _unmount_status = self.unmount_container(
                    mount_path=item.mount_path,
                )
                logger.warning(f"unmount_az_containers() - status: %s", _unmount_status)
