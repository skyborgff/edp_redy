from datetime import datetime
from typing import Any, TypeVar, Type, cast
from uuid import UUID

import dateutil.parser
import requests
from authenticate import AuthenticationResult
from consts import ENDPOINT
from helpers import from_str, from_datetime, from_none


class User:
    user_id: UUID
    first_name: str
    last_name: str
    email: str
    creation_date: datetime
    last_login: None
    language_code: str
    identity_id: str

    def __init__(self, user_id: UUID, first_name: str, last_name: str, email: str, creation_date: datetime,
                 last_login: None, language_code: str, identity_id: str) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.creation_date = creation_date
        self.last_login = last_login
        self.language_code = language_code
        self.identity_id = identity_id

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        user_id = UUID(obj.get("userId"))
        first_name = from_str(obj.get("firstName"))
        last_name = from_str(obj.get("lastName"))
        email = from_str(obj.get("email"))
        creation_date = from_datetime(obj.get("creationDate"))
        last_login = from_none(obj.get("lastLogin"))
        language_code = from_str(obj.get("languageCode"))
        identity_id = from_str(obj.get("identityId"))
        return User(user_id, first_name, last_name, email, creation_date, last_login, language_code,
                    identity_id)


class UserResponse:
    user: User

    def __init__(self, user: User) -> None:
        self.user = user

    @staticmethod
    def from_dict(obj: Any) -> 'UserResponse':
        assert isinstance(obj, dict)
        user = User.from_dict(obj.get("User"))
        return UserResponse(user)


class UserManagement:
    authentication: AuthenticationResult = None
    endpoint = ENDPOINT + "/usermanagement"

    def __init__(self, authentication: AuthenticationResult):
        self.authentication = authentication

    def user(self) -> User:
        response = self.authentication.get(f"{self.endpoint}/user")
        user_response = UserResponse.from_dict(response.json())
        return user_response.user
