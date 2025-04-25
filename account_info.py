# pip install alpaca-py
import os
from alpaca.trading.client import TradingClient

# put your keys in env vars or replace directly (not recommended to commit!)
API_KEY = ("PK7AU5IZPU65QSAUDBW1")
SECRET_KEY = ("sAAuQ1py1XIPb28QI9qlpayScWNO4SrnwUpGu3qe")

# paper=True ⇒ connects to the paper-trading endpoint. Omit or set False for live.
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

account = trading_client.get_account()
print("Account ID:", account.id)
print("Status:", account.status)   # e.g. 'ACTIVE', 'ACCOUNT_UPDATED'
print("Cash balance ($):", account.cash)           # liquid cash in the account
print("Equity/portfolio ($):", account.portfolio_value)  # cash + positions
