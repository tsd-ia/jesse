import os
import sys
import traceback
import sqlite3

# --- DIAGNOSTICO ---
print(f"CWD: {os.getcwd()}")
print(f"DB Exists: {os.path.exists('jesse_db.sqlite')}")

# --- AMBIENTE JESSE ---
sys.path.insert(0, os.getcwd())

import jesse.helpers as jh
jh.is_unit_testing = lambda: False
jh.should_execute_silently = lambda: True

from jesse.modes import backtest_mode
from jesse.config import config, set_config
from jesse.routes import router
from jesse.store import store
import jesse.services.exchange_service as exchange_service
import jesse.services.order_service as order_service
import jesse.services.position_service as position_service
from jesse.services.validators import validate_routes

def run_test(strategy_name, start_date='2026-02-15', finish_date='2026-03-14'):
    print(f"\n>>> TEST DIAGNOSTICO: {strategy_name}")
    
    user_config = {
        'warm_up_candles': 210,
        'exchanges': {
            'Binance Perpetual Futures': {
                'name': 'Binance Perpetual Futures',
                'fee': 0.0004,
                'type': 'futures',
                'futures_leverage': 50,
                'futures_leverage_mode': 'cross',
                'balance': 10000
            }
        }
    }

    try:
        set_config(user_config)
        config['env']['exchanges']['Binance Perpetual Futures'] = user_config['exchanges']['Binance Perpetual Futures']
        
        r = router
        r.routes = []
        routes = [{'exchange': 'Binance Perpetual Futures', 'symbol': 'PAXG-USDT', 'timeframe': '1m', 'strategy': strategy_name}]
        data_routes = [{'exchange': 'Binance Perpetual Futures', 'symbol': 'PAXG-USDT', 'timeframe': '1m'}]
        
        r.initiate(routes, data_routes)
        store.reset()
        validate_routes(r)
        
        start_ts = jh.date_to_timestamp(start_date)
        finish_ts = jh.date_to_timestamp(finish_date)
        
        print(f"Cargando velas {start_ts} -> {finish_ts}")
        
        # Intentamos cargar velas directamente para ver el fallo
        warmup_candles, candles = backtest_mode.load_candles(start_ts, finish_ts)
        
        if candles is None or len(candles) == 0:
            print("ERROR: Velas cargadas es None o vacio.")
            return None
            
        print(f"Cargadas {len(candles)} velas.")
        return True

    except Exception:
        print("!!! EXCEPCION DETECTADA !!!")
        traceback.print_exc()
        return None

run_test('Titan_Oro')
