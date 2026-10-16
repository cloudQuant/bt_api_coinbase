"""Module-level docstring."""
# generated, verify register call

from __future__ import annotations

from typing import TYPE_CHECKING

from bt_api_base.plugins.protocol import PluginInfo

from bt_api_coinbase.exchange_registers.register_coinbase import register_coinbase

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry


def register_plugin(registry: ExchangeRegistry) -> PluginInfo:
    """register_plugin function"""
    register_coinbase(registry)

    return PluginInfo(
        name="bt_api_coinbase",
        version="0.1.0",
        core_requires=">=0.15,<1.0",
        supported_exchanges=("COINBASE___SPOT",),
        supported_asset_types=("SPOT",),
    )
