# Wells Data Pipeline Cores library

The `wells-data-pipeline-cores` library supports datasources  integration:
- Support application configuration - [EnvVariables](https://github.com/ExxonMobil/wells-data-pipeline-cores/blob/develop/wells_data_pipeline_cores/commons/env_variables.py) - in the `.\conf\tasks\app_config_dev|staging|prod.yml` file, and secret in the Local System environement (`.env` file) or Az KeyVault in the Databricks environement.
- Support Azure AD Authentication - [AzAuthzService](https://github.com/ExxonMobil/wells-data-pipeline-cores/blob/develop/wells_data_pipeline_cores/services/cores/az_ad_authz_service.py) - to retrieve Azure service's JWT Token.
- Support Az Storage Account - [AzStorageAccountService](https://github.com/ExxonMobil/wells-data-pipeline-cores/blob/develop/wells_data_pipeline_cores/services/cores/az_storage_account_service.py) - to Mount/UnMount a Az Storage Container at the runtime.
- Support email out - [SendEmailService](https://github.com/ExxonMobil/wells-data-pipeline-cores/blob/develop/wells_data_pipeline_cores/services/cores/send_email_service.py) - to send an email from Databrick Jobs by using MuleSoft SMTP API.
- Support Azure CosmosDB integration - [AzCosmosDataService](https://github.com/ExxonMobil/wells-data-pipeline-cores/blob/develop/wells_data_pipeline_cores/services/cosmos/az_cosmos_data_service.py)
- Support Azure ADX integration - [AzAdxDataService](https://github.com/ExxonMobil/wells-data-pipeline-cores/blob/develop/wells_data_pipeline_cores/services/adx/az_adx_data_service.py)
- Support Snowflake integration with Snowpark - [SnowDataService](https://github.com/ExxonMobil/wells-data-pipeline-cores/blob/develop/wells_data_pipeline_cores/services/snow/snow_data_service.py)
- Support abstract ETL class - [WellsETLService](https://github.com/ExxonMobil/wells-data-pipeline-cores/blob/develop/wells_data_pipeline_cores/services/etl/wells_etl_service.py) to load a dataframe to an table in the Snowflake

While using this project, you need Python 3.10 and `pip` or `conda` for package management.

## Wells Data Pipeline Cores library setup

The [wells-data-pipeline-cores](https://github.com/ExxonMobil/wells-data-pipeline-cores) library will require the following dependencies to enable supported features/integrations in the [setup.py](./setup.py) and [deployment.yml](./conf/deployment.yml) files:

### Support application configuration:
- pyyaml
- python-decouple

### Support Azure AD Authentication:
- msal==1.23.0
- azure-identity==1.13.0

### Support Az Storage Account:
- dbutils (default pacakge in the Databricks runtime lib)

### Support email out:
- requests
- Azure AD authentication - AzAuthzService

### Support Azure CosmosDB integration:
- azure-cosmos==4.4.0

### Support Azure ADX integration:
- azure-kusto-data==4.2.0

### Support Snowflake integration with Snowpark:
- snowflake-connector-python[pandas]==2.9.0
- snowflake-snowpark-python[pandas]==1.5.1

Libraries dependencies:

- The `snowpark:1.5.1, snow-connector:2.9.0` requires `pyarrow==8.0.0` library.
- The `snowpark:1.6.x, snow-connector:3.x.y` requires `pyarrow==10.0.1` library. It conflicts with default Databrick's runtime 13.2 libraries.

Note: The DBX runtime 13.2 includes `pyarrow==8.0.0, pandas==1.4.4` libraries.

## Requirements.

Python 3.10+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import wells-data-pipeline-cores
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import wells-data-pipeline-cores
```

### Tools - Python symtax checking

- stop the build if there are Python syntax errors or undefined names

    ```
    flake8 ./wells_data_pipeline_cores --count --select=E9,F63,F7,F82 --show-source --statistics

    flake8 ./ipy-notebooks --count --select=E9,F63,F7,F82 --show-source --statistics
    ```

- exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide

    ```
    flake8 ./wells_data_pipeline_cores --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

    flake8 ./ipy-notebooks --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    ```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import wells-data-pipeline-cores
from pprint import pprint

# TODO - add sample code here....

```

## Author


