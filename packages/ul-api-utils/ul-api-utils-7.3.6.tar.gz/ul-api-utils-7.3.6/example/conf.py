import os

from ul_db_utils.modules.db import DbConfig

from ul_api_utils.modules.api_sdk import ApiSdk
from ul_api_utils.modules.api_sdk_config import ApiSdkConfig, ApiSdkIdentifyTypeEnum
from example.permissions import permissions

sdk = ApiSdk(ApiSdkConfig(
    service_name='example_service',
    permissions=permissions,
    rate_limit_storage_uri='redis://localhost:16379',
    rate_limit_identify=ApiSdkIdentifyTypeEnum.JWT_USER_ID,
))


fake_models_dir = os.path.join(os.path.dirname(__file__), 'models')


db_config = DbConfig(uri='postgresql://admin:admin@localhost:45432/example', models_path=fake_models_dir)
