from enum import Enum
from typing import List, Optional, Callable, Union

from pydantic import BaseModel, Extra

from ul_api_utils.access import PermissionRegistry, PermissionDefinition
from ul_api_utils.modules.api_sdk_jwt import ApiSdkJwt


def join_route_paths(prev_sect: str, next_sect: str) -> str:
    return prev_sect.rstrip('/') + '/' + next_sect.lstrip('/')


class ApiSdkIdentifyTypeEnum(Enum):
    DISABLED = 'DISABLED'
    CLIENT_IP = 'IP'
    JWT_USER_ID = 'JWT_USER_ID'

    def __repr__(self) -> str:
        return f'{type(self).__name__}.{self.name}'


class ApiSdkHttpAuth(BaseModel):
    realm: str = 'Hidden Zone'
    scheme: str = 'Basic'


class ApiSdkConfig(BaseModel):
    service_name: str
    permissions: Optional[Union[Callable[[], PermissionRegistry], PermissionRegistry]] = None
    permissions_check_enabled: bool = True  # GLOBAL CHECK OF ACCESS AND PERMISSIONS ENABLE
    permissions_validator: Optional[Callable[[ApiSdkJwt, PermissionDefinition], bool]] = None

    jwt_validator: Optional[Callable[[ApiSdkJwt], bool]] = None
    jwt_environment_check_enabled: bool = True

    http_auth: Optional[ApiSdkHttpAuth] = None

    static_url_path: Optional[str] = None

    not_found_template: Optional[str] = None

    rate_limit: Union[str, List[str]] = '100/minute'  # [count (int)] [per|/] [second|minute|hour|day|month|year][s]
    rate_limit_storage_uri: str = ''  # supports url of redis, memcached, mongodb
    rate_limit_identify: Union[ApiSdkIdentifyTypeEnum, Callable[[], str]] = ApiSdkIdentifyTypeEnum.DISABLED  # must be None if disabled

    api_route_path_prefix: str = '/api'

    class Config:
        extra = Extra.forbid
        allow_mutation = False
        frozen = True
        arbitrary_types_allowed = True
