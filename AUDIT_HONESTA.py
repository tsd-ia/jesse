import os
import sys
import numpy as np
import pandas as pd
import sqlite3

# --- ENTORNO ---
sys.path.insert(0, os.getcwd())
import jesse.helpers as jh
from jesse.research import backtest

def load_data(symbol):
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query(f"SELECT timestamp, open, close, high, low, volume FROM Candle WHERE symbol='{symbol}' ORDER BY timestamp ASC LIMIT 5000", conn)
    conn.close()
    return df.values

def run_real_audit():
    print("🚢 EJECUTANDO AUDITORÍA REAL EN MOTOR JESSE ($500 USD)")
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    all_candles = load_data(symbol)
    
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[240:]}}
    warmup_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[:240]}}

    config = {
        'starting_balance': 500,
        'fee': 0.0004, # Comisión real de Binance
        'type': 'futures',
        'futures_leverage': 100,
        'futures_leverage_mode': 'cross',
        'exchange': exchange,
        'warm_up_candles': 240
    }
    
    try:
        res = backtest(config, [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}], 
                       [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                       candles=candles_dict, warmup_candles=warmup_dict)
        
        m = res['metrics']
        print("\n========================================")
        print("📊 REPORTE DE EJECUCIÓN REAL (NO SIMULADO)")
        print(f"ROI: {m.get('net_profit_percentage', 0):.2f}%")
        print(f"Trades: {len(res.get('trades', []))}")
        print(f"WinRate: {m.get('win_rate', 0)*100:.2f}%")
        print("========================================\n")
        
        df = pd.DataFrame([{
            'ROI': m.get('net_profit_percentage', 0),
            'Trades': len(res.get('trades', [])),
            'WinRate': m.get('win_rate', 0)
        }])
        df.to_csv('REPORTE_HONESTO_JESSE.csv', index=False)
        
    except Exception as e:
        print(f"Fallo técnico en Jesse: {e}")

if __name__ == "__main__":
    run_real_audit()
