import os
import sys

# --- ENTORNO JESSE ---
sys.path.insert(0, os.getcwd())

import jesse.helpers as jh
from jesse.modes import backtest_mode
from jesse.config import set_config
from jesse.services.redis import sync_redis
import jesse.services.redis as redis_service

# MOCK PARA CAPTURAR TRADES
def mock_publish(event, msg, compression=False):
    if event == 'trades':
        # msg es una lista de trades
        print("\n--- AUDITORÍA DE TRADES ---")
        for i, t in enumerate(msg[-5:]): # Últimos 5
            print(f"Trade {i}: Side:{t['type']} | Entry:{t['entry_price']} | Exit:{t['exit_price']} | PNL:{t['pnl']} | PNL%:{t['pnl_percentage']}%")
        print("--------------------------\n")

# Inyectar mocks
import jesse.models.BacktestSession as bs
bs.store_backtest_session = lambda *args, **kwargs: None
bs.update_backtest_session_status = lambda *args, **kwargs: None
bs.update_backtest_session_results = lambda *args, **kwargs: None
bs.store_backtest_session_exception = lambda *args, **kwargs: None

backtest_mode.sync_publish = mock_publish

def auditar_trades():
    client_id = 'AUDIT-TRADES-001'
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
        'logging': {'balance_update': False}
    }
    
    exchange = 'Binance Perpetual Futures'
    routes = [{'exchange': exchange, 'symbol': 'PAXG-USDT', 'timeframe': '1m', 'strategy': 'Gold_Terminator'}]
    
    try:
        jh.should_execute_silently = lambda: False
        from jesse.config import config
        config['app']['trading_mode'] = 'backtest'
        
        backtest_mode._execute_backtest(
            client_id, False, user_config, exchange, routes, [],
            '2026-03-10', '2026-03-14'
        )
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    auditar_trades()
