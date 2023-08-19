from abc import ABC, abstractmethod


class BrokerBase(ABC):    
    @abstractmethod
    def authenticate_with_email_password(self, **kwargs) -> None:
        pass

    @abstractmethod
    def authenticate_with_username_password(self, **kwargs) -> None:
        pass
    
    @abstractmethod
    def authenticate_with_token(self, **kwargs) -> None:
        pass
    
    @abstractmethod
    def logout_with_username_password(self, **kwargs) -> None:
        pass

    @abstractmethod
    def get_current_stock_holdings(self):
        pass