"""
Coinbase Trade Data Container

This module uses a template pattern for parsing trade data across different sources:
- CoinbaseTradeData: Base template for REST API data
- CoinbaseWssTradeData: WebSocket data variant (field name differences)
- CoinbaseRequestTradeData: REST API historical fills variant

Pattern: Subclasses override init_data() to handle source-specific field mappings,
while reusing common initialization logic from the parent class.
"""

from __future__ import annotations

import json
import time

from bt_api_base.containers.trades.trade import TradeData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string
from bt_api_base.logging_factory import get_logger

_logger = get_logger("coinbase_trade")


class CoinbaseTradeData(TradeData):
    """Coinbase（，REST API）"""

    def __init__(self, trade_info, symbol_name, asset_type, has_been_json_encoded=False):
        """__init__ method"""
        super().__init__(trade_info, has_been_json_encoded)
        self.exchange_name = "COINBASE"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        # If already JSON encoded, parse it to dict; otherwise store raw
        if has_been_json_encoded:
            self.trade_data = json.loads(trade_info) if isinstance(trade_info, str) else trade_info
        else:
            self.trade_data = None
        self.trade_id = None
        self.order_id = None
        self.product_id = None
        self.trade_type = None
        self.side = None
        self.price = None
        self.size = None
        self.commission = None
        self.trade_time = None
        self.liquidity_indicator = None
        self.all_data = None
        self.has_been_init_data = False

    def init_data(self):
        """init_data method"""
        if not self.has_been_json_encoded:
            self.trade_data = json.loads(self.trade_info)
            self.has_been_json_encoded = True
        # Ensure trade_data is a dict
        if isinstance(self.trade_data, str):
            self.trade_data = json.loads(self.trade_data)
        if self.has_been_init_data:
            return self
        try:
            # Parse trade data
            if isinstance(self.trade_data, dict):
                self.trade_id = from_dict_get_string(self.trade_data, "entry_id")
                self.order_id = from_dict_get_string(self.trade_data, "order_id")
                self.product_id = from_dict_get_string(self.trade_data, "product_id")
                self.trade_type = from_dict_get_string(self.trade_data, "trade_type")
                self.side = from_dict_get_string(self.trade_data, "side")

                self.price = from_dict_get_float(self.trade_data, "price")
                self.size = from_dict_get_float(self.trade_data, "size")
                self.commission = from_dict_get_float(self.trade_data, "commission")

                self.trade_time = from_dict_get_string(self.trade_data, "trade_time")
                self.liquidity_indicator = from_dict_get_string(
                    self.trade_data, "liquidity_indicator"
                )
        except Exception as e:
            _logger.error(f"Error parsing trade data: {e}")
            self.trade_data = {}
        self.has_been_init_data = True
        return self

    def get_all_data(self):
        """get_all_data method"""
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "trade_id": self.trade_id,
                "order_id": self.order_id,
                "product_id": self.product_id,
                "trade_type": self.trade_type,
                "side": self.side,
                "price": self.price,
                "size": self.size,
                "commission": self.commission,
                "trade_time": self.trade_time,
                "liquidity_indicator": self.liquidity_indicator,
            }
        return self.all_data

    def __str__(self):
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self):
        return self.__str__()

    def get_exchange_name(self):
        """get_exchange_name method"""
        return self.exchange_name

    def get_local_update_time(self):
        """get_local_update_time method"""
        return self.local_update_time

    def get_symbol_name(self):
        """get_symbol_name method"""
        return self.symbol_name

    def get_asset_type(self):
        """get_asset_type method"""
        return self.asset_type

    def get_trade_id(self):
        """get_trade_id method"""
        self.init_data()
        return self.trade_id

    def get_order_id(self):
        """get_order_id method"""
        self.init_data()
        return self.order_id

    def get_product_id(self):
        """get_product_id method"""
        self.init_data()
        return self.product_id

    def get_trade_type(self):
        """get_trade_type method"""
        self.init_data()
        return self.trade_type

    def get_side(self):
        """get_side method"""
        self.init_data()
        return self.side

    def get_price(self):
        """get_price method"""
        self.init_data()
        return self.price

    def get_size(self):
        """get_size method"""
        self.init_data()
        return self.size

    def get_commission(self):
        """get_commission method"""
        self.init_data()
        return self.commission

    def get_trade_time(self):
        """get_trade_time method"""
        self.init_data()
        return self.trade_time

    def get_liquidity_indicator(self):
        """get_liquidity_indicator method"""
        self.init_data()
        return self.liquidity_indicator


class CoinbaseWssTradeData(CoinbaseTradeData):
    """WebSocket（：trade_identry_id，timetrade_time）"""

    def init_data(self):
        """init_data method"""
        if not self.has_been_json_encoded:
            self.trade_data = json.loads(self.trade_info)
            self.has_been_json_encoded = True
        # Ensure trade_data is a dict
        if isinstance(self.trade_data, str):
            self.trade_data = json.loads(self.trade_data)
        if self.has_been_init_data:
            return self
        try:
            # WebSocket trade data
            if isinstance(self.trade_data, dict):
                self.trade_id = from_dict_get_string(self.trade_data, "trade_id")
                self.order_id = from_dict_get_string(self.trade_data, "order_id")
                self.product_id = from_dict_get_string(self.trade_data, "product_id")
                self.side = from_dict_get_string(self.trade_data, "side")

                self.price = from_dict_get_float(self.trade_data, "price")
                self.size = from_dict_get_float(self.trade_data, "size")
                self.commission = from_dict_get_float(self.trade_data, "commission")

                self.trade_time = from_dict_get_string(self.trade_data, "time")
                self.liquidity_indicator = from_dict_get_string(
                    self.trade_data, "liquidity_indicator"
                )
        except Exception as e:
            _logger.error(f"Error parsing WebSocket trade data: {e}")
            self.trade_data = {}
        self.has_been_init_data = True
        return self


class CoinbaseRequestTradeData(CoinbaseTradeData):
    """REST API（REST API，）"""

    def init_data(self):
        """init_data method"""
        if not self.has_been_json_encoded:
            self.trade_data = json.loads(self.trade_info)
            self.has_been_json_encoded = True
        # Ensure trade_data is a dict
        if isinstance(self.trade_data, str):
            self.trade_data = json.loads(self.trade_data)
        if self.has_been_init_data:
            return self
        try:
            # REST API trade data (from /brokerage/orders/historical/fills)
            if isinstance(self.trade_data, dict):
                self.trade_id = from_dict_get_string(self.trade_data, "entry_id")
                self.order_id = from_dict_get_string(self.trade_data, "order_id")
                self.product_id = from_dict_get_string(self.trade_data, "product_id")
                self.trade_type = from_dict_get_string(self.trade_data, "trade_type")
                self.side = from_dict_get_string(self.trade_data, "side")

                self.price = from_dict_get_float(self.trade_data, "price")
                self.size = from_dict_get_float(self.trade_data, "size")
                self.commission = from_dict_get_float(self.trade_data, "commission")

                self.trade_time = from_dict_get_string(self.trade_data, "trade_time")
                self.liquidity_indicator = from_dict_get_string(
                    self.trade_data, "liquidity_indicator"
                )
        except Exception as e:
            _logger.error(f"Error parsing REST trade data: {e}")
            self.trade_data = {}
        self.has_been_init_data = True
        return self
