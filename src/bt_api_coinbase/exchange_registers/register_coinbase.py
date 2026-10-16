"""
Coinbase
 Coinbase Spot  feed 、 ExchangeRegistry

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from bt_api_base.balance_utils import simple_balance_handler as _coinbase_balance_handler

from bt_api_coinbase.containers.exchanges.coinbase_exchange_data import (
    CoinbaseExchangeDataSpot,
)
from bt_api_coinbase.feeds.live_coinbase.spot import (
    CoinbaseRequestDataSpot,
)

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry


def register_coinbase(registry: ExchangeRegistry) -> None:
    """Register Coinbase Spot on the loader's isolated registry."""
    # Spot
    registry.register_feed("COINBASE___SPOT", CoinbaseRequestDataSpot)
    registry.register_exchange_data("COINBASE___SPOT", CoinbaseExchangeDataSpot)
    registry.register_balance_handler("COINBASE___SPOT", _coinbase_balance_handler)
