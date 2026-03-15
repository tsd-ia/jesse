import os
import sys
import numpy as np
import pandas as pd
import sqlite3

# --- ENTORNO ---
sys.path.insert(0, os.getcwd())
import jesse.helpers as jh
from jesse.research import backtest

def load_data(symbol):
    conn = sqlite3.connect('jesse_db.sqlite')
    c = conn.cursor()
    # Cargamos un bloque solido de velas
    c.execute("SELECT timestamp, open, high, low, close, volume FROM Candle WHERE symbol=? ORDER BY timestamp DESC LIMIT 720", (symbol,))
    rows = c.fetchall()
    conn.close()
    # Invertimos para que esten cronologicas
    rows = rows[::-1]
    return np.array([[float(r[0]), float(r[1]), float(r[4]), float(r[2]), float(r[3]), float(r[5])] for r in rows])

def run_final_audit():
    print("💎 CULMINANDO AUDITORÍA GANADORA ($500 USD)")
    
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    all_candles = load_data(symbol)
    
    if len(all_candles) < 2:
        print("Error: No hay datos suficientes.")
        return

    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles}}
    
    config = {
        'starting_balance': 500,
        'fee': 0.0000,
        'type': 'futures',
        'futures_leverage': 500,
        'futures_leverage_mode': 'cross',
        'exchange': exchange,
        'warm_up_candles': 0
    }
    
    res = backtest(config, [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'DeadMarketWinner'}], 
                   [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                   candles=candles_dict)
    
    m = res['metrics']
    trades = res.get('trades', [])
    
    # SALVAR REPORTE REAL (LEEREMOS ESTO PARA NO MENTIR)
    pd.DataFrame([{
        'Estrategia': 'DeadMarketWinner_FINAL',
        'Profit_USD': m.get('net_profit', 0),
        'ROI': f"{m.get('net_profit_percentage', 0):.2f}%",
        'Trades': len(trades),
        'WinRate': f"{m.get('win_rate', 0)*100:.2f}%"
    }]).to_csv('ULTIMO_REPORTE_REAL.csv', index=False)
    
    print(f"\n[!] PROCESO COMPLETADO. Trades: {len(trades)}")

if __name__ == "__main__":
    run_final_audit()
