import logging
from abc import ABC, abstractmethod

from typing import Union
from datetime import datetime, timedelta

import pandas as pd

from snowflake.snowpark import Session, Table, DataFrame, MergeResult
from snowflake.snowpark.types import StructType
from snowflake.snowpark.functions import when_matched, when_not_matched

from wells_data_pipeline_cores.commons import EnvVariables, Utils

from wells_data_pipeline_cores.services.snow import SnowDataService

class WellsETLService(SnowDataService):
    """
     WellsETLService is base (abstract) class. It provides a common/utility methods to do data ingestion pipeline
    """
    def __init__(self, env_vars:EnvVariables):
        self.env_vars:EnvVariables = env_vars

        # keep snowpark Session connection
        self.session:Session = self._create_snowpark_session(env_vars=env_vars)

        # keep data_type and table_name mapping
        self._dtype_table_names_mapping:dict = {}

    def add_dtype_table_mapping(self, dtype:str, table_name:str) -> bool:
        if dtype is not None and table_name is not None:
            self._dtype_table_names_mapping[dtype] = table_name
            return True
        return False
        
    def add_dtype_table_mappings(self, dtype_table_mappings:dict) -> bool:
        if dtype_table_mappings is not None:
            self._dtype_table_names_mapping.update(dtype_table_mappings)
            return True
        return False
    
    def get_table_name_mapping(self, dtype: str):
        if dtype is not None:
            return self._dtype_table_names_mapping.get(dtype)
        return None

    def to_timestamp(self, dtime:Union[str, float, int, datetime]=None):
        """
        Utility method to convert str | float | int to Unix timestamp in millis seconds
        """
        try:
            if dtime is not None:
                if isinstance(dtime, str) or isinstance(dtime, datetime):
                    obj_dtime = Utils.to_datetime(dtime=dtime)
                    return Utils.to_timestamp(dtime=obj_dtime)
                elif isinstance(dtime, int) or isinstance(dtime, float):
                    return dtime
        except Exception as ex:
            logging.warning("WellsETLService-to_timestamp() - error: %s", ex)

        return None
    
    def generate_id(self, dtime:Union[str, float, int, datetime]=None, rig:str=None, well:str=None, wellbore:str=None) -> str:
        """
        Utility method to generate unique Id based on Rig | Well | Wellbore | Timestamp data.
        It will be used to support incremental update data to database
        """
        _timestamp = self.to_timestamp(dtime=dtime)
        
        return self.generate_id_from_list(data=[
                ("R", str(rig or '')),
                ("W", str(well or '')),
                ("WB", str(wellbore or '')),
                ("TS", str(_timestamp or '')),
            ])

    def generate_id_from_list(self, data:list[(str, str)]) -> str:
        """ 
        Utility method to generate unique Id based on dict[str,str] data.
        It will be used to support incremental update data to database
        Params:
            - data:list[(str, str)] : list of (key, value) pairs e.g: [(key1, value1), (key2, value2), (key3, value3)]
        
        """
        _id = None
        if data is not None:
            for (key, value) in data:
                if _id is None:
                    _id = f"{key}={value}"
                else:
                    _id = f"{_id}|{key}={value}"
        return _id

    def fill_na_missing_columns(self, expected_columns_names:list[str], df:pd.DataFrame=None)-> pd.DataFrame:
        """
        Utility method to fill missing colunms in pd.DataFrame with None value.
        Params:
            - expected_columns_names:list[str] - list of expected columns in the pd.DataFrame object.
            - df:pd.DataFrame - DataFrame object
        Return:
            - Updated pd.DataFrame object
        """
        if expected_columns_names is not None and df is not None:
            try:
                for col in expected_columns_names:
                    if col not in df.columns:
                        df[col] = None
            except Exception as ex:
                logging.warn("fill_na_missing_columns - error: %s", ex)
        return df

    @abstractmethod
    def load_data(self, file_path:str=None, data:pd.DataFrame=None, tbl_schema:StructType=None, data_type:str=None) -> pd.DataFrame:
        """
        Load data to Data frame.
        :return:
        """
        logging.info("load_data() - No Implementation!!! - Process - file_path: %s, data_type: %s", file_path, data_type)

    @abstractmethod
    def get_target_table(self, file_path:str=None, data_type:str=None) -> Table:
        """
        Get target table to merge.
        Params:
            - file_path:str (Optional): it is used by WellsETLService.process_etl_file_task(...) method to load data from a file system.
            - data_type:str : it is used to get table_name from dtype_table_name_mapping dictionary
        Return:
            - Snowpark Table instance with pattern
                - [table_name]_DEV: for dev environement (default)
                - [table_name]_STG: for stagging environement
                - [table_name]: for production environement
        """
        logging.info("get_target_table() - No Implementation!!! - Process - file_path: %s, data_type: %s", file_path, data_type)

    @abstractmethod
    def get_data_type(self, file_path:str) -> str:
        """
        Return data_type which is used to map to table_name output.
        Params:
            - file_path:str (Optional): it is used by WellsETLService.process_etl_file_task(...) method to load data from a file system.
        Return:
            - data type of dataset
        """
        return "dtype"

    def get_table_primary_keyname(self, file_path:str=None, data_type:str=None) -> str:
        """
        Return primary keyname of table for merging
        """
        log_func_name = "get_table_primary_keyname(...)"
        logging.info("%s - file_path: %s, data_type: %s", log_func_name, file_path, data_type)
        return "ID"

    def process_etl_task(self, file_path:str=None, data:pd.DataFrame=None, data_type:str=None) -> bool:
        """
        Process to load data from a [file] OR [data_frame + data-type] to a database table
        """
        log_func_name = "process_etl_task(...)"
        logging.info("%s - file_path: %s, data_type: %s", log_func_name, file_path, data_type)
        try:
            if data_type and (not data.empty):
                return self.process_etl_dataframe_task(data=data, data_type=data_type)
            
            if file_path:
                return self.process_etl_file_task(file_path=file_path)

            logging.info("%s - INFO: there is NO [file_path] or [DataFrame] data!", log_func_name)
        except Exception as ex:
            logging.error("%s - ERROR: %s", log_func_name, ex)
            
        return False

    def process_etl_file_task(self, file_path:str) -> bool:
        """
        Process to load data from a file to a database table
        """
        log_func_name = "process_etl_file_task(...)"
        
        data_type = self.get_data_type(file_path=file_path)

        logging.info("%s - file_path: %s - data_type: %s", log_func_name, file_path, data_type)
        try:
            _df_source = self.load_data(file_path=file_path)

            return self.process_etl_dataframe_task(data=_df_source, data_type=data_type)
        except Exception as ex:
            logging.error("%s - ERROR: %s", log_func_name, ex)
            
        return False
        
    def process_etl_dataframe_task(self, data:pd.DataFrame=None, data_type:str=None) -> bool:
        """
        Process to load data from a pd.DataFrame to a database table
        """
        log_func_name = "process_etl_dataframe_task(...)"
        logging.info("%s - data_type: %s", log_func_name, data_type)
        try:
            # get target table
            tbl_target = self.get_target_table(data_type=data_type)
            if tbl_target:
                logging.info("%s - process - target table: %s", log_func_name, tbl_target.table_name)

                if self._validate_schema(data=data, tbl_schema=tbl_target.schema):
                    logging.info("%s - process - Panda DataFrame Columns: %s", log_func_name, data.columns)

                    dd_source = self.session.create_dataframe(data=data)
                    logging.info("%s - process - snowpark DataFrame Columns: %s", log_func_name, dd_source.columns)

                    primary_key_name = self.get_table_primary_keyname(data_type==data_type)
                    logging.info("%s - process - primary_key_name: %s", log_func_name, primary_key_name)

                    result = self._upsert_data(tbl_target=tbl_target, dd_source=dd_source, primary_key_name=primary_key_name)
                    logging.info("%s - upsert data result: %s", log_func_name, result)

                    if result.rows_inserted == -1 or result.rows_updated == -1:
                        return False
                        
                    return True
                else:
                    logging.info("%s - INFO: there is NO data in data source table!", log_func_name)
            else:
                logging.info("%s - INFO: there is NO tbl_target table!", log_func_name)
        except Exception as ex:
            logging.error("%s - ERROR: %s", log_func_name, ex)
        
        return False

    def read_csv(self, file_path:str, tbl_schema:StructType = None) -> pd.DataFrame:
        try:
            # Let's import a new dataframe so that we can test this.
            #original = r"C:\Users\you\awesome_coding\file.csv" # <- Replace with your path.
            original = file_path
            delimiter = "," # Replace if you're using a different delimiter.

            logging.info("read_csv() - file_path:%s", file_path)

            # Get it as a pandas dataframe.
            df = pd.read_csv(original, sep = delimiter, encoding="unicode_escape")
            # Capitalize Column Names Using series.str.upper() Method
            df.columns = df.columns.str.upper()
            logging.info("read_csv() - DataFrame columns:%s", df.columns)

            # Verify columns with table schema, add missing columns with N/A value
            if tbl_schema:
                missing_fields = list(set(tbl_schema.names) - set(df.columns))
                logging.info("read_csv() - missing fields:%s", missing_fields)
                for field_name in missing_fields:
                    logging.info("read_csv() - add new field:%s", field_name)
                    df[field_name] = pd.NA

            # Drop any columns you may not need (optional).
            # df.drop(columns = ['A_ColumnName',
            #                       'B_ColumnName'],
            #                        inplace = True)

            # Rename the columns in the dataframe if they don't match your existing table.
            # This is optional, but ESSENTIAL if you already have created the table format
            # in Snowflake.
            # df.rename(columns={"A_ColumnName": "A_COLUMN", 
            #                       "B_ColumnName": "B_COLUMN"},
            #                        inplace=True)
            return df
        except Exception as ex:
            logging.error("read_csv - ERROR: %s", ex)

        # return an empty DataFrame object
        return pd.DataFrame()


