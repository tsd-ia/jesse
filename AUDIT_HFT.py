import os
import sys
import numpy as np
import pandas as pd
import sqlite3

# --- ENTORNO ---
sys.path.insert(0, os.getcwd())
import jesse.helpers as jh
from jesse.research import backtest

def load_data(symbol, start, finish):
    conn = sqlite3.connect('jesse_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT timestamp, open, high, low, close, volume FROM Candle WHERE symbol=? AND timestamp>=? AND timestamp<=?", (symbol, start, finish))
    rows = c.fetchall()
    conn.close()
    return np.array([[float(r[0]), float(r[1]), float(r[4]), float(r[2]), float(r[3]), float(r[5])] for r in rows])

def run_hft_audit():
    print("🚢 AUDITORÍA HFT AGRESIVA ($500 USD)")
    
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    all_candles = load_data(symbol, jh.date_to_timestamp('2026-03-01'), jh.date_to_timestamp('2026-03-14'))
    
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[240:]}}
    warmup_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[:240]}}
    
    config = {
        'starting_balance': 500,
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 100,
        'futures_leverage_mode': 'cross',
        'exchange': exchange,
        'warm_up_candles': 240
    }
    
    res = backtest(config, [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'HighFrequencyGold'}], 
                   [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                   candles=candles_dict, warmup_candles=warmup_dict)
    
    m = res['metrics']
    trades = res.get('trades', [])
    
    report = {
        'Estrategia': 'HighFrequencyGold_REAL',
        'Capital': 500,
        'ROI': f"{m.get('net_profit_percentage', 0):.2f}%",
        'Trades': len(trades),
        'WinRate': f"{m.get('win_rate', 0)*100:.2f}%"
    }
    
    pd.DataFrame([report]).to_csv('REPORTE_HFT_REAL.csv', index=False)
    print("\n[V] Auditoría finalizada. Datos guardados en REPORTE_HFT_REAL.csv")

if __name__ == "__main__":
    run_hft_audit()
