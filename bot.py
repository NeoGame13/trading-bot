from flask import Flask, request
from pybit.unified_trading import HTTP
import os

app = Flask(__name__)

# підключення до Bybit
session = HTTP(
    testnet=True,  # DEMO
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET")
)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received signal:", data)

    side = "Buy" if data["signal"] == "buy" else "Sell"
    symbol = data["symbol"]

    try:
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty="0.001"
        )
        print("Order placed:", order)
    except Exception as e:
        print("Error:", e)

    return "ok", 200

if __name__ == "__main__":
    app.run(port=10000)
