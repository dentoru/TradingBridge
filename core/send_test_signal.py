import requests
import json

url = "http://127.0.0.1:80/webhook"

# Test payload simulating a TradingView alert
payload = {
    "symbol": "XAUUSD",
    "action": "buy",
    "volume": 0.03,
    "tp": 600,
    "sl": 400,
    "timeframe": "5m"
}

headers = {
    "Content-Type": "application/json"
}

print("📤 Sending test signal to Flask webhook...")
response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    print("✅ Signal delivered successfully!")
else:
    print(f"❌ Failed to deliver signal: HTTP {response.status_code}")
