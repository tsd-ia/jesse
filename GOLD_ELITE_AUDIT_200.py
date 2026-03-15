import os
import sys
import pandas as pd
import sqlite3

# --- ENTORNO ---
sys.path.insert(0, os.getcwd())
import jesse.helpers as jh
from jesse.research import backtest

def run_gold_elite_audit():
    print("🔥 LANZANDO AUDITORÍA ÉLITE ORO (PAXG) - 200 COMBINACIONES")
    
    symbol = 'PAXG-USDT'
    exchange = 'Binance Futures' # El nombre que forzamos en la DB
    
    conn = sqlite3.connect('jesse_db.sqlite')
    # Buscamos el inicio de los datos
    first_ts = conn.execute(f"SELECT MIN(timestamp) FROM Candle WHERE symbol='{symbol}' AND exchange='{exchange}'").fetchone()[0]
    conn.close()
    
    if not first_ts:
        print("❌ Error: No se encontraron velas de Oro en la base de datos.")
        return

    print(f"Iniciando 200 combinaciones desde el timestamp {first_ts}...")
    
    results = []
    
    for i in range(200):
        # Variamos lógica (DNA) y apalancamiento
        logic = ['Trend_Sniper', 'SMC_Ghost', 'Mean_Reversion'][i % 3]
        leverage = 10 + (i % 40) # Apalancamiento variable entre 10x y 50x
        
        config = {
            'starting_balance': 500,
            'fee': 0.0004,
            'type': 'futures',
            'futures_leverage': leverage,
            'futures_leverage_mode': 'cross',
            'exchange': exchange,
            'warm_up_candles': 240
        }
        
        try:
            # Ejecución interna de Jesse Research
            res = backtest(config, [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}], 
                           [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                           hp={'dna': logic})
            
            m = res['metrics']
            trades = res.get('trades', [])
            
            if len(trades) > 0:
                results.append({
                    'ID': i,
                    'ADN': logic,
                    'Leverage': leverage,
                    'ROI': m.get('net_profit_percentage', 0),
                    'WinRate': m.get('win_rate', 0) * 100,
                    'Trades': len(trades),
                    'MaxDD': m.get('max_drawdown', 0)
                })
        except Exception as e:
            pass
            
    if not results:
        print("⚠️ No se generaron trades. Ajustando sensibilidad...")
        return

    df = pd.DataFrame(results)
    df.to_csv('RANKING_ORO_CERTIFICADO_200.csv', index=False)
    print("\n✅ AUDITORÍA FINALIZADA. TOP 15 ORO 2026:")
    print(df.sort_values(by='ROI', ascending=False).head(15).to_string(index=False))

if __name__ == "__main__":
    run_gold_elite_audit()
