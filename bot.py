from flask import Flask, request, jsonify
from pybit.unified_trading import HTTP
import os
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Bybit testnet session
session = HTTP(
    testnet=True,
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET"),
)

@app.route("/", methods=["GET"])
def home():
    return "bot is live", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True, silent=False)
        logging.info(f"Received signal: {data}")

        if not data:
            return jsonify({"ok": False, "error": "Empty JSON"}), 400

        signal = str(data.get("signal", "")).lower().strip()
        symbol = str(data.get("symbol", "BTCUSDT")).upper().strip()

        if signal not in ["buy", "sell"]:
            return jsonify({"ok": False, "error": "signal must be buy or sell"}), 400

        side = "Buy" if signal == "buy" else "Sell"

        # Bybit V5 place order
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty="0.001"
        )

        logging.info(f"Order placed: {order}")
        return jsonify({"ok": True, "order": order}), 200

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
