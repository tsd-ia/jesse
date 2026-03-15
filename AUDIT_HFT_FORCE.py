import os
import sys
import pandas as pd
import sqlite3
import random

sys.path.insert(0, os.getcwd())
from jesse.research import backtest
import jesse.helpers as jh

def run_hft_audit_2026():
    print("🔥 INICIANDO AUDITORÍA TITAN HFT (200 VARIACIONES)")
    
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query("SELECT timestamp, open, high, low, close, volume FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    # Subiremos el balance a $100,000 para que el bot pueda tradear miles de veces sin morir por comisiones
    config = {
        'starting_balance': 100000,
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 50,
        'futures_leverage_mode': 'cross',
        'exchange': 'Binance Perpetual Futures',
        'warm_up_candles': 210
    }

    routes = [{'exchange': 'Binance Perpetual Futures', 'symbol': 'BTC-USDT', 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}]
    data_routes = [{'exchange': 'Binance Perpetual Futures', 'symbol': 'BTC-USDT', 'timeframe': '1m'}]
    candles_dict = {jh.key('Binance Perpetual Futures', 'BTC-USDT'): {'exchange': 'Binance Perpetual Futures', 'symbol': 'BTC-USDT', 'candles': df.values}}

    results = []
    
    for i in range(200):
        hps = {
            'sensitivity': random.uniform(0.01, 0.2),
            'tp_usd': random.uniform(1.0, 5.0)
        }
        
        try:
            res = backtest(config, routes, data_routes, candles_dict, hyperparameters=hps)
            m = res['metrics']
            n_trades = len(res.get('trades', []))
            
            results.append({
                'ID': f"HFT_{i:03d}",
                'TRADES': n_trades,
                'ROI': round(m['net_profit_percentage'], 2),
                'WIN_RATE': round(m['win_rate'] * 100, 2)
            })
            if i % 10 == 0:
                print(f"Auditando bot {i}/200 - Trades: {n_trades}")

        except Exception as e:
            continue

    ranking = pd.DataFrame(results).sort_values(by='TRADES', ascending=False)
    ranking.to_csv('RANKING_HFT_CERTIFICADO_2026.csv', index=False)
    print("\n✅ RANKING HFT GENERADO:")
    print(ranking.head(10).to_string(index=False))

if __name__ == "__main__":
    run_hft_audit_2026()
