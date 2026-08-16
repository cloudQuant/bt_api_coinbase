"""
Coinbase kline (bar) data container.
"""

from __future__ import annotations

import json
import time

from bt_api_base.containers.bars.bar import BarData
from bt_api_base.functions.utils import from_dict_get_float
from bt_api_base.logging_factory import get_logger

logger = get_logger("container")


class CoinbaseBarData(BarData):
    """Base class for Coinbase kline/bar data."""

    def __init__(self, bar_info, symbol_name, asset_type, has_been_json_encoded=False):
        """__init__ method"""
        super().__init__(bar_info, has_been_json_encoded)
        self.exchange_name = "COINBASE"
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.bar_data = bar_info if has_been_json_encoded else None
        self.bar_symbol_name = None
        self.server_time = None
        self.local_update_time = time.time()
        self.period = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.volume = None
        self.turnover = None
        self.all_data = None
        self.has_been_init_data = False

    def init_data(self):
        """init_data method"""
        raise NotImplementedError("Subclasses must implement init_data")

    def get_all_data(self):
        """get_all_data method"""
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "bar_symbol_name": self.bar_symbol_name,
                "server_time": self.server_time,
                "period": self.period,
                "open": self.open,
                "high": self.high,
                "low": self.low,
                "close": self.close,
                "volume": self.volume,
                "turnover": self.turnover,
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

    def get_symbol_name(self):
        """get_symbol_name method"""
        return self.symbol_name

    def get_asset_type(self):
        """get_asset_type method"""
        return self.asset_type

    def get_bar_symbol_name(self):
        """get_bar_symbol_name method"""
        return self.bar_symbol_name

    def get_server_time(self):
        """get_server_time method"""
        return self.server_time

    def get_period(self):
        """get_period method"""
        return self.period

    def get_open(self):
        """get_open method"""
        return self.open

    def get_high(self):
        """get_high method"""
        return self.high

    def get_low(self):
        """get_low method"""
        return self.low

    def get_close(self):
        """get_close method"""
        return self.close

    def get_volume(self):
        """get_volume method"""
        return self.volume

    def get_turnover(self):
        """get_turnover method"""
        return self.turnover

    def get_local_update_time(self):
        """get_local_update_time method"""
        return self.local_update_time

    def get_open_price(self):
        """get_open_price method"""
        return self.open

    def get_high_price(self):
        """get_high_price method"""
        return self.high

    def get_low_price(self):
        """get_low_price method"""
        return self.low

    def get_close_price(self):
        """get_close_price method"""
        return self.close


class CoinbaseRequestBarData(CoinbaseBarData):
    """Coinbase REST API kline data.

    API response format for GET /brokerage/products/{product_id}/candles:
    {
        "candles": [
            {
                "start": "1688671800",
                "low": "49500",
                "high": "50500",
                "open": "50000",
                "close": "50200",
                "volume": "1000"
            }
        ]
    }
    """

    def init_data(self):
        """init_data method"""
        if not self.has_been_json_encoded:
            self.bar_data = json.loads(self.bar_info)
            self.has_been_json_encoded = True
        if isinstance(self.bar_data, str):
            self.bar_data = json.loads(self.bar_data)
        if self.has_been_init_data:
            return self
        try:
            if isinstance(self.bar_data, dict):
                self.server_time = from_dict_get_float(self.bar_data, "start")
                self.open = from_dict_get_float(self.bar_data, "open")
                self.high = from_dict_get_float(self.bar_data, "high")
                self.low = from_dict_get_float(self.bar_data, "low")
                self.close = from_dict_get_float(self.bar_data, "close")
                self.volume = from_dict_get_float(self.bar_data, "volume")
            elif isinstance(self.bar_data, (list, tuple)) and len(self.bar_data) >= 6:
                self.server_time = float(self.bar_data[0])
                self.open = float(self.bar_data[1])
                self.high = float(self.bar_data[2])
                self.low = float(self.bar_data[3])
                self.close = float(self.bar_data[4])
                self.volume = float(self.bar_data[5])
        except Exception as e:
            logger.error(f"Error parsing bar data: {e}", exc_info=True)

            self.bar_data = {}
        self.has_been_init_data = True
        return self
