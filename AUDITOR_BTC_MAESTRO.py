import os
import sys
import pandas as pd
import sqlite3
import numpy as np

# Inyectamos el entorno para que Jesse encuentre sus estrategias
sys.path.insert(0, os.getcwd())

from jesse.research import backtest
import jesse.helpers as jh

def run_200_audit_jesse_engine():
    print("🔥 INICIANDO AUDITORÍA REAL: MOTOR JESSE v2026")
    
    # 1. Cargar Velas de BTC desde la base de datos
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query("SELECT timestamp, open, high, low, close, volume FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    if df.empty:
        print("❌ Error: No se encontraron velas de BTC.")
        return

    # Formato Jesse: array de numpy [timestamp, open, high, low, close, volume]
    candles_np = df.values
    print(f"Cargadas {len(candles_np)} velas reales.")

    # 2. Configuración siguiendo la firma de jesse/research/backtest.py
    exchange_name = 'Binance Perpetual Futures'
    symbol = 'BTC-USDT'
    
    config = {
        'starting_balance': 500,
        'fee': 0.0004, # Comisión real de Binance
        'type': 'futures',
        'futures_leverage': 50,
        'futures_leverage_mode': 'cross',
        'exchange': exchange_name,
        'warm_up_candles': 210
    }

    # Ruta de ejecución
    routes = [{
        'exchange': exchange_name,
        'symbol': symbol,
        'timeframe': '1m',
        'strategy': 'MasterWarrior2026'
    }]

    # Rutas de datos (Obligatorio en v2026)
    data_routes = [{
        'exchange': exchange_name,
        'symbol': symbol,
        'timeframe': '1m'
    }]

    # Diccionario de velas corregido para la API v2026
    # La clave suele ser {exchange}-{symbol} o lo que jh.key genere
    candles_dict = {
        jh.key(exchange_name, symbol): {
            'exchange': exchange_name,
            'symbol': symbol,
            'candles': candles_np
        }
    }

    results = []
    
    # 3. Bombardeo de 200 Variaciones via Hiperparámetros
    for i in range(200):
        # Generamos un set de hiperparámetros distinto por cada bot
        hps = {
            'dna': f'BOT_MODEL_{i:03d}',
            'sensitivity': 1.0 + (i * 0.1)
        }
        
        try:
            # Ejecutamos el motor de Jesse REAL
            res = backtest(
                config, 
                routes, 
                data_routes, 
                candles_dict, 
                hyperparameters=hps,
                generate_logs=False 
            )
            
            m = res['metrics']
            results.append({
                'BOT_ID': f"BTC_{i:03d}",
                'ROI': round(m['net_profit_percentage'], 2),
                'TRADES': m['total'],
                'WIN_RATE': round(m['win_rate'] * 100, 2)
            })
            
            if i % 20 == 0:
                print(f"Auditado bot {i}/200...")

        except Exception as e:
            # Si un bot falla, reportamos el error técnico real
            results.append({'BOT_ID': f"BTC_{i:03d}", 'ROI': 0, 'ERROR': str(e)})

    # 4. Generar el Ranking Legítimo
    ranking_df = pd.DataFrame(results).sort_values(by='ROI', ascending=False)
    ranking_df.to_csv('RANKING_REAL_BTC_2026.csv', index=False)
    
    print("\n✅ AUDITORÍA FINALIZADA. TOP 10 (DATOS REALES):")
    print(ranking_df.head(10).to_string(index=False))

if __name__ == "__main__":
    run_200_audit_jesse_engine()
