import os
import sys

# --- ENTORNO JESSE ---
sys.path.insert(0, os.getcwd())

import jesse.helpers as jh
from jesse.modes import backtest_mode
from jesse.config import set_config
from jesse.services.redis import sync_redis
import jesse.services.redis as redis_service

# 1. MOCK DE PUBLICACIÓN PARA IMPRIMIR MÉTRICAS
def mock_publish(event, msg, compression=False):
    if event == 'metrics':
        print("\n" + "="*50)
        print("          MÉTRICAS FINALES DE BACKTEST          ")
        print("="*50)
        for key, val in msg.items():
            if key in ['total_net_profit', 'net_profit_percentage', 'win_rate', 'total_trades', 'max_drawdown']:
                print(f"{key.replace('_', ' ').upper()}: {val}")
        print("="*50 + "\n")
    elif event == 'backtest.progress':
        # Mostrar algo de feedback aunque no tengamos Dashboard
        print(f"[PROGRESS] {msg}%", end='\r')

# 2. MOCK DE BASE DE DATOS PARA EVITAR ERROR DE UUID
def ghost_func(*args, **kwargs): pass

# Inyectar mocks
import jesse.models.BacktestSession as bs
bs.store_backtest_session = ghost_func
bs.update_backtest_session_status = ghost_func
bs.update_backtest_session_results = ghost_func
bs.store_backtest_session_exception = ghost_func

backtest_mode.sync_publish = mock_publish
redis_service.sync_publish = mock_publish

def certificar_roi_2026():
    print("==================================================")
    print("   CERTIFICACIÓN ULTRA-DIRECTA GOLD 2026          ")
    print("==================================================")
    
    # Client ID dummy (ya no importa porque no va a DB)
    client_id = '00000000-0000-0000-0000-000000000000'
    
    # Configuración de combate
    user_config = {
        'warm_up_candles': 240,
        'exchanges': {
            'Binance Perpetual Futures': {
                'name': 'Binance Perpetual Futures',
                'fee': 0.0004,
                'type': 'futures',
                'balance': 10000,
                'futures_leverage_mode': 'cross',
                'futures_leverage': 10
            }
        },
        'logging': {
            'balance_update': False,
            'trading_candles': False,
            'strategy_execution': False
        }
    }
    
    exchange = 'Binance Perpetual Futures'
    routes = [{
        'exchange': exchange, 
        'symbol': 'PAXG-USDT', 
        'timeframe': '1m', 
        'strategy': 'Gold_Terminator'
    }]
    
    print(f"[*] Período: 2026-02-15 a 2026-03-14")
    
    try:
        # Aseguramos que NO sea silencioso para que llame a sync_publish con las métricas
        jh.should_execute_silently = lambda: False
        
        from jesse.config import config
        config['app']['trading_mode'] = 'backtest'
        
        # Ejecución directa
        backtest_mode._execute_backtest(
            client_id, 
            False, 
            user_config, 
            exchange, 
            routes, 
            [], 
            '2026-02-15', 
            '2026-03-14'
        )
        
        print("\n[V] PRUEBA FINALIZADA.")
        
    except Exception as e:
        print(f"\n[X] ERROR DURANTE LA CERTIFICACIÓN: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    certificar_roi_2026()
