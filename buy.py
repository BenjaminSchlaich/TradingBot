"""Place a $5,000 market buy order for Bitcoin (BTC/USD) using Alpaca‑py.

Usage:
    1. pip install alpaca-py
    2. export ALPACA_API_KEY and ALPACA_SECRET_KEY (paper keys are fine).
    3. python place_btc_order.py

Set PAPER=0 in the environment if you want to send the order to your LIVE account
(instead of the default paper trading endpoint).

Note: Crypto orders support fractional trading and accept a *notional* amount
(USD value) instead of quantity. See Alpaca docs: https://docs.alpaca.markets/docs/crypto-orders
"""

import os
import sys
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import OrderRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce

API_KEY = ("PK7AU5IZPU65QSAUDBW1")
SECRET_KEY = ("sAAuQ1py1XIPb28QI9qlpayScWNO4SrnwUpGu3qe")

if not API_KEY or not SECRET_KEY:
    sys.exit("ERROR: Set ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables first.")

PAPER = os.getenv("PAPER", "1") != "0"  # default True
print(f"Connecting to {'paper' if PAPER else 'live'} trading endpoint …")

client = TradingClient(API_KEY, SECRET_KEY, paper=PAPER)

order = client.submit_order(
    order_data=OrderRequest(
        symbol="AAPL",
        notional=5000,            # USD amount of BTC to buy
        side=OrderSide.BUY,
        type=OrderType.MARKET,
        time_in_force=TimeInForce.DAY,
    )
)

print("Order submitted successfully! →")
print(f"  id:        {order.id}")
print(f"  status:    {order.status}")
print(f"  notional:  {order.notional} USD")
print(f"  filled:    {order.filled_qty} {order.symbol}")
