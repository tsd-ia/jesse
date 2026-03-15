import sqlite3
import pandas as pd
import numpy as np
import random

def run_reconquista_audit():
    print("🔥 LANZANDO AUDITORÍA DE RECONQUISTA (200 ESTRATEGIAS DIVERSIFICADAS)")
    
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query("SELECT timestamp, close, high, low FROM Candle WHERE symbol='PAXG-USDT' ORDER BY timestamp ASC", conn)
    conn.close()
    
    prices = df['close'].values
    if len(prices) == 0: return

    results = []
    logics = ['SMC_Institutional', 'Trend_Sniper', 'Mean_Reversion', 'Dynamic_Grid']

    for i in range(1, 201):
        logic_base = logics[i % 4]
        balance = 500.0
        trades = 0
        wins = 0
        peak = 500.0
        max_dd = 0
        
        # Parámetros por ADN
        risk_multiplier = random.uniform(0.5, 5.0)
        tp_ratio = random.uniform(1.5, 3.0)
        
        for j in range(20, len(prices)):
            # Simulación de lógica simplificada
            entry = False
            pnl_move = 0
            
            if logic_base == 'SMC_Institutional': # Entra en retrocesos profundos
                if prices[j] < np.mean(prices[j-20:j]) * 0.9999: 
                    entry = True
                    pnl_move = (prices[min(j+10, len(prices)-1)] - prices[j])
            
            elif logic_base == 'Trend_Sniper': # Rompimientos de volatilidad
                if abs(prices[j] - prices[j-1]) > 0.05:
                    entry = True
                    pnl_move = (prices[min(j+5, len(prices)-1)] - prices[j]) if prices[j] > prices[j-1] else (prices[j] - prices[min(j+5, len(prices)-1)])

            if entry:
                trades += 1
                trade_pnl = (pnl_move * 10 * risk_multiplier) - 0.01 # PNL menos spread
                balance += trade_pnl
                if trade_pnl > 0: wins += 1
                if balance > peak: peak = balance
                dd = (peak - balance) / peak * 100
                if dd > max_dd: max_dd = dd
            
            if balance <= 0:
                balance = 0
                break
        
        roi = ((balance - 500) / 500) * 100
        winrate = (wins / trades * 100) if trades > 0 else 0
        
        results.append({
            'ID': i,
            'Estrategia': f'{logic_base}_v{i}',
            'Logica': logic_base,
            'ROI_%': round(roi, 2),
            'WinRate_%': round(winrate, 2),
            'MaxDD_%': round(max_dd, 2),
            'Trades': trades,
            'Final_USD': round(balance, 2)
        })

    df_res = pd.DataFrame(results)
    df_res.to_csv('REPORTE_RECONQUISTA_200.csv', index=False)
    print("✅ Auditoría completada. Reporte: REPORTE_RECONQUISTA_200.csv")

if __name__ == "__main__":
    run_reconquista_audit()
