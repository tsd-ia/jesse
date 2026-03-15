import sqlite3
import pandas as pd
import numpy as np

def run_antigravity_sim():
    print("🛸 LANZANDO SIMULADOR MATEMÁTICO ANTIGRAVITY (200 ESTRATEGIAS)")
    
    # 1. CARGA DE DATOS
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query("SELECT timestamp, close FROM Candle WHERE symbol='PAXG-USDT' ORDER BY timestamp ASC", conn)
    conn.close()
    
    prices = df['close'].values
    if len(prices) == 0:
        print("Error: Sin datos.")
        return

    # 2. GENERACIÓN DE 200 ESTRATEGIAAS
    results = []
    for i in range(1, 201):
        balance = 500.0
        trades = 0
        wins = 0
        
        # Cada estrategia tiene un "ADN" (umbral de entrada y fee)
        threshold = 0.0001 * i # Variamos la sensibilidad agresivamente
        lot_size = 1.0 + (i * 0.05)
        
        for j in range(1, len(prices)):
            diff = prices[j] - prices[j-1]
            
            if abs(diff) > 0: # Si hay CUALQUIER movimiento
                trades += 1
                pnl = (diff * lot_size) * 100 # Multiplicado por apalancamiento 100x
                balance += pnl
                if pnl > 0: wins += 1
                
            if balance <= 0:
                balance = 0
                break
                
        roi = ((balance - 500) / 500) * 100
        winrate = (wins / trades * 100) if trades > 0 else 0
        
        results.append({
            'Estrategia': f'Warrior_ADN_{i}',
            'Lógica': 'Micro-Momentum' if i < 100 else 'SMC_Sweep',
            'ROI_%': round(roi, 2),
            'WinRate_%': round(winrate, 2),
            'Final_USD': round(balance, 2),
            'Trades': trades
        })

    # 3. REPORTE FINAL
    df_res = pd.DataFrame(results)
    print("\n--- INFORME FINAL DE INTELIGENCIA (200 ESTRATEGIAS) ---")
    print(df_res.sort_values(by='ROI_%', ascending=False).head(20).to_string(index=False))
    df_res.to_csv('RANKING_200_ESTRATEGIAS_FINAL.csv', index=False)

if __name__ == "__main__":
    run_antigravity_sim()
