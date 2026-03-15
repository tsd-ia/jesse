import os
import sys
import numpy as np
import pandas as pd
import sqlite3
import random

# --- ENTORNO ---
sys.path.insert(0, os.getcwd())
import jesse.helpers as jh
from jesse.research import backtest

def load_data(symbol):
    conn = sqlite3.connect('jesse_db.sqlite')
    # Cargamos 30,000 velas para tener historial real de 2026
    df = pd.read_sql_query(f"SELECT timestamp, open, close, high, low, volume FROM Candle WHERE symbol='{symbol}' ORDER BY timestamp ASC", conn)
    conn.close()
    return df.values

def run_ultimate_200_audit():
    print("🔥 INICIANDO MEGA-AUDITORÍA FINAL (200 ESTRATEGIAS ÚNICAS $500)")
    
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    all_candles = load_data(symbol)
    
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[240:]}}
    warmup_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[:240]}}

    # ADN de los mejores bots del mundo
    dnas = ['SMC', 'HFT', 'Reversal']
    kill_zones = [(8, 11), (13, 16), (20, 23), (0, 7)]
    lots = [0.01, 0.05, 0.1, 0.25]
    
    results = []
    
    for i in range(200):
        # Generar combinación única
        dna = random.choice(dnas)
        kz = random.choice(kill_zones)
        lot = random.choice(lots)
        tp = random.uniform(20, 80)
        sl = random.uniform(10, 30)
        
        config = {
            'starting_balance': 500,
            'fee': 0.0004,
            'type': 'futures',
            'futures_leverage': 100,
            'futures_leverage_mode': 'cross',
            'exchange': exchange,
            'warm_up_candles': 240
        }
        
        hps = {
            'dna': dna,
            'h_start': kz[0],
            'h_end': kz[1],
            'lot': lot,
            'tp': tp,
            'sl': sl
        }
        
        try:
            res = backtest(config, [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}], 
                           [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                           candles=candles_dict, warmup_candles=warmup_dict, hyperparameters=hps)
            
            m = res['metrics']
            results.append({
                'ID': i + 1,
                'Style': dna,
                'KZ': f"{kz[0]}-{kz[1]}",
                'Lot': lot,
                'ROI': round(m.get('net_profit_percentage', 0), 2),
                'WinRate': round(m.get('win_rate', 0)*100, 2),
                'Trades': len(res.get('trades', [])),
                'MaxDD': round(m.get('max_drawdown', 0), 2)
            })
        except:
            pass
            
        if (i+1) % 50 == 0:
            print(f"[*] Progreso: {i+1}/200 concluidos.")

    # Guardar Reporte Final
    df = pd.DataFrame(results)
    df.to_csv('REPORT_MUNDIAL_ORO_2026.csv', index=False)
    print("\n✅ MEGA-AUDITORÍA FINALIZADA. Archivo: REPORT_MUNDIAL_ORO_2026.csv")
    print(df.sort_values(by='ROI', ascending=False).head(10).to_string(index=False))

if __name__ == "__main__":
    run_ultimate_200_audit()
