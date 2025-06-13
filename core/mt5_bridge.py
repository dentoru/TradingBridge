import MetaTrader5 as mt5

def open_mt5_trade(symbol, volume, action, tp, sl):
    print("📤 Sending trade to MT5...")

    if not mt5.initialize():
        print("❌ Failed to initialize MT5:", mt5.last_error())
        return

    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"❌ Symbol info not found: {symbol}")
        mt5.shutdown()
        return

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"❌ Failed to select symbol: {symbol}")
            mt5.shutdown()
            return

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"❌ Could not get price for {symbol}")
        mt5.shutdown()
        return

    point = symbol_info.point
    price = tick.ask if action == "buy" else tick.bid

    tp_price = price + tp * point if action == "buy" else price - tp * point
    sl_price = price - sl * point if action == "buy" else price + sl * point

    # ✅ Enforce broker's minimum TP/SL distance
    min_distance_points = symbol_info.trade_stops_level
    min_distance_price = min_distance_points * point

    if abs(tp_price - price) < min_distance_price or abs(sl_price - price) < min_distance_price:
        print(f"❌ TP/SL too close to price. Min required: {min_distance_points} points.")
        mt5.shutdown()
        return

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": round(volume, 2),
        "type": mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": 20,
        "magic": 123456,
        "comment": f"TV Signal {action.upper()}",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    mt5.shutdown()

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Order send failed: {result.retcode} — {result.comment if hasattr(result, 'comment') else ''}")
        return

    print(f"✅ MT5 Trade Executed: {action.upper()} {symbol} {volume} lots @ {price}")
    print(f"    TP: {tp_price} | SL: {sl_price}")
