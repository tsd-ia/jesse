import os
import sys
import sqlite3
import numpy as np
import traceback

# --- ENTORNO JESSE ---
sys.path.insert(0, os.getcwd())
import jesse.helpers as jh
jh.is_unit_testing = lambda: False # Garantizar carga de estrategias local

from jesse.modes import backtest_mode
from jesse.config import config, set_config
from jesse.routes import router
from jesse.store import store
import jesse.services.exchange_service as exchange_service

def run_pure_audit(strategy_name, timeframe):
    print(f"\nAUDIT: {strategy_name} ({timeframe})")
    store.reset()
    user_config = {
        'warm_up_candles': 240,
        'exchanges': {
            'Binance Perpetual Futures': {
                'name': 'Binance Perpetual Futures',
                'fee': 0.0004,
                'type': 'futures',
                'futures_leverage': 50,
                'balance': 10000
            }
        },
        'logging': {'balance_update': False, 'order_execution': False}
    }
    
    try:
        set_config(user_config)
        config['app']['trading_mode'] = 'backtest'
        exchange, symbol = 'Binance Perpetual Futures', 'PAXG-USDT'
        
        # Cargar RUTAS
        router.initiate([{'exchange': exchange, 'symbol': symbol, 'timeframe': timeframe, 'strategy': strategy_name}], [])
        
        # Cargar velas manual de la DB
        start_ts = jh.date_to_timestamp('2026-02-15')
        finish_ts = jh.date_to_timestamp('2026-03-14')
        conn = sqlite3.connect('jesse_db.sqlite')
        c = conn.cursor()
        c.execute("SELECT timestamp, open, close, high, low, volume FROM Candle WHERE symbol='PAXG-USDT' AND timestamp >= ? AND timestamp <= ?", (start_ts, finish_ts))
        rows = c.fetchall()
        conn.close()
        
        if not rows: 
            print("No se encontraron velas en la DB.")
            return 0, 0
        
        candles = np.array([[float(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5])] for r in rows])
        
        # Inyectar en el store
        store.candles.init_storage(len(candles) + 1000)
        key = jh.key(exchange, symbol)
        
        # Dividir en warmup y trading
        warmup = candles[:240]
        trading = candles[240:]
        
        print(f"Buscando beneficios en {len(trading)} velas...")
        
        # Simular warmup
        for can in warmup:
            store.candles.add_candle(can, exchange, symbol, '1m')
            
        # Simular trading
        # El simulator de jesse hace el loop interno de 1m
        result = backtest_mode.simulator({key: {'exchange': exchange, 'symbol': symbol, 'candles': trading}}, run_silently=True)
        
        m = result['metrics'] if result else None
        profit = m.get('net_profit_percentage', 0) if m else 0
        trades = m.get('total_closed_trades', 0) if m else 0
        
        print(f"RES: {profit:.2f}% ROI | {trades} trades")
        return profit, trades
    except Exception:
        traceback.print_exc()
        return 0, 0

# --- AUDITORIA FINAL 2026 ---
rank = []
scenarios = [
    ('Antigravity_Beast', '15m'),
    ('Titan_Oro', '1h'),
    ('Gold_Terminator', '1m')
]

for s, tf in scenarios:
    p, t = run_pure_audit(s, tf)
    rank.append({'name': s, 'profit': p, 'trades': t, 'tf': tf})

rank.sort(key=lambda x: x['profit'], reverse=True)
print("\n" + "!"*50)
print(" RESULTADOS AUDITORIA ORO 2026 ")
print("!"*50)
for r in rank:
    print(f"{r['name']} ({r['tf']}): {r['profit']:.2f}% ROI | {r['trades']} trades")
print("!"*50)
