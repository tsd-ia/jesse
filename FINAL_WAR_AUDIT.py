import os
import sys
import pandas as pd
import sqlite3
import numpy as np

# Entorno Jesse
sys.path.insert(0, os.getcwd())
from jesse.research import backtest
from jesse.services.selector import get_strategy_class

def run_certified_research():
    print("🔥 ATAQUE FINAL: MOTOR JESSE RESEARCH (ORO 1m)")
    
    # 1. Extraer velas reales de la DB para marzo 2026
    conn = sqlite3.connect('jesse_db.sqlite')
    query = """
    SELECT timestamp, open, high, low, close, volume 
    FROM Candle 
    WHERE symbol='PAXG-USDT' 
    AND exchange='Binance Perpetual Futures'
    AND timestamp >= 1772323200000 
    ORDER BY timestamp ASC
    """
    df_candles = pd.read_sql_query(query, conn)
    conn.close()

    if df_candles.empty:
        print("❌ Error: No hay velas en el rango solicitado.")
        return

    # Convertir a formato numpy que Jesse entiende (M1)
    candles = df_candles.values
    print(f"Cargadas {len(candles)} velas de Oro.")

    # 2. Configuración de la cuenta
    config = {
        'starting_balance': 500,
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 50,
        'futures_leverage_mode': 'cross',
        'exchange': 'Binance Perpetual Futures',
        'warm_up_candles': 210
    }

    routes = [
        {'exchange': 'Binance Perpetual Futures', 'symbol': 'PAXG-USDT', 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}
    ]
    
    extra_candles = [
        {'exchange': 'Binance Perpetual Futures', 'symbol': 'PAXG-USDT', 'timeframe': '1m'}
    ]

    # 3. Disparar el Backtest de verdad
    try:
        # En Research Mode, pasamos las velas en un diccionario mapeado
        full_candles = {
            ('Binance Perpetual Futures', 'PAXG-USDT'): candles
        }
        
        res = backtest(config, routes, extra_candles, candles=full_candles)
        
        m = res['metrics']
        t = res['trades']
        
        print("\n✅ RESULTADO OBTENIDO:")
        print(f"TRADES: {len(t)}")
        print(f"ROI: {m['net_profit_percentage']}%")
        print(f"WIN RATE: {m['win_rate'] * 100}%")
        print(f"MAX DRAWDOWN: {m['max_drawdown']}%")

        # Guardar resultados
        pd.DataFrame(t).to_csv('REPORTE_GUERRA_MAESTRO_ORO_2026.csv', index=False)
        print("\nReporte generado: REPORTE_GUERRA_MAESTRO_ORO_2026.csv")

    except Exception as e:
        print(f"❌ Error en ejecución: {e}")

if __name__ == "__main__":
    run_certified_research()
