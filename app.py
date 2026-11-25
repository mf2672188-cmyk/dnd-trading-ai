"""
dnd-trading-ai: a simple starter web app for Render.

This is a DEMO. It uses fake (simulated) prices and does NOT place any trades.
It shows the basic idea of a trading signal: a moving average crossover.
"""

import random
from flask import Flask, jsonify

app = Flask(__name__)


def fake_prices(count=60):
    """Make a list of fake prices that wander up and down (a random walk)."""
    price = 1.1000  # pretend EUR/USD
    prices = []
    for _ in range(count):
        price += random.uniform(-0.0010, 0.0010)
        prices.append(round(price, 5))
    return prices


def moving_average(values, length):
    """Average of the last `length` values."""
    return sum(values[-length:]) / length


def get_signal(prices):
    """
    Moving average crossover:
    - fast average above slow average -> BUY
    - fast average below slow average -> SELL
    """
    fast = moving_average(prices, 5)
    slow = moving_average(prices, 20)
    if fast > slow:
        signal = "BUY"
    elif fast < slow:
        signal = "SELL"
    else:
        signal = "HOLD"
    return signal, round(fast, 5), round(slow, 5)


@app.route("/")
def home():
    prices = fake_prices()
    signal, fast, slow = get_signal(prices)
    return f"""
    <html>
      <head><title>dnd-trading-ai</title></head>
      <body style="font-family: Arial; max-width: 600px; margin: 40px auto;">
        <h1>dnd-trading-ai</h1>
        <p><b>Demo only.</b> Prices are simulated and no trades are placed.</p>
        <p>Latest price: <b>{prices[-1]}</b></p>
        <p>Fast average (5): {fast}<br>Slow average (20): {slow}</p>
        <h2>Signal: {signal}</h2>
        <p>Refresh the page to generate new fake prices.</p>
        <p>JSON version: <a href="/api/signal">/api/signal</a></p>
      </body>
    </html>
    """


@app.route("/api/signal")
def api_signal():
    prices = fake_prices()
    signal, fast, slow = get_signal(prices)
    return jsonify(
        {
            "latest_price": prices[-1],
            "fast_average": fast,
            "slow_average": slow,
            "signal": signal,
            "note": "Simulated data. Not financial advice.",
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # Only used when running on your own computer. Render uses gunicorn.
    app.run(host="0.0.0.0", port=5000)
