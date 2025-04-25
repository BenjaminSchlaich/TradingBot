"""Real‑time Alpaca portfolio value chart

Requirements:
    pip install alpaca-py matplotlib
    Export your keys:
        export ALPACA_API_KEY="<key>"
        export ALPACA_SECRET_KEY="<secret>"

Run the script and a Tkinter window will open, fetching and
plotting account.portfolio_value once per second.
Note: In paper trading the value updates roughly once a minute, so
the graph may show flat segments between account updates.
"""

import os
import datetime as dt
import tkinter as tk
from collections import deque

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from alpaca.trading.client import TradingClient

# --- Alpaca authentication -------------------------------------------------
# put your keys in env vars or replace directly (not recommended to commit!)
API_KEY = ("PK7AU5IZPU65QSAUDBW1")
SECRET_KEY = ("sAAuQ1py1XIPb28QI9qlpayScWNO4SrnwUpGu3qe")

if not (API_KEY and SECRET_KEY):
    raise RuntimeError("Please set ALPACA_API_KEY and ALPACA_SECRET_KEY env vars")

# paper=True uses the paper endpoint; set False for live trading
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

# --- Plot configuration ----------------------------------------------------
UPDATE_MS = 1000       # update interval in milliseconds (≈ 1 second)
MAX_POINTS = 3600      # keep last hour of data to avoid memory bloat

# Deques automatically discard old points when maxlen is reached
_times: deque[dt.datetime] = deque(maxlen=MAX_POINTS)
_values: deque[float] = deque(maxlen=MAX_POINTS)

# --- Tkinter window + matplotlib figure ------------------------------------
root = tk.Tk()
root.title("Alpaca Portfolio Value – Real‑Time")

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlabel("Time (local)")
ax.set_ylabel("Portfolio Value ($)")
ax.set_title("Real‑Time Portfolio Equity")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- Data fetch + refresh loop --------------------------------------------

def fetch_portfolio_value() -> float:
    """Return current portfolio (equity) value as float."""
    account = trading_client.get_account()  # REST call each iteration
    return float(account.portfolio_value)   # property documented in Alpaca API

def update_chart():
    """Fetch latest value, update line chart, and reschedule."""
    now = dt.datetime.now()
    try:
        value = fetch_portfolio_value()
    except Exception as exc:
        print("API error:", exc)
        # keep previous value so the line doesn’t break
        value = _values[-1] if _values else 0.0

    _times.append(now)
    _values.append(value)

    # Update line data and rescale axes
    line.set_data(_times, _values)
    ax.relim()
    ax.autoscale_view()

    canvas.draw_idle()
    root.after(UPDATE_MS, update_chart)

# Kick off the loop and start the main‑loop
update_chart()
root.mainloop()
