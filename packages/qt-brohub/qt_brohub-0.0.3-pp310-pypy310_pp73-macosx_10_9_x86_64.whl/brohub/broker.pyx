from brohub.broker_base import BrokerBase
from brohub.broker_factory import BrokerFactory
from brohub.brokers import Brokers
from brohub.utils import BaseEnum


class AuthenticationMethods(BaseEnum):
    USERNAME_PASSWORD = "username and password"
    EMAIL_PASSWORD = "email and password"


def authenticate(broker_name: Brokers, auth_method: AuthenticationMethods, **kwargs) -> BrokerBase:
    broker = BrokerFactory.create_broker(broker_name)
    
    if auth_method == AuthenticationMethods.USERNAME_PASSWORD:
        broker.authenticate_with_username_password(**kwargs)
    elif auth_method == AuthenticationMethods.EMAIL_PASSWORD:
        broker.authenticate_with_email_password(**kwargs)
    else:
        raise ValueError(f"Unsupported authentication method: {auth_method}")

    return broker

def logout(broker_connection: BrokerBase, auth_method: AuthenticationMethods, **kwargs) -> None:
    if auth_method == AuthenticationMethods.USERNAME_PASSWORD:
        broker_connection.logout_with_username_password(**kwargs)
    else:
        raise ValueError(f"Unsupported logout method: {auth_method}")