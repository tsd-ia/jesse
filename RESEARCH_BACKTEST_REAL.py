import os
import sys
import numpy as np
import sqlite3
from datetime import datetime

# --- ENTORNO PROYECTO ---
sys.path.insert(0, os.getcwd())

import jesse.helpers as jh
from jesse.research import backtest

def load_candles_from_db(exchange, symbol, start_date, finish_date):
    start_ts = jh.date_to_timestamp(start_date)
    finish_ts = jh.date_to_timestamp(finish_date)
    
    conn = sqlite3.connect('jesse_db.sqlite')
    cursor = conn.cursor()
    query = "SELECT timestamp, open, high, low, close, volume FROM Candle WHERE exchange=? AND symbol=? AND timeframe='1m' AND timestamp>=? AND timestamp<=? ORDER BY timestamp ASC"
    cursor.execute(query, (exchange, symbol, start_ts, finish_ts))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return np.array([])
    
    # Jesse format: [timestamp, open, close, high, low, volume]
    return np.array([[float(r[0]), float(r[1]), float(r[4]), float(r[2]), float(r[3]), float(r[5])] for r in rows])

def run_real_research():
    print("--- INICIANDO BACKTEST VIA JESSE RESEARCH MODULE (OFFICIAL) ---")
    
    exchange = 'Binance Perpetual Futures'
    symbol = 'PAXG-USDT'
    start_date = '2026-03-01'
    finish_date = '2026-03-14'
    
    # Cargar velas
    all_candles = load_candles_from_db(exchange, symbol, start_date, finish_date)
    if len(all_candles) == 0:
        print("No se encontraron velas en la base de datos.")
        return

    # Dividir en warmup y trading (Jesse Research lo maneja por separado si se desea, 
    # o simplemente pasamos las velas de trading y el warmup_candles en la config)
    warmup_count = 240
    warmup_candles = all_candles[:warmup_count]
    trading_candles = all_candles[warmup_count:]

    # Configuración formato Research (REAL PARA EL COMANDANTE)
    config = {
        'starting_balance': 363.80, # Capital Real Reconquista
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 200,    # Apalancamiento agresivo 200x
        'futures_leverage_mode': 'cross',
        'exchange': exchange,
        'warm_up_candles': warmup_count
    }

    # Rutas
    routes = [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'Gold_Terminator'}]
    data_routes = [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}]

    # Velas formato dict para Research
    candles_dict = {
        jh.key(exchange, symbol): {
            'exchange': exchange,
            'symbol': symbol,
            'candles': trading_candles
        }
    }
    
    warmup_dict = {
        jh.key(exchange, symbol): {
            'exchange': exchange,
            'symbol': symbol,
            'candles': warmup_candles
        }
    }

    print(f"Ejecutando simulación para {len(trading_candles)} minutos...")
    
    try:
        # LLAMADA OFICIAL AL MÓDULO DE INVESTIGACIÓN
        result = backtest(
            config,
            routes,
            data_routes,
            candles=candles_dict,
            warmup_candles=warmup_dict,
            generate_equity_curve=True
        )
        
        if result and 'metrics' in result:
            print("\n" + "="*50)
            print("🏆 REPORTE OFICIAL JESSE (RESEARCH MODULE) 🏆")
            print("="*50)
            m = result['metrics']
            print(f"Total Trades: {m.get('total', 0)}")
            print(f"Net Profit: {m.get('net_profit_percentage', 0):.2f}%")
            print(f"Win Rate: {m.get('win_rate', 0)*100:.2f}%")
            print("="*50)
            
            if 'trades' in result and len(result['trades']) > 0:
                print(f"\nSe ejecutaron {len(result['trades'])} trades reales.")
        else:
            print("No se generaron resultados.")

    except Exception as e:
        print(f"Error en el módulo Research: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_real_research()
