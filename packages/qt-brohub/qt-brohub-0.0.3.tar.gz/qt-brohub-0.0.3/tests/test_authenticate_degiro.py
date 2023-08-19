import unittest
from unittest.mock import MagicMock, patch

import pytest

from brohub.broker import AuthenticationMethods, authenticate
from brohub.broker_base import BrokerBase
from brohub.broker_degiro import BrokerDeGiro
from brohub.brokers import Brokers


class TestAuthenticateDegiro(unittest.TestCase):
    def test_authenticate_degiro_without_username_and_password(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            authenticate(Brokers.DEGIRO, AuthenticationMethods.USERNAME_PASSWORD)

        assert str(exc_info.value) == "Both 'username' and 'password' must be provided."

    def test_authenticate_degiro_without_password(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            authenticate(
                Brokers.DEGIRO,
                AuthenticationMethods.USERNAME_PASSWORD,
                username="username",
            )

        assert str(exc_info.value) == "Both 'username' and 'password' must be provided."

    def test_authenticate_degiro_without_username(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            authenticate(
                Brokers.DEGIRO,
                AuthenticationMethods.USERNAME_PASSWORD,
                password="password",
            )

        assert str(exc_info.value) == "Both 'username' and 'password' must be provided."

    def test_authenticate_degiro_invalid_username_password(self) -> None:
        with pytest.raises(ConnectionError) as exc_info:
            authenticate(
                Brokers.DEGIRO,
                AuthenticationMethods.USERNAME_PASSWORD,
                username="username",
                password="password",
            )

        assert (
            str(exc_info.value)
            == "400 Client Error:  for url: https://trader.degiro.nl/login/secure/login"
        )

    def test_authenticate_degiro_without_email_password(self) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            authenticate(
                Brokers.DEGIRO,
                AuthenticationMethods.EMAIL_PASSWORD,
                email="test@test.com",
                password="password123",
            )

        assert (
            str(exc_info.value)
            == "DEGIRO does not support authentication with email and password."
        )

    @patch("brohub.broker_factory.BrokerFactory.create_broker")
    @patch.object(BrokerDeGiro, "_create_and_connect_api")
    def test_authenticate_degiro_valid_username_password(
        self, mock_api: MagicMock, mock_create_broker: BrokerBase
    ) -> None:
        # Mock the create_broker method to return a BrokerDeGiro instance
        mock_broker = BrokerDeGiro()
        mock_create_broker.return_value = mock_broker

        # Mock the _create_and_connect_api to just set the trading_api attribute
        mock_api.return_value = MagicMock()

        broker = authenticate(
            Brokers.DEGIRO,
            AuthenticationMethods.USERNAME_PASSWORD,
            username="testuser",
            password="testpass",
        )

        self.assertIsInstance(broker, BrokerDeGiro)
