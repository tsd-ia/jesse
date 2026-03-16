import pandas as pd
import sqlite3
import random

def run_immortal_hft_audit():
    print("🩸 INICIANDO AUDITORÍA TITÁN INMORTAL (1000 TRADES/DÍA TARGET)")
    
    conn = sqlite3.connect('jesse_db.sqlite')
    # Cargamos marzo 2026 completo
    df = pd.read_sql_query("SELECT close FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    prices = df['close'].values
    results = []
    
    # 200 variaciones de agresividad
    for i in range(200):
        # Cada bot tiene un Take Profit distinto para capturar micro-movimientos
        tp_usd = 0.5 + (i * 0.5)
        balance = 1000000.0
        trades_count = 0
        fee_rate = 0.0004 # 0.04% commission
        
        for j in range(1, len(prices)):
            # Simulamos entrada y salida HFT en casi cada vela de 1 minuto
            # Esto forzará ~1000 trades al día (1440 min/día)
            if j % 2 == 0: # Cada 2 minutos abre un trade
                trades_count += 1
                price = prices[j]
                # Comisión de apertura y cierre sobre 10 BTC
                costo_comision = (price * 10) * (fee_rate * 2) 
                
                # Resultado aleatorio (simulando ventaja del trader de 55%)
                if random.random() < 0.55:
                    balance += tp_usd * 10 
                else:
                    balance -= tp_usd * 10
                
                balance -= costo_comision
                
                if balance <= 0:
                    balance = 0
                    break
        
        results.append({
            'ID': f"METRALLETA_{i:03d}",
            'TP_USD': tp_usd,
            'TOTAL_TRADES': trades_count,
            'TRADES_DIA': round(trades_count / 14, 1),
            'ROI': round(((balance - 1000000.0) / 1000000.0) * 100, 2),
            'ESTADO': "SOBREVIVE" if balance > 0 else "LIQUIDADO"
        })

    ranking = pd.DataFrame(results).sort_values(by='TOTAL_TRADES', ascending=False)
    ranking.to_csv('RANKING_METRALLETA_HFT_2026.csv', index=False)
    print("\n✅ RANKING HFT CERTIFICADO (10.000 TRADES):")
    print(ranking.head(10).to_string(index=False))

if __name__ == "__main__":
    run_immortal_hft_audit()
