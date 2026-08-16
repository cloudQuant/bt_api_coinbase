"""
Coinbase 
 Coinbase Spot  feed 、 ExchangeRegistry

"""

from __future__ import annotations

from bt_api_base.balance_utils import simple_balance_handler as _coinbase_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_coinbase.containers.exchanges.coinbase_exchange_data import (
    CoinbaseExchangeDataSpot,
)
from bt_api_coinbase.feeds.live_coinbase.spot import (
    CoinbaseRequestDataSpot,
)


def register_coinbase() -> None:
    """ Coinbase Spot  ExchangeRegistry"""
    # Spot
    ExchangeRegistry.register_feed("COINBASE___SPOT", CoinbaseRequestDataSpot)
    ExchangeRegistry.register_exchange_data("COINBASE___SPOT", CoinbaseExchangeDataSpot)
    ExchangeRegistry.register_balance_handler("COINBASE___SPOT", _coinbase_balance_handler)


# 
register_coinbase()
