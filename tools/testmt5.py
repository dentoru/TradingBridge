from mt5_bridge import open_mt5_trade

open_mt5_trade(
    symbol="XAUUSD",
    volume=0.03,
    action="buy",
    tp=600,
    sl=400
)
