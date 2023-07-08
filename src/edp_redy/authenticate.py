import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

import requests
from awscrt import io
from warrant.aws_srp import AWSSRP

from .consts import POOL_ID, CLIENT_ID, POOL_REGION

io.init_logging(io.LogLevel.Error, 'stderr')


def authenticate(USERNAME, PASSWORD):
    aws = AWSSRP(username=USERNAME, password=PASSWORD, pool_id=POOL_ID, client_id=CLIENT_ID, pool_region=POOL_REGION)
    authentication = AuthenticationResult.from_dict(json.loads(aws.authenticate_user()))
    return authentication


@dataclass
class NewDeviceMetadata:
    DeviceKey: str
    DeviceGroupKey: str

    @staticmethod
    def from_dict(obj: Any) -> 'NewDeviceMetadata':
        _DeviceKey = str(obj.get("DeviceKey"))
        _DeviceGroupKey = str(obj.get("DeviceGroupKey"))
        return NewDeviceMetadata(_DeviceKey, _DeviceGroupKey)


@dataclass
class AuthenticationResult:
    AccessToken: str
    ExpiresIn: int
    ExpiresAt: datetime
    TokenType: str
    RefreshToken: str
    IdToken: str
    NewDeviceMetadata: NewDeviceMetadata

    @staticmethod
    def from_dict(obj: Any) -> 'AuthenticationResult':
        _AccessToken = str(obj.get("AccessToken"))
        _ExpiresIn = int(obj.get("ExpiresIn"))
        _ExpiresAt = datetime.now() + timedelta(seconds=_ExpiresIn)
        _TokenType = str(obj.get("TokenType"))
        _RefreshToken = str(obj.get("RefreshToken"))
        _IdToken = str(obj.get("IdToken"))
        _NewDeviceMetadata = NewDeviceMetadata.from_dict(obj.get("NewDeviceMetadata"))
        return AuthenticationResult(_AccessToken, _ExpiresIn, _ExpiresAt, _TokenType, _RefreshToken, _IdToken,
                                    _NewDeviceMetadata)

    def get(self, *args, **kwargs):
        # TODO: check if token is still valid
        return requests.get(headers={"Authorization": self.IdToken}, *args, **kwargs)
