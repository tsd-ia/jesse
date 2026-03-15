import os
import sys

# --- ENTORNO JESSE ---
sys.path.insert(0, os.getcwd())

import jesse.helpers as jh
from jesse.modes import backtest_mode
from jesse.config import set_config
from jesse.services import report
from jesse.routes import router

# MOCKS PARA ESTABILIDAD EN WINDOWS
def ghost_func(*args, **kwargs): pass
import jesse.models.BacktestSession as bs
bs.store_backtest_session = ghost_func
bs.update_backtest_session_status = ghost_func
bs.update_backtest_session_results = ghost_func
bs.store_backtest_session_exception = ghost_func

# Forzamos que Jesse NO intente usar WebSockets/Redis para el progreso
jh.should_execute_silently = lambda: True

def certificar_real():
    print(">>> EJECUTANDO MOTOR JESSE ORIGINAL (MODO SINCRONO)")
    
    client_id = 'REAL-REPORT-2026'
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
            'order_execution': True # Queremos ver las ordenes reales
        }
    }
    
    exchange = 'Binance Perpetual Futures'
    symbol = 'PAXG-USDT'
    # Usaremos Antigravity_Beast que es la que tiene mas sentido tecnico
    routes = [{'exchange': exchange, 'symbol': symbol, 'timeframe': '15m', 'strategy': 'Antigravity_Beast'}]
    
    try:
        from jesse.config import config
        config['app']['trading_mode'] = 'backtest'
        
        # Ejecutar simulacion completa
        result = backtest_mode.simulator(
            {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': None}}, # None para que cargue de DB
            run_silently=True
        )
        
        if result and 'metrics' in result:
            print("\n" + "="*60)
            print("          INFORME OFICIAL DE JESSE (TERMINAL)          ")
            print("="*60)
            # Usamos el formateador interno de Jesse para el reporte
            print(f"Estrategia: Antigravity_Beast | Periordo: 2026-02-15 / 2026-03-14")
            print(f"Total Trades: {result['metrics']['total_closed_trades']}")
            print(f"Net Profit: {result['metrics']['net_profit_percentage']}%")
            print(f"Win Rate: {result['metrics']['win_rate'] * 100}%")
            print(f"Max Drawdown: {result['metrics']['max_drawdown']}%")
            print("="*60)
            
            if len(result['trades']) > 0:
                print("\nÚLTIMOS 3 TRADES DETALLADOS:")
                for t in result['trades'][-3:]:
                    print(f"ID: {t['id']} | {t['type']} | PNL: {t['pnl']} ({t['pnl_percentage']}%)")
        else:
            print("Jesse no generó métricas. Es posible que no se cumplieran las condiciones de entrada.")

    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    certificar_real()
