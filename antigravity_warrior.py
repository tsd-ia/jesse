import os
import sys
import sqlite3
import time
import numpy as np
import traceback

# --- AMBIENTE JESSE ---
sys.path.insert(0, os.getcwd())

import jesse.helpers as jh
from jesse.modes import backtest_mode
from jesse.config import config, set_config
from jesse.routes import router
from jesse.store import store
import jesse.services.exchange_service as exchange_service
import jesse.services.order_service as order_service
import jesse.services.position_service as position_service
from jesse.services.validators import validate_routes

jh.is_unit_testing = lambda: False
jh.should_execute_silently = lambda: True

def load_candles_direct(exchange, symbol, start_date, finish_date):
    start_ts = jh.date_to_timestamp(start_date)
    finish_ts = jh.date_to_timestamp(finish_date)
    conn = sqlite3.connect('jesse_db.sqlite')
    cursor = conn.cursor()
    query = "SELECT timestamp, open, high, low, close, volume FROM Candle WHERE exchange=? AND symbol=? AND timeframe='1m' AND timestamp>=? AND timestamp<=? ORDER BY timestamp ASC"
    cursor.execute(query, (exchange, symbol, start_ts, finish_ts))
    rows = cursor.fetchall()
    conn.close()
    if not rows: return [], []
    # Jesse: [timestamp, open, close, high, low, volume]
    candles = np.array([[float(r[0]), float(r[1]), float(r[4]), float(r[2]), float(r[3]), float(r[5])] for r in rows])
    return candles[:240], candles[240:]

def run_test(strategy_name, timeframe='1m', start_date='2026-02-15', finish_date='2026-03-14'):
    print(f"\n>>> AUDIT: {strategy_name} ({timeframe})")
    store.reset()
    user_config = {
        'warm_up_candles': 240,
        'exchanges': {
            'Binance Perpetual Futures': {
                'name': 'Binance Perpetual Futures',
                'fee': 0.0004,
                'type': 'futures',
                'futures_leverage': 50,
                'futures_leverage_mode': 'cross',
                'balance': 10000
            }
        },
        'logging': {'balance_update': False, 'order_execution': False}
    }
    try:
        set_config(user_config)
        config['env']['exchanges']['Binance Perpetual Futures'] = user_config['exchanges']['Binance Perpetual Futures']
        config['app']['trading_mode'] = 'backtest'
        exchange, symbol = 'Binance Perpetual Futures', 'PAXG-USDT'
        
        # IMPORTANTE: Definir rutas correctamente para que Jesse sepa que agregar
        router.initiate([{'exchange': exchange, 'symbol': symbol, 'timeframe': timeframe, 'strategy': strategy_name}], [])
        validate_routes(router)
        
        warmup_arr, trading_arr = load_candles_direct(exchange, symbol, start_date, finish_date)
        if len(trading_arr) == 0: return None
        
        store.candles.init_storage(len(trading_arr) + len(warmup_arr) + 500)
        exchange_service.initialize_exchanges_state()
        order_service.initialize_orders_state()
        position_service.initialize_positions_state()
        
        key = jh.key(exchange, symbol)
        # Jesse simulator SIEMPRE requiere velas de 1m para simular el precio interno 
        # y luego el mismo las agrega segun la ruta.
        if len(warmup_arr) > 0:
            backtest_mode._handle_warmup_candles({key: {'exchange': exchange, 'symbol': symbol, 'candles': warmup_arr}}, start_date)
        
        result = backtest_mode.simulator({key: {'exchange': exchange, 'symbol': symbol, 'candles': trading_arr}}, run_silently=True)
        
        if not result or 'metrics' not in result or result['metrics'] is None:
            return {'name': strategy_name, 'profit': 0, 'trades': 0}
            
        m = result['metrics']
        profit = m.get('net_profit_percentage', 0)
        trades = m.get('total_closed_trades', 0)
        print(f"RES: {profit:.2f}% ROI | {trades} trades")
        return {'name': strategy_name, 'profit': profit, 'trades': trades}
    except Exception:
        traceback.print_exc()
        return None

# --- AUDITORIA FINAL ---
rank = []
audit_list = [
    ('Gold_Terminator', '1m'),
    ('Antigravity_Beast', '15m'),
    ('Titan_Oro', '15m'),
    ('HyperScalp', '1m')
]

for s, tf in audit_list:
    res = run_test(s, tf)
    if res: rank.append(res)

rank.sort(key=lambda x: x['profit'], reverse=True)
print("\n" + "="*50)
print("🏆 RANKING ORO 2026 - AUDITORIA CERTIFICADA 🏆")
print("="*50)
for r in rank:
    print(f"{r['name']}: {r['profit']:.2f}% ROI ({r['trades']} trades)")
print("="*50)
