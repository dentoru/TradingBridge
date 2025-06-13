from flask import Flask, request
import json
import os
from datetime import datetime
from core.mt5_bridge import open_mt5_trade

# Create Flask app
app = Flask(__name__)

# Route to accept POST requests from TradingView
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Parse and validate JSON
        data = request.get_json(force=True)
        if not data:
            print("❌ No data received.")
            return 'Invalid JSON', 400

        # Get timeframe (default fallback)
        tf = data.get("timeframe", "unknown").lower()

        # Map timeframe to filename
        file_map = {
            "5m": "tv_signal_5m.txt",
            "30m": "tv_signal_30m.txt",
            "1h": "tv_signal_1h.txt"
        }
        file_name = file_map.get(tf, f"tv_signal_{tf}.txt")
        file_path = os.path.join("data", file_name)

        # Save JSON to file
        with open(file_path, "w") as f:
            json.dump(data, f)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Webhook for {tf} saved to {file_path}")
        print(json.dumps(data, indent=2))

        # Send order to MetaTrader 5
        open_mt5_trade(
            symbol=data["symbol"],
            volume=float(data["volume"]),
            action=data["action"],
            tp=float(data["tp"]),
            sl=float(data["sl"])
        )

        return '', 200

    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return 'Server Error', 500

# Run the app on port 80
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
