import os
import sys
import multiprocessing

# --- AMBIENTE JESSE ---
sys.path.insert(0, os.getcwd())

import jesse.helpers as jh
from jesse.modes import backtest_mode

def worker_target(client_id, user_config, exchange, routes):
    print("Iniciando target del trabajador...")
    try:
        # Importar dinámicamente para simular el entorno del worker
        from jesse.modes import backtest_mode
        backtest_mode._execute_backtest(
            client_id, False, user_config, exchange, routes, [],
            '2026-02-15', '2026-03-14'
        )
    except Exception as e:
        print(f"CRASH EN EL WORKER: {e}")
        import traceback
        traceback.print_exc()

def run_forensic():
    print("Iniciando Diagnóstico Forense del Worker (Windows)...")
    
    client_id = 'forensic-001'
    user_config = {
        'warm_up_candles': 240,
        'exchanges': {
            'Binance Perpetual Futures': {
                'name': 'Binance Perpetual Futures',
                'fee': 0.0004,
                'type': 'futures',
                'balance': 10000
            }
        },
        'logging': {'balance_update': True}
    }
    exchange = 'Binance Perpetual Futures'
    routes = [{'exchange': exchange, 'symbol': 'PAXG-USDT', 'timeframe': '1m', 'strategy': 'Gold_Terminator'}]
    
    # Intentar ejecutar el worker manualmente en un proceso de multiprocessing
    if os.name == 'nt':
        multiprocessing.set_start_method('spawn', force=True)
    
    p = multiprocessing.Process(target=worker_target, args=(client_id, user_config, exchange, routes))
    p.start()
    p.join(timeout=30)
    
    if p.is_alive():
        print("El worker se quedó bloqueado (0% freeze detectable).")
        p.terminate()
    else:
        print(f"El worker terminó con código: {p.exitcode}")

if __name__ == "__main__":
    run_forensic()
