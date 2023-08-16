import logging

from typing import Dict, Any
from decouple import config
from pathlib import Path
import yaml

class DevUtils():
    """ DevUtils class is used in development (Local Machine) environement to load yaml configuration
        It can be used in Notebooks or Python test code
    """
    def get_conf_folder(self) -> Path:
        root_path = DevUtils._read_app_root_folder()
        if root_path is not None:
            logging.info("get_conf_folder() - root_path:  %s",root_path)
            return root_path / "conf"
        else:
            logging.info("get_conf_folder() - load default root folder")
            return Path(__file__).parent.parent.parent / "conf"

    def get_conf_tasks_folder(self) -> Path:
        root_path = DevUtils._read_app_root_folder()
        if root_path is not None:
            logging.info("get_conf_tasks_folder() - root_path:  %s",root_path)
            return root_path / "conf/tasks"
        else:
            logging.info("get_conf_tasks_folder() - load default root folder")
            return Path(__file__).parent.parent.parent / "conf/tasks"

    def read_config(self, conf_file_name) -> Dict[str, Any]:
        try:
            conf_folder = self.get_conf_tasks_folder()
            conf_file_path = conf_folder / conf_file_name
            logging.info("read_config() - conf_file_path: %s", conf_file_path)
            return DevUtils._read_config(conf_file=conf_file_path)
        except Exception as ex:
            logging.error("read_config() - Error: %s", ex)
            return {}

    @staticmethod
    def _read_app_root_folder() -> Path:
        """
        Try to retive App's ROOT FOLDER from environement 
        """
        try:
            vars_names = [
                "WELLS_DATA_PIPELINE_ROOT",
                "WELLS_DATA_ROOT",
                "WELLS_APP_ROOT",
                "WELLS_DBX_JOBS_ROOT",
                "WELLS_JOBS_ROOT",
            ]

            for var_name in vars_names:
                root_path = config(var_name, default=None)
                if root_path is not None:
                    return Path(root_path)

        except Exception as ex:
            logging.info(" %s", ex)
        return None

    @staticmethod
    def _read_config(conf_file) -> Dict[str, Any]:
        config = yaml.safe_load(Path(conf_file).read_text())
        return config

    def read_dev_config(self) -> Dict[str, Any]:
        return self.read_config(conf_file_name="app_config_dev.yml")

    def read_staging_config(self) -> Dict[str, Any]:
        return self.read_config(conf_file_name="app_config_staging.yml")

    def read_prod_config(self) -> Dict[str, Any]:
        return self.read_config(conf_file_name="app_config_prod.yml")

