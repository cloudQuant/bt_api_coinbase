"""Coinbase orderbook data container."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.orderbooks.orderbook import OrderBookData
from bt_api_base.functions.utils import from_dict_get_string
from bt_api_base.logging_factory import get_logger

logger = get_logger("container")


class CoinbaseOrderBookData(OrderBookData):
    """Coinbase.

    Coinbase。
    """

    def __init__(
        self,
        order_book_info: str | dict,
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """Coinbase.

        Args: order_book_info: （JSON）
            symbol_name: 
            asset_type: （ "SPOT"）
            has_been_json_encoded: JSON
        """
        super().__init__(order_book_info, has_been_json_encoded)
        self.exchange_name = "COINBASE"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.order_book_data: Any = order_book_info if has_been_json_encoded else None
        self.order_book_symbol_name: str | None = None
        self.server_time: str | None = None
        self.bid_price_list: list[float] | None = None
        self.ask_price_list: list[float] | None = None
        self.bid_volume_list: list[float] | None = None
        self.ask_volume_list: list[float] | None = None
        self.bid_trade_nums: list[int] | None = None
        self.ask_trade_nums: list[int] | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> CoinbaseOrderBookData:
        """（）.

        Returns: CoinbaseOrderBookData: self

        Raises: NotImplementedError:
        """
        raise NotImplementedError("Subclasses must implement init_data")

    def get_all_data(self) -> dict[str, Any]:
        """.

        Returns: dict: 、、
        """
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "asset_type": self.asset_type,
                "symbol_name": self.symbol_name,
                "order_book_symbol_name": self.order_book_symbol_name,
                "local_update_time": self.local_update_time,
                "server_time": self.server_time,
                "bid_price_list": self.bid_price_list,
                "ask_price_list": self.ask_price_list,
                "bid_volume_list": self.bid_volume_list,
                "ask_volume_list": self.ask_volume_list,
                "bid_trade_nums": self.bid_trade_nums,
                "ask_trade_nums": self.ask_trade_nums,
            }
        return self.all_data

    def __str__(self) -> str:
        """JSON."""
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        """."""
        return self.__str__()

    def get_exchange_name(self) -> str:
        """.

        Returns: str: （"COINBASE"）
        """
        return self.exchange_name

    def get_local_update_time(self) -> float:
        """.

        Returns: float: （Unix）
        """
        return self.local_update_time

    def get_symbol_name(self) -> str:
        """.

        Returns: str:
        """
        return self.symbol_name

    def get_asset_type(self) -> str:
        """.

        Returns: str: （ "SPOT"）
        """
        return self.asset_type

    def get_server_time(self) -> str | None:
        """.

        Returns: str | None:
        """
        return self.server_time

    def get_bid_price_list(self) -> list[float] | None:
        """.

        Returns: list | None:
        """
        return self.bid_price_list

    def get_ask_price_list(self) -> list[float] | None:
        """.

        Returns: list | None:
        """
        return self.ask_price_list

    def get_bid_volume_list(self) -> list[float] | None:
        """.

        Returns: list | None:
        """
        return self.bid_volume_list

    def get_ask_volume_list(self) -> list[float] | None:
        """.

        Returns: list | None:
        """
        return self.ask_volume_list

    def get_bid_trade_nums(self) -> list[int] | None:
        """.

        Returns: list | None:
        """
        return self.bid_trade_nums

    def get_ask_trade_nums(self) -> list[int] | None:
        """.

        Returns: list | None:
        """
        return self.ask_trade_nums


class CoinbaseRequestOrderBookData(CoinbaseOrderBookData):
    """Coinbase REST API.

    API:
    {
        "pricebook": {
            "product_id": "BTC-USD",
            "bids": [{"price": "49999", "size": "1.5"}, ...],
            "asks": [{"price": "50001", "size": "1.8"}, ...],
            "time": "2024-01-01T00:00:00Z"
        }
    }
    """

    def init_data(self) -> CoinbaseRequestOrderBookData:
        """REST API.

        Returns: CoinbaseRequestOrderBookData: self
        """
        if not self.has_been_json_encoded:
            self.order_book_data = json.loads(self.order_book_info)
            self.has_been_json_encoded = True
        if isinstance(self.order_book_data, str):
            self.order_book_data = json.loads(self.order_book_data)
        if self.has_been_init_data:
            return self
        try:
            if isinstance(self.order_book_data, dict):
                pricebook = self.order_book_data.get("pricebook", self.order_book_data)
                self.order_book_symbol_name = from_dict_get_string(pricebook, "product_id")
                self.server_time = from_dict_get_string(pricebook, "time")

                bids = pricebook.get("bids", [])
                asks = pricebook.get("asks", [])

                self.bid_price_list = []
                self.bid_volume_list = []
                for bid in bids:
                    if isinstance(bid, dict):
                        self.bid_price_list.append(float(bid.get("price", 0)))
                        self.bid_volume_list.append(float(bid.get("size", 0)))
                    elif isinstance(bid, (list, tuple)) and len(bid) >= 2:
                        self.bid_price_list.append(float(bid[0]))
                        self.bid_volume_list.append(float(bid[1]))

                self.ask_price_list = []
                self.ask_volume_list = []
                for ask in asks:
                    if isinstance(ask, dict):
                        self.ask_price_list.append(float(ask.get("price", 0)))
                        self.ask_volume_list.append(float(ask.get("size", 0)))
                    elif isinstance(ask, (list, tuple)) and len(ask) >= 2:
                        self.ask_price_list.append(float(ask[0]))
                        self.ask_volume_list.append(float(ask[1]))

        except Exception as e:
            logger.error(f"Error parsing orderbook data: {e}", exc_info=True)
            self.order_book_data = {}
        self.has_been_init_data = True
        return self
