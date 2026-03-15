import os
import sys
import time
import threading

# --- AMBIENTE JESSE ---
sys.path.insert(0, os.getcwd())

import jesse.helpers as jh
from jesse.modes import backtest_mode
from jesse.config import config, set_config
from jesse.routes import router
from jesse.store import store
from jesse.services.redis import sync_redis

def run_test():
    print("Iniciando Test de Infraestructura Jesse 2026 (Fix Configuration V4 - Correct Dict)...")
    
    # Simular un client_id único
    client_id = jh.generate_unique_id()
    
    # Estructura de diccionario con 'name' interno como pide set_config:144
    user_config = {
        'warm_up_candles': 240,
        'exchanges': {
            'Binance Perpetual Futures': {
                'name': 'Binance Perpetual Futures',
                'fee': 0.0004,
                'type': 'futures',
                'futures_leverage_mode': 'cross',
                'futures_leverage': 50,
                'balance': 10000
            }
        },
        'logging': {
            'balance_update': True, 
            'order_execution': True,
            'trading_candles': True,
        }
    }
    
    exchange = 'Binance Perpetual Futures'
    symbol = 'PAXG-USDT'
    timeframe = '1m'
    strategy = 'Gold_Terminator'
    start_date = '2026-02-15'
    finish_date = '2026-03-14'
    
    # Rutas
    routes = [{'exchange': exchange, 'symbol': symbol, 'timeframe': timeframe, 'strategy': strategy}]
    
    # Monitorear fakeredis en un hilo aparte para ver si el progreso llega
    def monitor_progress():
        print("Monitor de Progreso: ACTIVO")
        key = f"9000:channel:1" 
        pubsub = sync_redis.pubsub()
        pubsub.subscribe(key)
        
        start_time = time.time()
        while time.time() - start_time < 60: 
            message = pubsub.get_message()
            if message and message['type'] == 'message':
                import json
                data = json.loads(message['data'])
                if 'event' in data and 'backtest.progress' in data['event']:
                    print(f"PROGRESO RECIBIDO: {data['data']['percentage']}%")
                if 'event' in data and 'backtest.exception' in data['event']:
                    print(f"ERROR RECIBIDO: {data['data']['error']}")
            time.sleep(0.1)

    m_thread = threading.Thread(target=monitor_progress)
    m_thread.daemon = True
    m_thread.start()

    # Ejecutar backtest
    try:
        backtest_mode.run(
            client_id, False, user_config, exchange, routes, [],
            start_date, finish_date
        )
    except Exception as e:
        print(f"CRASH EN BACKTEST: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
