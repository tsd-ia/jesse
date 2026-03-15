import os
import sys
import pandas as pd
import sqlite3
import random

# Entorno Jesse
sys.path.insert(0, os.getcwd())
from jesse.research import backtest
import jesse.helpers as jh

def run_hft_audit():
    print("🔥 LANZANDO AUDITORÍA TITAN HFT (200 MODELOS)")
    
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query("SELECT timestamp, open, high, low, close, volume FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    config = {
        'starting_balance': 500,
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 50,
        'exchange': 'Binance Perpetual Futures',
        'warm_up_candles': 210
    }

    routes = [{'exchange': 'Binance Perpetual Futures', 'symbol': 'BTC-USDT', 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}]
    data_routes = [{'exchange': 'Binance Perpetual Futures', 'symbol': 'BTC-USDT', 'timeframe': '1m'}]
    candles_dict = {jh.key('Binance Perpetual Futures', 'BTC-USDT'): {'exchange': 'Binance Perpetual Futures', 'symbol': 'BTC-USDT', 'candles': df.values}}

    results = []
    
    for i in range(200):
        hps = {'sensitivity': random.uniform(0.1, 1.0), 'tp_usd': random.uniform(1.0, 5.0)}
        try:
            res = backtest(config, routes, data_routes, candles_dict, hyperparameters=hps)
            m = res['metrics']
            # Si m es None, significa que el bot fue liquidado o falló, pero capturamos los trades si existen
            n_trades = len(res.get('trades', []))
            roi = m['net_profit_percentage'] if m else -100.0
            results.append({'ID': f"HFT_{i:03d}", 'TRADES': n_trades, 'ROI': roi})
            if i % 10 == 0: print(f"Procesado HFT {i}/200 - Trades detectados: {n_trades}")
        except:
            continue

    ranking = pd.DataFrame(results).sort_values(by='TRADES', ascending=False)
    ranking.to_csv('RANKING_TITAN_HFT_2026.csv', index=False)
    print("\n✅ RANKING HFT GENERADO:")
    print(ranking.head(10).to_string(index=False))

if __name__ == "__main__":
    run_hft_audit()
