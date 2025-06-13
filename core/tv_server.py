from flask import Flask, request
import json
import os
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# Define full path to signal file
signal_file_path = "C:\\TradingBridge\\tv_signal.txt"

# Define route to receive TradingView alerts
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)  # ✅ FIXED HERE

        if not data:
            print("❌ No JSON data received")
            return 'Invalid or missing JSON', 400

        # Save data to file
        with open(signal_file_path, "w") as f:
            json.dump(data, f)

        # Log the webhook data
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📩 Webhook received:")
        print(json.dumps(data, indent=2))

        return '', 200

    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return 'Internal Server Error', 500

# Run Flask app on port 80
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
