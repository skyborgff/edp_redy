from .authenticate import authenticate, AuthenticationResult
from .edp_mqtt import EDPMQTT
from .usermanagement.usermanagement import UserManagement


class Redy:
    authentication: AuthenticationResult = None
    user_management: UserManagement
    mqtt: EDPMQTT

    def __init__(self, username: str, password: str):
        self.authentication = authenticate(username, password)
        self.user_management = UserManagement(self.authentication)
        self.mqtt = EDPMQTT(self.authentication)
        # user = self.user_management.user()
        # self.mqtt.connect(user)
