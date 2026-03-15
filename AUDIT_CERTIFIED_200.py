import os
import sys
import numpy as np
import pandas as pd
import sqlite3
import random

sys.path.insert(0, os.getcwd())
import jesse.helpers as jh
from jesse.research import backtest

def load_data(symbol):
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query(f"SELECT timestamp, open, close, high, low, volume FROM Candle WHERE symbol='{symbol}' ORDER BY timestamp ASC", conn)
    conn.close()
    return df.values

def run_certified_audit():
    print("💎 INICIANDO MEGA-AUDITORÍA 200 ESTRATEGIAS ($500 USD) - VERSIÓN FINAL")
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    all_candles = load_data(symbol)
    
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[240:]}}
    warmup_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[:240]}}

    dnas = ['SMC_Ghost', 'London_Breakout', 'Grid_Venus', 'HFT_Velocity', 'Trend_Filter', 
            'Fibonacci_Level', 'OrderBlock_Mitigation', 'Psych_Numbers', 'Volume_POC', 'RSI_Divergence']
    
    results = []
    
    for i in range(200):
        dna = dnas[i % len(dnas)]
        risk = random.choice([0.01, 0.05, 0.1, 0.2])
        config = {'starting_balance': 500, 'fee': 0.0004, 'type': 'futures', 'futures_leverage': 50, 'futures_leverage_mode': 'cross', 'exchange': exchange, 'warm_up_candles': 240}
        hps = {'dna': dna, 'risk': risk, 'tp': random.uniform(20, 100), 'sl': random.uniform(10, 30)}
        
        try:
            res = backtest(config, [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}], [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], candles=candles_dict, warmup_candles=warmup_dict, hyperparameters=hps)
            m = res['metrics']
            results.append({'ID': i+1, 'DNA': dna, 'Risk': risk, 'ROI': m.get('net_profit_percentage', 0), 'WinRate': m.get('win_rate', 0), 'Trades': len(res.get('trades', []))})
        except: pass
        if (i+1) % 20 == 0: print(f"Auditando: {i+1}/200...")

    df = pd.DataFrame(results)
    df.to_csv('REPORT_FINAL_200.csv', index=False)
    print("\n✅ REPORTE GENERADO: REPORT_FINAL_200.csv")
    print(df.sort_values(by='ROI', ascending=False).head(10).to_string())

if __name__ == "__main__":
    run_certified_audit()
