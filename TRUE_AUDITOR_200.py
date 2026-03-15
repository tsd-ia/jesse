import os
import sys
import pandas as pd
import sqlite3
import random

# Entorno Jesse
sys.path.insert(0, os.getcwd())
from jesse.research import backtest
import jesse.helpers as jh

def run_true_varied_audit():
    print("🔥 LANZANDO AUDITORÍA REAL DE 200 VARIACIONES (BTC-USDT)")
    
    # Cargar Velas
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query("SELECT timestamp, open, high, low, close, volume FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    candles_np = df.values
    
    exchange = 'Binance Perpetual Futures'
    symbol = 'BTC-USDT'
    
    config = {
        'starting_balance': 500,
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 50,
        'futures_leverage_mode': 'cross',
        'exchange': exchange,
        'warm_up_candles': 210
    }

    # API v2026 Requisitos
    routes = [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}]
    data_routes = [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}]
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': candles_np}}

    results = []
    
    for i in range(200):
        # Generamos Hiperparámetros ÚNICOS
        hps = {
            'fast_ema': random.randint(3, 10),
            'slow_ema': random.randint(11, 25),
            'stop_loss_pct': round(random.uniform(0.5, 3.0), 2)
        }
        
        try:
            res = backtest(config, routes, data_routes, candles_dict, hyperparameters=hps)
            m = res['metrics']
            results.append({
                'ID': f"VARIACION_{i:03d}",
                'FAST_EMA': hps['fast_ema'],
                'SLOW_EMA': hps['slow_ema'],
                'SL_PCT': hps['stop_loss_pct'],
                'ROI': round(m['net_profit_percentage'], 2),
                'TRADES': m['total'],
                'WIN_RATE': round(m['win_rate'] * 100, 2)
            })
            if i % 25 == 0: print(f"Procesado: {i}/200...")
        except:
            continue

    # Generar Ranking Real
    ranking = pd.DataFrame(results).sort_values(by='ROI', ascending=False)
    ranking.to_csv('AUDITORIA_VERDADERA_BTC_200.csv', index=False)
    
    print("\n✅ RANKING CERTIFICADO:")
    print(ranking.head(10).to_string(index=False))

if __name__ == "__main__":
    run_true_varied_audit()
