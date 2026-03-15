import pandas as pd
import sqlite3

def run_titan_blood_audit():
    print("🩸 INICIANDO AUDITORÍA TITAN SANGRE (SISTEMA HFT PURO)")
    
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query("SELECT open, high, low, close FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000 LIMIT 14400", conn) # 10 días
    conn.close()
    
    results = []
    prices = df['close'].values
    commission = 0.0004 # 0.04% fee
    
    for i in range(200):
        # Cada bot tiene un umbral de disparo agresivo ($1 a $10 de movimiento)
        trigger = 1.0 + (i * 0.1)
        balance = 500.0
        trades_count = 0
        
        for j in range(1, len(prices)):
            price_change = abs(prices[j] - prices[j-1])
            if price_change > (trigger / 50): # Ajustado por apalancamiento
                trades_count += 1
                # Simulación de un trade HFT rápido
                # Ganancia/Pérdida promedio del 0.05% antes de comisiones
                resultado_neto = (prices[j] * 0.0005) - (prices[j] * commission * 2)
                balance += resultado_neto * 50 # 50x leverage
                
                if balance <= 0:
                    balance = 0
                    break
        
        results.append({
            'ID': f"TITAN_{i:03d}",
            'UMBRAL_GATILLO': trigger,
            'TOTAL_TRADES': trades_count,
            'TRADES_DIA': round(trades_count / 10, 1),
            'ROI_FINAL': round(((balance - 500) / 500) * 100, 2),
            'LIQUIDADO': "SÍ" if balance == 0 else "NO"
        })

    final_df = pd.DataFrame(results).sort_values(by='TOTAL_TRADES', ascending=False)
    final_df.to_csv('REPORTE_TITAN_SANGRE_2026.csv', index=False)
    
    print("\n✅ REPORTE HFT GENERADO (CERTIFICADO ANTIGRAVITY):")
    print(final_df.head(10).to_string(index=False))

if __name__ == "__main__":
    run_titan_blood_audit()
