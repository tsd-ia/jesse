import os
import sys

# --- AMBIENTE JESSE ---
sys.path.insert(0, os.getcwd())

import jesse.helpers as jh
from jesse.modes import backtest_mode
from jesse.config import set_config
from jesse.services.redis import sync_redis

def run_synchronous_backtest():
    print("Iniciando Backtest Síncrono (Bypass Multiprocessing)...")
    
    client_id = 'sync-cert-001'
    # Configuración manual para asegurar que no falte nada
    user_config = {
        'warm_up_candles': 240,
        'exchanges': {
            'Binance Perpetual Futures': {
                'name': 'Binance Perpetual Futures',
                'fee': 0.0004,
                'type': 'futures',
                'balance': 10000,
                'futures_leverage_mode': 'cross',
                'futures_leverage': 1
            }
        },
        'logging': {
            'balance_update': True,
            'trading_candles': True
        }
    }
    
    exchange = 'Binance Perpetual Futures'
    routes = [{
        'exchange': exchange, 
        'symbol': 'PAXG-USDT', 
        'timeframe': '1m', 
        'strategy': 'Gold_Terminator'
    }]
    
    # Marcar como activo en el redis local (fakeredis)
    from jesse.services.env import ENV_VALUES
    sync_redis.sadd(f"{ENV_VALUES['APP_PORT']}|active-processes", client_id)
    
    try:
        # EJECUCIÓN DIRECTA
        print("Cargando motor de backtest...")
        backtest_mode._execute_backtest(
            client_id, False, user_config, exchange, routes, [],
            '2026-02-15', '2026-03-14'
        )
        print("\n--- BACKTEST COMPLETADO ---")
    except Exception as e:
        print(f"\nERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_synchronous_backtest()
