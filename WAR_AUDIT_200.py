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
    # Cargamos un bloque sólido de velas de marzo 2026
    df = pd.read_sql_query(f"SELECT timestamp, open, close, high, low, volume FROM Candle WHERE symbol='{symbol}' ORDER BY timestamp ASC", conn)
    conn.close()
    return df.values

def run_war_audit():
    print("🔥 LANZANDO AUDITORÍA DE COMBATE (200 VARIACIONES $500)")
    
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    all_candles = load_data(symbol)
    
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[240:]}}
    warmup_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[:240]}}

    results = []
    
    # Generamos 200 variaciones profesionales de la MasterWarrior
    for i in range(200):
        # Variamos parámetros de la lógica core para encontrar el 'Sweet Spot'
        config = {
            'starting_balance': 500,
            'fee': 0.0004,
            'type': 'futures',
            'futures_leverage': 50 + (i * 2), # Apalancamiento dinámico 50x a 450x
            'futures_leverage_mode': 'cross',
            'exchange': exchange,
            'warm_up_candles': 240
        }
        
        try:
            res = backtest(config, [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}], 
                           [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                           candles=candles_dict, warmup_candles=warmup_dict)
            
            m = res['metrics']
            results.append({
                'ID': i + 1,
                'ROI': round(m.get('net_profit_percentage', 0), 2),
                'WinRate': round(m.get('win_rate', 0)*100, 2),
                'Trades': len(res.get('trades', [])),
                'Leverage': config['futures_leverage'],
                'MaxDD': round(m.get('max_drawdown', 0), 2)
            })
        except:
            pass
            
        if (i+1) % 50 == 0:
            print(f"[*] Progreso: {i+1}/200 concluidos.")

    # Guardar Reporte Final
    df = pd.DataFrame(results)
    df.to_csv('RANKING_MUNDIAL_ORO_2026.csv', index=False)
    print("\n✅ MEGA-AUDITORÍA FINALIZADA. Archivo: RANKING_MUNDIAL_ORO_2026.csv")
    print(df.sort_values(by='ROI', ascending=False).head(15).to_string(index=False))

if __name__ == "__main__":
    run_war_audit()
