import json

import degiro_connector.core.helpers.pb_handler as pb_handler
from degiro_connector.trading.api import API as DegiroAPI
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
    ProductsInfo,
    Update,
)

from brohub.broker_base import BrokerBase
from brohub.utils import get_exchange_mic_to_suffix_dict


class BrokerDeGiro(BrokerBase):
    def __init__(self):
        self.int_account = None
        self.trading_api = None

    def _create_and_connect_api(self, username, password):
        trading_api = DegiroAPI(Credentials(
            username=username,
            password=password,
            int_account=self.int_account
        ))
        trading_api.connect()
        return trading_api

    def authenticate_with_username_password(self, **kwargs) -> None:
        username = kwargs.get("username")
        password = kwargs.get("password")
        self.int_account = kwargs.get("int_account")

        if not username or not password:
            raise ValueError("Both 'username' and 'password' must be provided.")

        trading_api = self._create_and_connect_api(username, password)

        if not self.int_account:
            client_details_table = trading_api.get_client_details()
            self.int_account = client_details_table["data"]["intAccount"]

            trading_api.logout()
            trading_api = self._create_and_connect_api(username, password)

        self.trading_api = trading_api

    def authenticate_with_email_password(self, **kwargs):
        raise NotImplementedError("DEGIRO does not support authentication with email and password.")

    def authenticate_with_token(self, **kwargs):
        raise NotImplementedError("DEGIRO does not support authentication with tokens.")
    
    def logout_with_username_password(self, **kwargs):
        self.trading_api.logout()

    def get_current_stock_holdings(self):
        request_list = Update.RequestList()
        request_list.values.extend([
            Update.Request(option=Update.Option.PORTFOLIO, last_updated=0),
        ])

        update = self.trading_api.get_update(request_list=request_list)
        return json.dumps(self._aggregated_active_holdings(
            pb_handler.message_to_dict(message=update)['portfolio']['values']
        ))
    
    def _aggregated_active_holdings(self, all_holdings):
        active_holdings = []
        active_holding_ids = []
        for holding in all_holdings:
            if holding["value"] == 0.0 or not self._can_cast_to_int(holding["id"]):
                continue

            active_holdings.append(
                self._create_new_active_holding(
                    holding["id"],
                    holding["size"],                    
                )
            )

            # cast to an int for the get_products_info API
            active_holding_ids.append(int(holding["id"]))
        
        active_holdings_info = self._get_stock_info(active_holding_ids)["data"]

        exchange_info = self.trading_api.get_products_config(raw=True)["exchanges"]
        
        return self._map_holdings_with_info(active_holdings, active_holdings_info, exchange_info)
    
    def _create_new_active_holding(self, id, size):
        return {
            "internal_id": id,
            "isin": None,
            "ticker": None,
            "ticker_suffix": None,
            "company": None,
            "exchange_id": None,
            "exchange_name": None,
            "exchange_city": None,
            "exchange_country": None,
            "currency": None,
            "quantity": size
        }
        
    def _get_stock_info(self, ids):
        request = ProductsInfo.Request()
        request.products.extend(ids)

        return self.trading_api.get_products_info(
            request=request,
            raw=True,
        )

    def _map_holdings_with_info(self, holdings, holdings_info, exchanges_info):
        exchange_mic_to_suffix_dict = get_exchange_mic_to_suffix_dict()

        for holding in holdings:
            holding_info = holdings_info[holding["internal_id"]]
            exchange_index = next((index for index, exchange_info in enumerate(exchanges_info) if exchange_info['id'] == int(holdings_info[holding["internal_id"]]["exchangeId"])), None)

            holding.update({
                "isin": holding_info["isin"],
                "ticker": holding_info["symbol"],
                "company": holding_info["name"],
                "exchange_id": holding_info["exchangeId"],
                "exchange_name": exchanges_info[exchange_index]["name"],
                "exchange_city": exchanges_info[exchange_index]["city"],
                "exchange_country": exchanges_info[exchange_index]["country"],
                "currency": holding_info["currency"],
                "ticker_suffix": self._get_ticker_with_suffix(
                    holding_info["symbol"], 
                    exchanges_info[exchange_index]["micCode"], 
                    exchanges_info[exchange_index]["country"], 
                    exchange_mic_to_suffix_dict
                ),
                "internal_id": int(holding["internal_id"])
            })

        return holdings
    
    def _get_ticker_with_suffix(self, ticker_name, exchange_mic, exchange_country, exchange_mic_to_suffix_dict):
        suffix = exchange_mic_to_suffix_dict.get(exchange_mic)

        if not suffix or exchange_country == "US":
            return ticker_name

        return f"{ticker_name}.{suffix}"

    def _can_cast_to_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False
