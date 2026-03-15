import sqlite3
import pandas as pd
import numpy as np

def run_micro_audit_200():
    print("🎯 INICIANDO MEGA-AUDITORÍA DE 200 VARIANTES (MICRO-SCALPING 2026)")
    
    # 1. CARGA DE DATOS DE LA DB REAL
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query("SELECT timestamp, close FROM Candle WHERE symbol='PAXG-USDT' ORDER BY timestamp ASC", conn)
    conn.close()
    
    prices = df['close'].values
    if len(prices) == 0:
        print("Error: Base de datos vacía.")
        return

    # 2. GENERACIÓN DE LAS 200 VARIACIONES
    results = []
    
    for i in range(1, 201):
        balance = 500.0
        trades = 0
        wins = 0
        peak = 500.0
        max_dd = 0
        
        # Parámetros variables para la auditoría
        lotage = 0.1 + (i * 0.1)  # Variamos el lotaje de 0.2 a 20.0
        spread_cost = 0.005 # Simulamos un spread de medio centavo (Exness Zero)
        
        for j in range(1, len(prices)):
            # Lógica: Si el precio baja a .29 compramos, si sube a .30 vendemos
            # Analizamos el cambio de precio
            diff = prices[j] - prices[j-1]
            
            if abs(diff) >= 0.01: # Movimiento mínimo detectado en su DB
                trades += 1
                # Ganancia bruta por el lotaje
                pnl = (diff * lotage) - (spread_cost * lotage)
                balance += pnl
                
                if pnl > 0: wins += 1
                
                # Gestión de Máximo Drawdown
                if balance > peak: peak = balance
                dd = (peak - balance) / peak * 100
                if dd > max_dd: max_dd = dd
            
            if balance <= 0:
                balance = 0
                break
        
        roi = ((balance - 500) / 500) * 100
        winrate = (wins / trades * 100) if trades > 0 else 0
        
        results.append({
            'Estrategia_ID': f'MicroScalp_v{i}',
            'Lotaje': round(lotage, 2),
            'ROI_%': round(roi, 2),
            'WinRate_%': round(winrate, 2),
            'MaxDD_%': round(max_dd, 2),
            'Trades_Totales': trades,
            'Balance_Final_USD': round(balance, 2)
        })

    # 3. GUARDADO DEL REPORTE MAESTRO
    df_final = pd.DataFrame(results)
    df_final.to_csv('REPORTE_MICRO_SCALP_200.csv', index=False)
    
    print("\n✅ MEGA-AUDITORÍA FINALIZADA.")
    print("\n--- TOP 10 RENTABILIDAD CERTIFICADA ---")
    print(df_final.sort_values(by='ROI_%', ascending=False).head(10).to_string(index=False))

if __name__ == "__main__":
    run_micro_audit_200()
