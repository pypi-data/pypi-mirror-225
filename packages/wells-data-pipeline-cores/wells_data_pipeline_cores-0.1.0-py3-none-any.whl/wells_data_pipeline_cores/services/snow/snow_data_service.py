import logging
from abc import ABC, abstractmethod

import pandas as pd

from snowflake.snowpark import Session, Table, DataFrame, MergeResult
from snowflake.snowpark.types import StructType
from snowflake.snowpark.functions import when_matched, when_not_matched

from wells_data_pipeline_cores.commons import EnvVariables

class SnowDataService(ABC):
    """
    Snowpark Developer Guide for Python: https://docs.snowflake.com/en/developer-guide/snowpark/python/index
    Snowpark Library for Python API Reference: https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/index
    Working with DataFrames in Snowpark Python: https://docs.snowflake.com/en/developer-guide/snowpark/python/working-with-dataframes
    """
    def __init__(self, env_vars:EnvVariables):
        self.env_vars:EnvVariables = env_vars
        self.session:Session = self._create_snowpark_session(env_vars=env_vars)

    def close_session(self):
        self._close_snowpark_session(session=self.session)

    def _validate_schema(self, data:pd.DataFrame=None, tbl_schema:StructType=None):
        """
        Return TRUE if there is NO missing fields in the table
        """
        if not data.empty and tbl_schema:
            missing_fields = list(set(tbl_schema.names) - set(data.columns))
            logging.info("_validate_schema() - missing fields: %s", missing_fields)
            return (len(missing_fields) == 0)
        return False

    def use_session(self, database:str=None, schema:str=None, role:str=None, warehouse:str=None):
        try:
            if database is not None:
                self.session.use_database(database=database)

            if schema is not None:
                self.session.use_schema(schema=schema)

            if role is not None:
                self.session.use_role(role=role)

            if warehouse is not None:
                self.session.use_warehouse(warehouse=warehouse)        

        except Exception as ex:
            logging.info("use_session() - error: %s", ex)
    @staticmethod
    def _close_snowpark_session(session:Session):
        try:
            if session is not None:
                session.close()
        except Exception as ex:
            pass

    @staticmethod
    def _create_snowpark_session(env_vars:EnvVariables) -> Session:
        conn_parameters = env_vars.kepler_conf.get_snowpark_conn_params()
        return Session.builder.configs(conn_parameters).create()

    @staticmethod
    def _get_target_table(session:Session, table_name:str) -> Table:
        return session.table(name=table_name)

    @staticmethod
    def _upsert_data(tbl_target:Table, dd_source:DataFrame, primary_key_name:str = "ID") -> MergeResult:
        """ 
        https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.Table.merge#snowflake.snowpark.Table.merge
        """
        merge_update_dict = {}
        merge_insert_dict = {}

        if tbl_target and dd_source:
            # check columns names
            missing_cols = list(set(tbl_target.columns) - set(dd_source.columns))
            if len(missing_cols) > 0:
                logging.error("upsert_data(....) - missing columns in dataframe source: ", missing_cols)
            else:
                for col_name in tbl_target.columns:
                    merge_insert_dict.update(
                        {col_name: dd_source[col_name]}
                    )

                    if col_name is not primary_key_name:
                        merge_update_dict.update(
                            {col_name: dd_source[col_name]}
                        )

                merge_result = tbl_target.merge(
                    source=dd_source,
                    join_expr=(tbl_target[primary_key_name] == dd_source[primary_key_name]),
                    clauses=[
                        when_matched().update(merge_update_dict),
                        when_not_matched().insert(merge_insert_dict)
                    ]
                )

                return merge_result
        
        return MergeResult(rows_inserted=-1, rows_updated=-1, rows_deleted=0)
