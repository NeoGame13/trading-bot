from flask import Flask, request
import os
from pybit.unified_trading import HTTP

app = Flask(__name__)

api_key = os.environ.get("BYBIT_API_KEY")
api_secret = os.environ.get("BYBIT_API_SECRET")

session = HTTP(
    testnet=True,
    api_key=api_key,
    api_secret=api_secret
)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received signal:", data)

    signal = data.get("signal")
    symbol = data.get("symbol", "BTCUSDT")

    side = "Buy" if signal == "buy" else "Sell"

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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
