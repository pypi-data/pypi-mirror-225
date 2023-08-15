from __future__ import absolute_import

import logging

# support Snowflake
try:
    from wells_data_pipeline_cores.services.snow.snow_data_service import SnowDataService
except Exception as ex:
    logging.warning("Export SnowDataService error - %s", ex)