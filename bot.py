from flask import Flask, request, jsonify
from pybit.unified_trading import HTTP
import os
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

session = HTTP(
    testnet=True,
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET"),
)

@app.route("/")
def home():
    return "bot is live", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        logging.info(f"Received signal: {data}")

        signal = data.get("signal")
        symbol = data.get("symbol", "BTCUSDT")

        side = "Buy" if signal == "buy" else "Sell"

        # 🔥 ставимо плече
        try:
            session.set_leverage(
                category="linear",
                symbol=symbol,
                buyLeverage="10",
                sellLeverage="10"
            )
        except:
            pass

        # 🔥 дуже маленький обʼєм щоб точно пройшло
        qty = "0.00005"

        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=qty,
            takeProfit="70000",   # зміню потім під тебе
            stopLoss="60000"
        )

        logging.info(f"Order placed: {order}")

        return jsonify({"ok": True, "order": order})

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
