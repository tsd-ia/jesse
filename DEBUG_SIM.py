import os
import sys
import numpy as np
import pandas as pd
import sqlite3

# --- ENTORNO ---
sys.path.insert(0, os.getcwd())
import jesse.helpers as jh
from jesse.research import backtest

def load_data():
    conn = sqlite3.connect('jesse_db.sqlite')
    # Cargamos 1000 velas para probar rapido
    df = pd.read_sql_query("SELECT timestamp, open, close, high, low, volume FROM Candle WHERE symbol='PAXG-USDT' ORDER BY timestamp ASC LIMIT 1000", conn)
    conn.close()
    return df.values

def debug_one_backtest():
    print("🛠 DEBUG: Probando 1 simulación de MasterWarrior2026")
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    all_candles = load_data()
    
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[240:]}}
    warmup_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[:240]}}

    config = {
        'starting_balance': 500,
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 50,
        'futures_leverage_mode': 'cross',
        'exchange': exchange,
        'warm_up_candles': 240
    }
    
    hps = {'dna': 'SMC_Ghost', 'risk': 0.1, 'tp': 50, 'sl': 20}
    
    # SIN TRY-EXCEPT PARA VER EL ERROR REAL
    res = backtest(config, [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}], 
                   [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                   candles=candles_dict, warmup_candles=warmup_dict, hyperparameters=hps)
    
    print("¡Éxito! trades:", len(res['trades']))

if __name__ == "__main__":
    debug_one_backtest()
