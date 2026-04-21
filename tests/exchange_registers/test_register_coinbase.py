from __future__ import annotations

from bt_api_coinbase.exchange_registers import register_coinbase


class TestRegisterCoinbase:
    def test_module_imports(self):
        assert register_coinbase is not None
