import pandas as pd
import sqlite3

def run_hft_1000_audit():
    print("🩸 INICIANDO AUDITORÍA TITÁN HFT (BÚSQUEDA DE 1000 TRADES/DÍA)")
    
    conn = sqlite3.connect('jesse_db.sqlite')
    # Cargamos marzo 2026 completo
    df = pd.read_sql_query("SELECT close FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    if df.empty:
        print("❌ Error: No hay velas en la DB.")
        return

    prices = df['close'].values
    results = []
    
    # Probaremos con 200 variaciones de sensibilidad extrema
    for i in range(200):
        # Gatillo desde $0.05 hasta $10.00 USD
        trigger = 0.05 + (i * 0.05)
        balance = 500.0
        trades_count = 0
        fee_rate = 0.0004 # 0.04% Binance Fee
        
        for j in range(1, len(prices)):
            price_change = abs(prices[j] - prices[j-1])
            
            if price_change > trigger:
                trades_count += 1
                # Simulación de un trade HFT instantáneo
                # Costo de comisión (apertura + cierre) sobre volumen de 50x
                costo_comision = (prices[j] * 0.5) * (fee_rate * 2) 
                balance -= costo_comision
                
                if balance <= 0:
                    balance = 0
                    break
        
        results.append({
            'ID': f"TITAN_HFT_{i:03d}",
            'GATILLO_USD': trigger,
            'TOTAL_TRADES': trades_count,
            'TRADES_DIA': round(trades_count / 14, 1),
            'ROI_FINAL': round(((balance - 500.0) / 500.0) * 100, 2),
            'EQUITY': round(balance, 2)
        })

    ranking = pd.DataFrame(results).sort_values(by='TOTAL_TRADES', ascending=False)
    ranking.to_csv('REPORT_TITAN_HFT_2026.csv', index=False)
    
    print("\n✅ REPORTE HFT GENERADO (CERTIFICADO):")
    print(ranking.head(10).to_string(index=False))

if __name__ == "__main__":
    run_hft_1000_audit()
