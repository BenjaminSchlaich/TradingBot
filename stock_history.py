"""
Simple Tkinter GUI to fetch and plot the last 5 years of S&P 500 price history
(using the SPY ETF) with Alpaca-py and matplotlib.

Requirements:
    pip install alpaca-py pandas matplotlib
    Set environment variables ALPACA_API_KEY and ALPACA_SECRET_KEY.
"""

import os
from datetime import datetime, timedelta
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

# --- Alpaca authentication --------------------------------------------------
# put your keys in env vars or replace directly (not recommended to commit!)
API_KEY = ("PK7AU5IZPU65QSAUDBW1")
SECRET_KEY = ("sAAuQ1py1XIPb28QI9qlpayScWNO4SrnwUpGu3qe")

data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

# --- Fetch last 5 years of daily data for the SPY ETF -----------------------
end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=5 * 365)

request_params = StockBarsRequest(
    symbol_or_symbols="SPY",        # S&P 500 tracking ETF
    timeframe=TimeFrame.Day,
    start=start_date,
    end=end_date,
    adjustment="split",            # adjust for splits; drop to get raw prices
)

bars = data_client.get_stock_bars(request_params).df
bars = bars.reset_index()  # move timestamp out of the index for plotting

# --- Build a simple Tkinter GUI with the chart ------------------------------
root = tk.Tk()
root.title("S&P 500 — Last 5 Years (SPY)")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(bars["timestamp"], bars["close"], linewidth=1)
ax.set_title("S&P 500 (SPY) Daily Close — Last 5 Years")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.grid(True)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()
