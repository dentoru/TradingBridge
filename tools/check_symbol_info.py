import MetaTrader5 as mt5

mt5.initialize()

symbol = "XAUUSD"
info = mt5.symbol_info(symbol)
if info:
    print(f"✅ {symbol} info:")
    print(f"Min lot: {info.volume_min}")
    print(f"Max lot: {info.volume_max}")
    print(f"Lot step: {info.volume_step}")
else:
    print("❌ Symbol info not found.")

mt5.shutdown()
