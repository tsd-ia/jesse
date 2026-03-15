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
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, open, high, low, close, volume FROM Candle WHERE symbol=? AND timestamp>=? AND timestamp<=?", (symbol, start, finish))
    rows = cursor.fetchall()
    conn.close()
    return np.array([[float(r[0]), float(r[1]), float(r[4]), float(r[2]), float(r[3]), float(r[5])] for r in rows])

def run_detailed_report():
    print("💎 GENERANDO REPORTE ULTRA-DETALLADO ORO 2026 ($500 USD)")
    
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    start_date = '2026-03-01'
    finish_date = '2026-03-14'
    
    start_ts = jh.date_to_timestamp(start_date)
    finish_ts = jh.date_to_timestamp(finish_date)
    
    all_candles = load_data(symbol, start_ts, finish_ts)
    if len(all_candles) < 300:
        print("Error: No hay suficientes velas.")
        return
        
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[240:]}}
    warmup_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[:240]}}
    
    strategies = ['GoldMasterGrid', 'LiquidityHunter2026', 'Antigravity_Beast']
    
    all_trade_logs = []
    summary_results = []
    
    for s_name in strategies:
        print(f"[*] Analizando {s_name}...")
        config = {
            'starting_balance': 500,
            'fee': 0.0004,
            'type': 'futures',
            'futures_leverage': 50,
            'futures_leverage_mode': 'cross',
            'exchange': exchange,
            'warm_up_candles': 240
        }
        
        try:
            res = backtest(config, [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': s_name}], 
                           [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                           candles=candles_dict, warmup_candles=warmup_dict)
            
            m = res['metrics']
            trades = res.get('trades', [])
            
            summary_results.append({
                'Estrategia': s_name,
                'ROI': f"{m.get('net_profit_percentage', 0):.2f}%",
                'WinRate': f"{m.get('win_rate', 0)*100:.2f}%",
                'Trades': len(trades),
                'MaxDD': f"{m.get('max_drawdown', 0):.2f}%"
            })
            
            # LOG DE TRADES ROBUSTO (Maneja Objeto o Dict)
            for t in trades:
                try:
                    # En Jesse Research, t puede ser un objeto ClosedTrade o un dict
                    entry = getattr(t, 'entry_price', t.get('entry_price', 0)) if not isinstance(t, dict) else t.get('entry_price', 0)
                    exit_p = getattr(t, 'exit_price', t.get('exit_price', 0)) if not isinstance(t, dict) else t.get('exit_price', 0)
                    pnl = getattr(t, 'pnl', t.get('PNL', 0)) if not isinstance(t, dict) else t.get('PNL', 0)
                    
                    all_trade_logs.append({
                        'Strategy': s_name,
                        'Entry': entry,
                        'Exit': exit_p,
                        'PnL': pnl,
                        'Type': getattr(t, 'type', t.get('type', 'unknown')) if not isinstance(t, dict) else t.get('type', 'unknown')
                    })
                except:
                    pass
        except Exception as e:
            print(f"Error en {s_name}: {e}")

    # Guardar archivos
    pd.DataFrame(summary_results).to_csv('INFORME_EJECUTIVO_ORO_2026.csv', index=False)
    pd.DataFrame(all_trade_logs).to_csv('DETALLE_TRADES_TOTAL_2026.csv', index=False)
    
    print("\n✅ REPORTE GENERADO.")
    print(f"- Resumen: INFORME_EJECUTIVO_ORO_2026.csv ({len(summary_results)} estrategias)")
    print(f"- Detalle: DETALLE_TRADES_TOTAL_2026.csv ({len(all_trade_logs)} trades)")

if __name__ == "__main__":
    run_detailed_report()
