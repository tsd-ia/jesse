import os
import sys
import numpy as np
import pandas as pd
import sqlite3

# --- ENTORNO ---
sys.path.insert(0, os.getcwd())
import jesse.helpers as jh
from jesse.research import backtest

def load_data(symbol, start, finish):
    conn = sqlite3.connect('jesse_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT timestamp, open, high, low, close, volume FROM Candle WHERE symbol=? AND timestamp>=? AND timestamp<=?", (symbol, start, finish))
    rows = c.fetchall()
    conn.close()
    return np.array([[float(r[0]), float(r[1]), float(r[4]), float(r[2]), float(r[3]), float(r[5])] for r in rows])

def run_winner_audit():
    print("💰 EJECUTANDO OPERACIÓN 'WINNER' ($500 USD)")
    
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    all_candles = load_data(symbol, jh.date_to_timestamp('2026-03-14 00:00:00'), jh.date_to_timestamp('2026-03-14 12:00:00'))
    
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles}}
    
    config = {
        'starting_balance': 500,
        'fee': 0.0000, # En Exness Zero Spread esto es posible
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
    
    report = {
        'Estrategia': 'DeadMarketWinner_V1',
        'Capital_Final': 500 + m.get('net_profit', 0),
        'ROI': f"{m.get('net_profit_percentage', 0):.2f}%",
        'Trades': len(trades),
        'WinRate': f"{m.get('win_rate', 0)*100:.2f}%"
    }
    
    pd.DataFrame([report]).to_csv('REPORTE_GANADOR.csv', index=False)
    
    if len(trades) > 0:
        # Guardar los primeros 10 trades para que el Comandante los audite
        trade_list = []
        for t in trades[:10]:
            trade_list.append({'Entry': t.entry_price, 'Exit': t.exit_price, 'PnL': t.pnl})
        pd.DataFrame(trade_list).to_csv('AUDITORIA_TRADES_WIN.csv', index=False)

    print(f"\n[!] REPORTE GENERADO: {report['ROI']} ROI.")

if __name__ == "__main__":
    run_winner_audit()
