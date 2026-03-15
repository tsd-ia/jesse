import os
import sys
import numpy as np
import pandas as pd
import sqlite3
import random

# Forzamos cargo manual de Jesse para evitar bloqueos
sys.path.insert(0, os.getcwd())
try:
    import jesse.helpers as jh
    from jesse.research import backtest
except ImportError:
    print("Error: No se pudo cargar Jesse. Verifique el entorno.")
    sys.exit()

def load_data(symbol):
    conn = sqlite3.connect('jesse_db.sqlite')
    # Cargamos solo los ultimos 10,000 minutos para que el reporte sea veloz pero detallado
    query = f"SELECT timestamp, open, high, low, close, volume FROM Candle WHERE symbol='{symbol}' ORDER BY timestamp DESC LIMIT 10000"
    df = pd.read_sql_query(query, conn)
    conn.close()
    # Jesse format: [timestamp, open, close, high, low, volume]
    return df.iloc[::-1][['timestamp', 'open', 'close', 'high', 'low', 'volume']].values

def run_world_audit():
    print("🌍 INICIANDO AUDITORÍA MUNDIAL DE 200 ESTRATEGIAS ($500 USD) - MODO STANDALONE")
    
    symbol = 'PAXG-USDT'
    exchange = 'Binance Perpetual Futures'
    all_candles = load_data(symbol)
    
    candles_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[240:]}}
    warmup_dict = {jh.key(exchange, symbol): {'exchange': exchange, 'symbol': symbol, 'candles': all_candles[:240]}}

    # ADN de los 20 mejores
    dnas = ['SMC_Ghost', 'London_Breakout', 'Grid_Venus', 'HFT_Velocity', 'Trend_Filter', 
            'Fibonacci_Level', 'OrderBlock_Mitigation', 'Psych_Numbers', 'Volume_POC', 'RSI_Divergence']
    
    results = []
    
    for i in range(200):
        current_dna = dnas[i % len(dnas)]
        current_risk = random.choice([0.01, 0.05, 0.1, 0.2, 0.5])
        
        config = {
            'starting_balance': 500,
            'fee': 0.0004,
            'type': 'futures',
            'futures_leverage': 50,
            'futures_leverage_mode': 'cross',
            'exchange': exchange,
            'warm_up_candles': 240
        }
        
        # Inyectamos el ADN via hiperparámetros
        hps = {'dna': current_dna, 'risk': current_risk, 'tp': random.randint(10, 100), 'sl': random.randint(5, 50)}
        
        try:
            res = backtest(config, 
                           [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}], 
                           [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                           candles=candles_dict, 
                           warmup_candles=warmup_dict, 
                           hyperparameters=hps)
            
            m = res['metrics']
            results.append({
                'ID': i + 1,
                'Style': current_dna,
                'Risk': f"{current_risk*100}%",
                'Trades': len(res.get('trades', [])),
                'WinRate': f"{m.get('win_rate', 0)*100:.2f}%",
                'ROI': f"{m.get('net_profit_percentage', 0):.2f}%",
                'MaxDD': f"{m.get('max_drawdown', 0):.2f}%"
            })
        except:
            pass
            
        if (i+1) % 20 == 0:
            print(f"[*] Reporte: {i+1}/200 concluidos.")

    df = pd.DataFrame(results)
    df.to_csv('RANKING_MUNDIAL_ORO_2026.csv', index=False)
    print("\n✅ MEGA-AUDITORÍA FINALIZADA. Archivo: RANKING_MUNDIAL_ORO_2026.csv")

if __name__ == "__main__":
    run_world_audit()
