# bt_api_coinbase

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_coinbase.svg)](https://pypi.org/project/bt_api_coinbase/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_coinbase.svg)](https://pypi.org/project/bt_api_coinbase/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_coinbase/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_coinbase/actions)
[![Docs](https://readthedocs.org/projects/bt-api-coinbase/badge/?version=latest)](https://bt-api-coinbase.readthedocs.io/)

---

<!-- English -->
# bt_api_coinbase

> **Coinbase exchange plugin for bt_api** — Unified REST API for Spot trading via Coinbase Advanced Trade API.

`bt_api_coinbase` is a runtime plugin for [bt_api](https://github.com/cloudQuant/bt_api_py) that connects to **Coinbase** exchange using the **Advanced Trade API v3**. It depends on [bt_api_base](https://github.com/cloudQuant/bt_api_base) for core infrastructure.

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-coinbase.readthedocs.io/ |
| Chinese Docs | https://bt-api-coinbase.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_coinbase |
| PyPI | https://pypi.org/project/bt_api_coinbase/ |
| Issues | https://github.com/cloudQuant/bt_api_coinbase/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://github.com/cloudQuant/bt_api_py |

---

## Features

### Asset Types

| Asset Type | Code | REST | WebSocket | Description |
|---|---|---|---|---|
| Spot | `COINBASE___SPOT` | ✅ | — | Spot trading via Advanced Trade API |

### Dual API Modes

- **REST API** — Synchronous polling for order management, balance queries, historical data
- **WebSocket API** — Real-time streaming (placeholder for future implementation)

### Plugin Architecture

Auto-registers at import time via `ExchangeRegistry`. Works seamlessly with `BtApi`:

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "COINBASE___SPOT": {
        "api_key": "your_api_key",
        "private_key": "your_private_key",
    }
})

ticker = api.get_tick("COINBASE___SPOT", "BTC-USD")
balance = api.get_balance("COINBASE___SPOT")
order = api.make_order(exchange_name="COINBASE___SPOT", symbol="BTC-USD", vol=0.001, price=50000, order_type="buy-limit")
```

### Unified Data Containers

All exchange responses normalized to bt_api_base container types:

- `CoinbaseRequestTickerData` — 24hr rolling ticker
- `CoinbaseRequestOrderBookData` — Order book depth
- `CoinbaseRequestBarData` — K-line/candlestick
- `CoinbaseRequestOrderData` — Order status and fills
- `CoinbaseRequestAccountData` — Account and balance info

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_coinbase
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_coinbase
cd bt_api_coinbase
pip install -e .
```

### Requirements

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `httpx` for HTTP client

---

## Quick Start

### 1. Install

```bash
pip install bt_api_coinbase
```

### 2. Get ticker (public — no API key needed)

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("COINBASE___SPOT", "BTC-USD")
print(f"BTC-USD price: {ticker.last_price}")
```

### 3. Place an order (requires API key)

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "COINBASE___SPOT": {
        "api_key": "your_api_key",
        "private_key": "your_private_key",
    }
})

order = api.make_order(
    exchange_name="COINBASE___SPOT",
    symbol="BTC-USD",
    vol=0.001,
    price=50000,
    order_type="buy-limit",
)
print(f"Order placed: {order}")
```

### 4. Get balance

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "COINBASE___SPOT": {
        "api_key": "your_api_key",
        "private_key": "your_private_key",
    }
})

balance = api.get_balance("COINBASE___SPOT")
print(f"Balance: {balance}")
```

---

## Architecture

```
bt_api_coinbase/
├── src/bt_api_coinbase/
│   ├── __init__.py
│   ├── exchange_registers/
│   │   ├── __init__.py
│   │   └── register_coinbase.py     # Feed/exchange_data registration
│   ├── containers/
│   │   ├── __init__.py
│   │   ├── exchanges/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_exchange_data.py  # CoinbaseExchangeData, CoinbaseExchangeDataSpot
│   │   ├── tickers/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_ticker.py    # CoinbaseRequestTickerData
│   │   ├── orderbooks/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_orderbook.py # CoinbaseRequestOrderBookData
│   │   ├── bars/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_bar.py       # CoinbaseRequestBarData
│   │   ├── orders/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_order.py     # CoinbaseRequestOrderData
│   │   ├── accounts/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_account.py   # CoinbaseRequestAccountData
│   │   ├── balances/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_balance.py   # CoinbaseRequestBalanceData
│   │   └── trades/
│   │       ├── __init__.py
│   │       └── coinbase_trade.py     # CoinbaseRequestTradeData
│   └── feeds/
│       ├── __init__.py
│       └── live_coinbase/
│           ├── __init__.py
│           ├── request_base.py        # CoinbaseRequestData base class
│           └── spot.py               # CoinbaseRequestDataSpot
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

---

## Supported Operations

| Category | Operation | Notes |
|---|---|---|
| **Market Data** | `get_ticker` / `get_tick` | 24hr rolling ticker |
| | `get_orderbook` / `get_depth` | Depth up to 100 levels |
| | `get_kline` / `get_bars` | Intervals: 1m/5m/15m/30m/1h/6h/1d |
| | `get_exchange_info` | Trading rules and symbol info |
| | `get_server_time` | Server time synchronization |
| **Account** | `get_balance` | All asset balances |
| | `get_account` | Full account info |
| **Trading** | `make_order` | LIMIT/MARKET orders (buy/sell) |
| | `cancel_order` | Cancel order by ID |
| | `query_order` | Query order by ID |
| | `get_open_orders` | All open orders |

---

## API Authentication

Coinbase Advanced Trade API uses HMAC SHA256 authentication:

```
message = timestamp + method + request_path + body
signature = Base64(HMAC-SHA256(secret_key, message))
```

Required headers:
- `CB-ACCESS-KEY` — API key
- `CB-ACCESS-SIGN` — Base64 encoded HMAC SHA256 signature
- `CB-ACCESS-TIMESTAMP` — Request timestamp (seconds)

---

## Rate Limits

| Endpoint Type | Limit |
|---|---|
| Public endpoints | 10 requests/second |
| Private endpoints | 15 requests/second |

---

## Supported Symbols

Coinbase uses hyphenated symbols (e.g., `BTC-USD`, `ETH-USD`, `SOL-USD`).

Popular pairs:
- `BTC-USD`, `ETH-USD`, `SOL-USD`, `XRP-USD`
- `BTC-EUR`, `ETH-EUR`, `EUR-USD`
- `GBP-USD`, `ETH-BTC`

---

## Documentation

| Doc | Link |
|-----|------|
| **English** | https://bt-api-coinbase.readthedocs.io/ |
| **中文** | https://bt-api-coinbase.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://cloudquant.github.io/bt_api_py/ |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Support

- [GitHub Issues](https://github.com/cloudQuant/bt_api_coinbase/issues) — bug reports, feature requests
- Email: yunjinqi@gmail.com

---

---

## 中文

> **bt_api 的 Coinbase 交易所插件** — 通过 Coinbase Advanced Trade API 为现货交易提供统一的 REST API。

`bt_api_coinbase` 是 [bt_api](https://github.com/cloudQuant/bt_api_py) 的运行时插件，通过 **Advanced Trade API v3** 连接 **Coinbase** 交易所。依赖 [bt_api_base](https://github.com/cloudQuant/bt_api_base) 提供核心基础设施。

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-coinbase.readthedocs.io/ |
| 中文文档 | https://bt-api-coinbase.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_coinbase |
| PyPI | https://pypi.org/project/bt_api_coinbase/ |
| 问题反馈 | https://github.com/cloudQuant/bt_api_coinbase/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://github.com/cloudQuant/bt_api_py |

---

## 功能特点

### 资产类型

| 资产类型 | 代码 | REST | WebSocket | 说明 |
|---|---|---|---|---|
| 现货 | `COINBASE___SPOT` | ✅ | — | 通过 Advanced Trade API 进行现货交易 |

### 双 API 模式

- **REST API** — 同步轮询：订单管理、余额查询、历史数据
- **WebSocket API** — 实时流（为未来实现预留）

### 插件架构

通过 `ExchangeRegistry` 在导入时自动注册，与 `BtApi` 无缝协作：

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "COINBASE___SPOT": {
        "api_key": "your_api_key",
        "private_key": "your_private_key",
    }
})

ticker = api.get_tick("COINBASE___SPOT", "BTC-USD")
balance = api.get_balance("COINBASE___SPOT")
order = api.make_order(exchange_name="COINBASE___SPOT", symbol="BTC-USD", vol=0.001, price=50000, order_type="buy-limit")
```

### 统一数据容器

所有交易所响应规范化为 bt_api_base 容器类型：

- `CoinbaseRequestTickerData` — 24小时滚动行情
- `CoinbaseRequestOrderBookData` — 订单簿深度
- `CoinbaseRequestBarData` — K线/蜡烛图
- `CoinbaseRequestOrderData` — 订单状态和成交
- `CoinbaseRequestAccountData` — 账户和余额信息

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_coinbase
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_coinbase
cd bt_api_coinbase
pip install -e .
```

### 系统要求

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `httpx` HTTP 客户端

---

## 快速开始

### 1. 安装

```bash
pip install bt_api_coinbase
```

### 2. 获取行情（公开接口，无需 API key）

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("COINBASE___SPOT", "BTC-USD")
print(f"BTC-USD 价格: {ticker.last_price}")
```

### 3. 下单交易（需要 API key）

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "COINBASE___SPOT": {
        "api_key": "your_api_key",
        "private_key": "your_private_key",
    }
})

order = api.make_order(
    exchange_name="COINBASE___SPOT",
    symbol="BTC-USD",
    vol=0.001,
    price=50000,
    order_type="buy-limit",
)
print(f"订单已下单: {order}")
```

### 4. 获取余额

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "COINBASE___SPOT": {
        "api_key": "your_api_key",
        "private_key": "your_private_key",
    }
})

balance = api.get_balance("COINBASE___SPOT")
print(f"余额: {balance}")
```

---

## 架构

```
bt_api_coinbase/
├── src/bt_api_coinbase/
│   ├── __init__.py
│   ├── exchange_registers/
│   │   ├── __init__.py
│   │   └── register_coinbase.py     # Feed/exchange_data 注册
│   ├── containers/
│   │   ├── __init__.py
│   │   ├── exchanges/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_exchange_data.py  # CoinbaseExchangeData, CoinbaseExchangeDataSpot
│   │   ├── tickers/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_ticker.py    # CoinbaseRequestTickerData
│   │   ├── orderbooks/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_orderbook.py # CoinbaseRequestOrderBookData
│   │   ├── bars/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_bar.py       # CoinbaseRequestBarData
│   │   ├── orders/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_order.py     # CoinbaseRequestOrderData
│   │   ├── accounts/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_account.py   # CoinbaseRequestAccountData
│   │   ├── balances/
│   │   │   ├── __init__.py
│   │   │   └── coinbase_balance.py   # CoinbaseRequestBalanceData
│   │   └── trades/
│   │       ├── __init__.py
│   │       └── coinbase_trade.py     # CoinbaseRequestTradeData
│   └── feeds/
│       ├── __init__.py
│       └── live_coinbase/
│           ├── __init__.py
│           ├── request_base.py        # CoinbaseRequestData 基类
│           └── spot.py               # CoinbaseRequestDataSpot
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

---

## 支持的操作

| 类别 | 操作 | 说明 |
|---|---|---|
| **行情数据** | `get_ticker` / `get_tick` | 24小时滚动行情 |
| | `get_orderbook` / `get_depth` | 深度最高100档 |
| | `get_kline` / `get_bars` | 周期: 1m/5m/15m/30m/1h/6h/1d |
| | `get_exchange_info` | 交易规则和交易对信息 |
| | `get_server_time` | 服务器时间同步 |
| **账户** | `get_balance` | 所有资产余额 |
| | `get_account` | 完整账户信息 |
| **交易** | `make_order` | 限价/市价订单（买入/卖出） |
| | `cancel_order` | 按ID撤销订单 |
| | `query_order` | 按ID查询订单 |
| | `get_open_orders` | 所有挂单 |

---

## API 认证

Coinbase Advanced Trade API 使用 HMAC SHA256 认证：

```
message = timestamp + method + request_path + body
signature = Base64(HMAC-SHA256(secret_key, message))
```

必需请求头：
- `CB-ACCESS-KEY` — API 密钥
- `CB-ACCESS-SIGN` — Base64 编码的 HMAC SHA256 签名
- `CB-ACCESS-TIMESTAMP` — 请求时间戳（秒）

---

## 限流配置

| 端点类型 | 限制 |
|---|---|
| 公开接口 | 10 次/秒 |
| 私有接口 | 15 次/秒 |

---

## 支持的交易对

Coinbase 使用连字符格式的交易对（例如 `BTC-USD`、`ETH-USD`、`SOL-USD`）。

热门交易对：
- `BTC-USD`, `ETH-USD`, `SOL-USD`, `XRP-USD`
- `BTC-EUR`, `ETH-EUR`, `EUR-USD`
- `GBP-USD`, `ETH-BTC`

---

## 文档

| 文档 | 链接 |
|-----|------|
| **英文文档** | https://bt-api-coinbase.readthedocs.io/ |
| **中文文档** | https://bt-api-coinbase.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://cloudquant.github.io/bt_api_py/ |

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

## 技术支持

- [GitHub Issues](https://github.com/cloudQuant/bt_api_coinbase/issues) — bug 报告、功能请求
- 邮箱: yunjinqi@gmail.com