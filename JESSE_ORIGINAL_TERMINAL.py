import os
import sys

# --- ENTORNO PROYECTO ---
sys.path.insert(0, os.getcwd())

import jesse.helpers as jh
from jesse.modes import backtest_mode
from jesse.config import set_config, config
from jesse.routes import router
import uuid

def main():
    print("--- INICIANDO MOTOR JESSE ORIGINAL ---")
    
    client_id = str(uuid.uuid4())
    user_config = {
        'warm_up_candles': 240,
        'exchanges': {
            'Binance Perpetual Futures': {
                'name': 'Binance Perpetual Futures',
                'fee': 0.0004,
                'type': 'futures',
                'balance': 10000,
                'futures_leverage': 10,
                'futures_leverage_mode': 'cross'
            }
        },
        'logging': {
            'balance_update': True,
            'order_execution': True,
            'trading_candles': False,
            'show_all_logs': False
        },
        'indicators': {
            'talib': True
        }
    }
    
    # 2. Inyectar config y rutas
    set_config(user_config)
    config['app']['trading_mode'] = 'backtest'
    
    # Ruta: Binance Perpetual Futures, PAXG-USDT, 1m, Gold_Terminator
    routes = [{
        'exchange': 'Binance Perpetual Futures', 
        'symbol': 'PAXG-USDT', 
        'timeframe': '1m', 
        'strategy': 'Gold_Terminator'
    }]
    router.initiate(routes, [])
    
    # 3. Lanzar backtest vía CLI interno (bypass multiprocessing para ver salida)
    print("Ejecutando simulación...")
    try:
        # Esto llamará al simulador y debería imprimir la tabla de Jesse al final
        # si lo hacemos bien.
        backtest_mode.run(
            client_id, 
            False, 
            user_config, 
            'Binance Perpetual Futures', 
            routes, 
            [], 
            '2026-03-01', 
            '2026-03-14'
        )
        
        # 4. EXTRAER Y MOSTRAR RESULTADOS REALES DE JESSE
        from jesse.store import store
        from jesse.services import metrics
        
        # Jesse guarda los trades en store.closed_trades.trades
        completed_trades = store.closed_trades.trades
        if len(completed_trades) > 0:
            # Necesitamos el balance diario para las métricas
            daily_balance = store.app.daily_balance
            stats = metrics.trades(completed_trades, daily_balance)
            
            print("\n" + "="*50)
            print("🏆 REPORTE REAL GENERADO POR EL MOTOR JESSE 🏆")
            print("="*50)
            print(f"Total Trades: {len(completed_trades)}")
            print(f"Net Profit: {stats['net_profit_percentage']:.2f}%")
            print(f"Win Rate: {stats['win_rate'] * 100:.2f}%")
            print(f"Max Drawdown: {stats['max_drawdown']:.2f}%")
            print("="*50)
        else:
            print("\n[!] No se ejecutaron trades en el periodo seleccionado.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
