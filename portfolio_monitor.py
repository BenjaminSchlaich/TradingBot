'''Real‑time Alpaca portfolio value chart – last 5 minutes

Requirements:
    pip install alpaca-py matplotlib
    export ALPACA_API_KEY and ALPACA_SECRET_KEY
'''

import os
import datetime as dt
import tkinter as tk

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from alpaca.trading.client import TradingClient
# put your keys in env vars or replace directly (not recommended to commit!)
API_KEY = ("PK7AU5IZPU65QSAUDBW1")
SECRET_KEY = ("sAAuQ1py1XIPb28QI9qlpayScWNO4SrnwUpGu3qe")

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

root = tk.Tk()
root.title("Alpaca Portfolio Value – Last 5 Minutes")

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill="both", expand=True)

_times = []  # store timestamps
_values = []  # store portfolio values
WINDOW = dt.timedelta(minutes=5)


def fetch_and_plot() -> None:
    """Fetch the latest portfolio value and refresh the chart."""
    account = trading_client.get_account()
    now = dt.datetime.utcnow()

    _times.append(now)
    _values.append(float(account.portfolio_value))

    # Keep only data within the last 5 minutes
    cutoff = now - WINDOW
    while _times and _times[0] < cutoff:
        _times.pop(0)
        _values.pop(0)

    # Update plot
    ax.clear()
    ax.plot(_times, _values)
    ax.set_xlim(cutoff, now)
    ax.set_title("Portfolio Value (last 5 minutes)")
    ax.set_xlabel("UTC Time")
    ax.set_ylabel("Value ($)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()
    canvas.draw()

    root.after(1000, fetch_and_plot)  # refresh every second

root.after(0, fetch_and_plot)
root.mainloop()
