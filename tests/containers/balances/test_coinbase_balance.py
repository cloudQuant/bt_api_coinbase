"""Module-level docstring."""
from __future__ import annotations

from bt_api_coinbase.containers.balances import (
    CoinbaseBalanceData,
    CoinbaseRequestBalanceData,
    CoinbaseWssBalanceData,
)


class TestCoinbaseBalanceData:
    """Class TestCoinbaseBalanceData"""
    def test_init(self):
        """test_init method"""
        balance = CoinbaseBalanceData({}, asset_type="SPOT")

        assert balance.exchange_name == "COINBASE"
        assert balance.asset_type == "SPOT"
        assert balance.has_been_init_data is False

    def test_init_data(self):
        """test_init_data method"""
        data = {
            "currency": "BTC",
            "available_balance": {"value": "1.5"},
            "hold": {"value": "0.5"},
            "total": {"value": "2.0"},
        }
        balance = CoinbaseBalanceData(data, asset_type="SPOT", has_been_json_encoded=True)
        balance.init_data()

        assert balance.currency == "BTC"
        assert balance.available == 1.5
        assert balance.hold == 0.5
        assert balance.total == 2.0

    def test_init_data_simple_format(self):
        """test_init_data_simple_format method"""
        data = {
            "currency": "BTC",
            "available": "1.5",
            "hold": "0.5",
            "total": "2.0",
        }
        balance = CoinbaseBalanceData(data, asset_type="SPOT", has_been_json_encoded=True)
        balance.init_data()

        assert balance.currency == "BTC"
        assert balance.available == 1.5

    def test_get_exchange_name(self):
        """test_get_exchange_name method"""
        balance = CoinbaseBalanceData({}, asset_type="SPOT")
        assert balance.get_exchange_name() == "COINBASE"

    def test_get_asset_type(self):
        """test_get_asset_type method"""
        balance = CoinbaseBalanceData({}, asset_type="SPOT")
        assert balance.get_asset_type() == "SPOT"

    def test_get_currency(self):
        """test_get_currency method"""
        data = {"currency": "BTC"}
        balance = CoinbaseBalanceData(data, asset_type="SPOT", has_been_json_encoded=True)

        assert balance.get_currency() == "BTC"

    def test_get_available(self):
        """test_get_available method"""
        data = {"currency": "BTC", "available": "1.5"}
        balance = CoinbaseBalanceData(data, asset_type="SPOT", has_been_json_encoded=True)

        assert balance.get_available() == 1.5

    def test_get_all_data(self):
        """test_get_all_data method"""
        data = {"currency": "BTC", "available": "1.5"}
        balance = CoinbaseBalanceData(data, asset_type="SPOT", has_been_json_encoded=True)
        result = balance.get_all_data()

        assert result["exchange_name"] == "COINBASE"
        assert result["currency"] == "BTC"

    def test_str_representation(self):
        """test_str_representation method"""
        data = {"currency": "BTC"}
        balance = CoinbaseBalanceData(data, asset_type="SPOT", has_been_json_encoded=True)
        result = str(balance)

        assert "COINBASE" in result
        assert "BTC" in result


class TestCoinbaseWssBalanceData:
    """Class TestCoinbaseWssBalanceData"""
    def test_init_data(self):
        """test_init_data method"""
        data = {
            "currency": "BTC",
            "available": "1.5",
            "hold": "0.5",
            "total": "2.0",
        }
        balance = CoinbaseWssBalanceData(data, asset_type="SPOT", has_been_json_encoded=True)
        balance.init_data()

        assert balance.currency == "BTC"
        assert balance.available == 1.5


class TestCoinbaseRequestBalanceData:
    """Class TestCoinbaseRequestBalanceData"""
    def test_init_data(self):
        """test_init_data method"""
        data = {
            "currency": "BTC",
            "available": "1.5",
            "hold": "0.5",
            "total": "2.0",
        }
        balance = CoinbaseRequestBalanceData(data, asset_type="SPOT", has_been_json_encoded=True)
        balance.init_data()

        assert balance.currency == "BTC"
        assert balance.available == 1.5
