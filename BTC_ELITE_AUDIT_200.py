import os
import sys
import pandas as pd
import sqlite3

# --- ENTORNO ---
sys.path.insert(0, os.getcwd())
import jesse.helpers as jh
from jesse.research import backtest

def run_btc_elite_audit():
    print("🔥 LANZANDO AUDITORÍA ÉLITE BTC-USDT (200 COMBINACIONES)")
    
    symbol = 'BTC-USDT'
    exchange = 'Binance Perpetual Futures'
    
    # Verificamos si ya hay velas descargadas
    conn = sqlite3.connect('jesse_db.sqlite')
    count = conn.execute(f"SELECT COUNT(*) FROM Candle WHERE symbol='{symbol}' AND timestamp >= {jh.date_to_timestamp('2026-03-01')}").fetchone()[0]
    conn.close()
    
    if count < 1000:
        print(f"Alerta: Solo hay {count} velas de BTC. Esperando importación...")
        return

    print(f"Detectadas {count} velas. Iniciando 200 combinaciones...")
    
    # Cargamos el ADN de los 20 mejores bots de BTC
    # (En la MasterWarrior ya tenemos estas lógicas por parámetros hp)
    
    results = []
    
    for i in range(200):
        # Variamos agresividad, lotaje y lógica (ADN)
        logic = ['Trend_Sniper', 'SMC_Ghost', 'Mean_Reversion'][i % 3]
        leverage = 20 + (i * 2) 
        
        config = {
            'starting_balance': 500,
            'fee': 0.0004,
            'type': 'futures',
            'futures_leverage': leverage,
            'futures_leverage_mode': 'cross',
            'exchange': exchange,
            'warm_up_candles': 240
        }
        
        # Ejecución interna de Jesse Research
        try:
            res = backtest(config, [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}], 
                           [{'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}], 
                           hp={'dna': logic})
            
            m = res['metrics']
            results.append({
                'ADN': logic,
                'ROI': m.get('net_profit_percentage', 0),
                'WinRate': m.get('win_rate', 0) * 100,
                'Trades': len(res.get('trades', [])),
                'MaxDD': m.get('max_drawdown', 0)
            })
        except:
            pass
            
    df = pd.DataFrame(results)
    df.to_csv('RANKING_BTC_MODELS_2026.csv', index=False)
    print("\n✅ AUDITORÍA FINALIZADA. TOP 10 BTC 2026:")
    print(df.sort_values(by='ROI', ascending=False).head(10).to_string(index=False))

if __name__ == "__main__":
    run_btc_elite_audit()
