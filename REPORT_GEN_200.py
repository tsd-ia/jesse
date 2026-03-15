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
    # Cargamos 20,000 velas para tener suficiente historial de trades (aprox 14 dias)
    df = pd.read_sql_query(f"SELECT timestamp, open, close, high, low, volume FROM Candle WHERE symbol='{symbol}' ORDER BY timestamp DESC LIMIT 20000", conn)
    conn.close()
    return df.iloc[::-1].values

def run_ultimate_audit():
    print("🔥 LANZANDO AUDITORÍA MAESTRA DE 200 ESTRATEGIAS ($500 USD)")
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    all_candles = load_data(symbol)
    
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[240:]}}
    warmup_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[:240]}}

    dnas = ['SMC_Ghost', 'London_Breakout', 'Grid_Venus', 'HFT_Velocity', 'Trend_Filter', 
            'Fibonacci_Level', 'OrderBlock_Mitigation', 'Psych_Numbers', 'Volume_POC', 'RSI_Divergence']
    
    results = []
    
    for i in range(200):
        # Elegimos una logica base y variamos parámetros para crear una estrategia UNICA
        dna = dnas[i % len(dnas)]
        risk = random.choice([0.01, 0.05, 0.1, 0.2, 0.3])
        tp_val = random.uniform(10, 80)
        sl_val = random.uniform(5, 25)
        
        config = {'starting_balance': 500, 'fee': 0.0004, 'type': 'futures', 'futures_leverage': 100, 'futures_leverage_mode': 'cross', 'exchange': exchange, 'warm_up_candles': 240}
        hps = {'dna': dna, 'risk': risk, 'tp': tp_val, 'sl': sl_val}
        
        try:
            res = backtest(config, 
                           [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}], 
                           [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                           candles=candles_dict, warmup_candles=warmup_dict, hyperparameters=hps)
            
            m = res['metrics']
            results.append({
                'ID': i+1, 
                'Estrategia_Estilo': f"{dna}_v{i}", 
                'ADN_Base': dna,
                'Riesgo_%': risk*100, 
                'TakeProfit_USD': round(tp_val, 2),
                'StopLoss_USD': round(sl_val, 2),
                'ROI_%': round(m.get('net_profit_percentage', 0), 2), 
                'WinRate_%': round(m.get('win_rate', 0)*100, 2), 
                'Total_Trades': len(res.get('trades', []))
            })
        except Exception as e:
            pass
            
        if (i+1) % 50 == 0: print(f"Procesando: {i+1}/200...")

    df = pd.DataFrame(results)
    df.to_csv('REPORT_FINAL_CERTIFIED.csv', index=False)
    print("\n✅ MEGA-AUDITORÍA FINALIZADA.")
    top_10 = df.sort_values(by='ROI_%', ascending=False).head(10)
    print("\n--- TOP 10 ESTRATEGIAS RECONQUISTA 2026 ---")
    print(top_10[['Estrategia_Estilo', 'ADN_Base', 'ROI_%', 'WinRate_%', 'Total_Trades']].to_string(index=False))

if __name__ == "__main__":
    run_ultimate_audit()
