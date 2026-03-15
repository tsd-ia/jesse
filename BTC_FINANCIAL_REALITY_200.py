import pandas as pd
import numpy as np
import sqlite3

def run_rigorous_btc_audit():
    print("🛡️ INICIANDO AUDITORÍA DE RIGOR: BTC-USDT MARZO 2026")
    
    # 1. Cargar Velas Reales de BTC
    conn = sqlite3.connect('jesse_db.sqlite')
    query = "SELECT close FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        print("❌ Error: No se encontraron velas de BTC en la base de datos.")
        return

    prices = df['close'].values
    results = []
    commission_rate = 0.0004 # 0.04% por operación

    # 2. Simular 200 variaciones de sensibilidad (Gap de volatilidad)
    for i in range(200):
        # Cada bot tiene un umbral de entrada distinto
        threshold = 5 + (i * 2) # Sensibilidad de movimiento en USD
        balance = 500.0
        trades = 0
        current_pos = 0 # 0: neutro, 1: long, -1: short
        entry_price = 0
        
        for j in range(1, len(prices)):
            price = prices[j]
            prev_price = prices[j-1]
            change = price - prev_price
            
            # Lógica de entrada/cambio
            if current_pos == 0:
                if change > threshold: # Long
                    current_pos = 1
                    entry_price = price
                    balance -= (balance * 50) * commission_rate # 50x leverage fee
                    trades += 1
                elif change < -threshold: # Short
                    current_pos = -1
                    entry_price = price
                    balance -= (balance * 50) * commission_rate
                    trades += 1
            
            # Cierre de posición (Cruce de precio)
            elif (current_pos == 1 and change < -threshold/2) or (current_pos == -1 and change > threshold/2):
                profit = (price - entry_price) * (50 * balance / entry_price) * current_pos
                balance += profit
                balance -= (balance * 50) * commission_rate # Exit fee
                current_pos = 0
                
            if balance <= 0:
                balance = 0
                break
        
        roi = ((balance - 500) / 500) * 100
        results.append({
            'BOT_ID': f"BTC_RIGOR_{i:03d}",
            'UMBRAL_USD': threshold,
            'TRADES': trades,
            'ROI_FINAL': round(roi, 2),
            'EQUITY': round(balance, 2)
        })

    # 3. Guardar el Ranking Real
    ranking_df = pd.DataFrame(results).sort_values(by='ROI_FINAL', ascending=False)
    ranking_df.to_csv('AUDITORIA_REAL_BTC_2026.csv', index=False)
    
    print("\n✅ RANKING BTC GENERADO (CON COMISIONES REALES):")
    print(ranking_df.head(10).to_string(index=False))

if __name__ == "__main__":
    run_rigorous_btc_audit()
