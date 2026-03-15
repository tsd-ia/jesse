import os
import sys
import pandas as pd
import sqlite3

# Entorno Jesse
sys.path.insert(0, os.getcwd())
from jesse.research import backtest

def run_atomic_audit():
    print("🚀 AUDITORÍA ATÓMICA ORO 2026")
    
    conn = sqlite3.connect('jesse_db.sqlite')
    query = "SELECT timestamp, open, high, low, close, volume FROM Candle WHERE symbol='PAXG-USDT' AND exchange='Binance Perpetual Futures' AND timestamp >= 1772323200000 ORDER BY timestamp ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print("❌ Sin velas.")
        return

    candles = df.values
    print(f"Cargadas {len(candles)} velas.")

    config = {
        'starting_balance': 500,
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 50,
        'exchange': 'Binance Perpetual Futures',
        'warm_up_candles': 210
    }

    # Definimos la ruta de forma manual y simple
    routes = [
        {'exchange': 'Binance Perpetual Futures', 'symbol': 'PAXG-USDT', 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}
    ]
    
    try:
        # Pasamos las velas directamente
        res = backtest(config, routes, candles={('Binance Perpetual Futures', 'PAXG-USDT'): candles})
        
        m = res['metrics']
        print(f"\n✅ RESULTADO:")
        print(f"TRADES: {len(res['trades'])}")
        print(f"ROI: {m['net_profit_percentage']}%")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_atomic_audit()
