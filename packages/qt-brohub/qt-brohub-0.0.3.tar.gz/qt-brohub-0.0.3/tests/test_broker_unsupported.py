import pytest

from brohub.broker import AuthenticationMethods, authenticate


class TestBrokerUnsupported:
    def test_unsupported_broker(self) -> None:
        broker = "non_existing_broker"
        with pytest.raises(ValueError) as exc_info:
            authenticate(broker, AuthenticationMethods.USERNAME_PASSWORD)

        assert str(exc_info.value) == f"Unsupported broker: {broker}"
