import os
import sys
import pandas as pd
import sqlite3

# Entorno Jesse
sys.path.insert(0, os.getcwd())
from jesse.research import backtest

def run_official_audit():
    print("🚀 AUDITORÍA OFICIAL JESSE ENGINE (ORO 2026)")
    
    # Cargar velas
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query("SELECT * FROM Candle WHERE symbol='PAXG-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    # Configuración Real
    config = {
        'starting_balance': 500,
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 50,
        'exchange': 'Binance Perpetual Futures',
        'warm_up_candles': 210
    }

    routes = [
        {'exchange': 'Binance Perpetual Futures', 'symbol': 'PAXG-USDT', 'timeframe': '1m', 'strategy': 'GoldWarriorFINAL'}
    ]
    
    try:
        res = backtest(config, routes, candles={('Binance Perpetual Futures', 'PAXG-USDT'): df.values})
        m = res['metrics']
        t = res['trades']
        
        print("\n✅ RESULTADO OFICIAL OBTENIDO:")
        print(f"Total Trades: {len(t)}")
        print(f"Net Profit: {m['net_profit_percentage']}%")
        print(f"Win Rate: {m['win_rate'] * 100}%")
        
        # Guardar el ranking oficial
        pd.DataFrame(t).to_csv('RANKING_REAL_JESSE_2026.csv', index=False)
        print("Reporte generado: RANKING_REAL_JESSE_2026.csv")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_official_audit()
