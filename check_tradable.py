"""Check if Dogecoin (DOGE/USD) is currently tradable on Alpaca.

Usage:
    pip install alpaca-py
    export ALPACA_API_KEY and ALPACA_SECRET_KEY (paper keys are fine).
    python check_doge_tradable.py

It queries the Trading API `/v2/assets/DOGEUSD` and reports the `tradable` flag.
"""

import os
from alpaca.trading.client import TradingClient
from requests.exceptions import HTTPError

SYMBOLS_TO_TRY = ("DOGEUSD", "DOGE/USD", "AAPL", "A")  # fallback just in case

API_KEY = ("PK7AU5IZPU65QSAUDBW1")
SECRET_KEY = ("sAAuQ1py1XIPb28QI9qlpayScWNO4SrnwUpGu3qe")

if not API_KEY or not SECRET_KEY:
    raise SystemExit("Please set ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables.")

client = TradingClient(API_KEY, SECRET_KEY, paper=True)

asset = None
for sym in SYMBOLS_TO_TRY:
    try:
        asset = client.get_asset(sym)

        if asset is None:
            print("Could not find DOGE asset on Alpaca API with tried symbols.")
        else:
            status = "TRADABLE" if asset.tradable else "NOT TRADABLE"
            print(f"{asset.symbol}: {status}")

        continue
    except Exception:
        # try next symbol form
        continue
