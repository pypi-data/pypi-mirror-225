from brohub.broker_base import BrokerBase
from brohub.broker_degiro import BrokerDeGiro
from brohub.brokers import Brokers


class BrokerFactory:
    @staticmethod
    def create_broker(broker_name: Brokers) -> BrokerBase:
        if broker_name == Brokers.DEGIRO:
            return BrokerDeGiro()
        else:
            raise ValueError(f"Unsupported broker: {broker_name}")