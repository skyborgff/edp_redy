import uuid
from typing import Callable

from awscrt import auth, io, mqtt
from awscrt.mqtt import Connection
from awsiot import mqtt_connection_builder

from .authenticate import AuthenticationResult
from .consts import POOL_REGION, POOL_ID, HOST
from .usermanagement.usermanagement import User


class EDPMQTT:
    authentication: AuthenticationResult = None
    connection: Connection

    def __init__(self, authentication: AuthenticationResult):
        self.authentication = authentication

    def get_cognito_provider(self, user: User) -> auth.AwsCredentialsProvider:
        cognito_endpoint = f"cognito-identity.{POOL_REGION}.amazonaws.com"
        credentials_provider = auth.AwsCredentialsProvider.new_cognito(
            endpoint=cognito_endpoint,
            identity=user.identity_id,
            tls_ctx=io.ClientTlsContext(io.TlsContextOptions()),
            logins=[(f"{cognito_endpoint}/{POOL_ID}", self.authentication.IdToken)]
        )
        return credentials_provider

    def connect(self, user: User):
        self.connection = mqtt_connection_builder.websockets_with_default_aws_signing(
            endpoint=HOST,
            region=POOL_REGION,
            port=443,
            credentials_provider=self.get_cognito_provider(user),
            http_proxy_options=None,
            # ca_filepath=rootCAPath,
            # on_connection_interrupted=on_connection_interrupted,
            # on_connection_resumed=on_connection_resumed,
            # on_connection_success=on_connection_success,
            # on_connection_failure=on_connection_failure,
            # on_connection_closed=on_connection_closed,
            client_id=f"PORTAL_{str(uuid.uuid4())}",
            clean_session=False,
            keep_alive_secs=60)

        connect_future = self.connection.connect()
        # Future.result() waits until a result is available
        return connect_future
        # return connect_future.result()

    def subscribe(self, topic: str, callback: Callable = None):
        subscribe_future, packet_id = self.connection.subscribe(
            topic=topic,
            qos=mqtt.QoS.AT_LEAST_ONCE, callback=callback)
        return subscribe_future
        # return subscribe_future.result()

    def publish(self, topic: str, message: str):
        publish_future, packet_id = self.connection.publish(
            topic=topic,
            payload=message,
            qos=mqtt.QoS.AT_LEAST_ONCE)
        return publish_future
        # return publish_future.result()
