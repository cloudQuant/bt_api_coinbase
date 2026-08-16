"""Module-level docstring."""
from __future__ import annotations

from bt_api_coinbase.exchange_registers import register_coinbase


class TestRegisterCoinbase:
    """Class TestRegisterCoinbase"""
    def test_module_imports(self):
        """test_module_imports method"""
        assert register_coinbase is not None
