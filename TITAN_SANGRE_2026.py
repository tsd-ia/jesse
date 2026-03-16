import pandas as pd
import sqlite3

def run_brutal_hft_audit():
    print("🩸 INICIANDO AUDITORÍA TITAN SANGRE (SISTEMA HFT PURO)")
    
    conn = sqlite3.connect('jesse_db.sqlite')
    # Cargamos 10 días de data (14,400 minutos)
    df = pd.read_sql_query("SELECT close FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    prices = df['close'].values
    results = []
    commission = 0.0004 # 0.04% taker fee

    for i in range(200):
        # Cada bot tiene una sensibilidad distinta, pero todas extremas ($0.1 a $10.0)
        sensitivity = 0.1 + (i * 0.1) 
        balance = 500.0
        trades_count = 0
        current_pos = 0 # 0: neutro, 1: long, -1: short
        
        for j in range(1, len(prices)):
            price_change = prices[j] - prices[j-1]
            
            # Si el precio se mueve más que la sensibilidad -> TRADEO
            if abs(price_change) > sensitivity:
                trades_count += 1
                # Simulación de un trade HFT rápido: Ganancia o pérdida por el movimiento
                # El balance sufre la comisión de entrar y salir (2 x 0.04%)
                balance -= (balance * 50) * (commission * 2) # 50x leverage cost
                if price_change > 0: balance += price_change * 0.1 # Ganancia proporcional
                else: balance -= abs(price_change) * 0.1
                
                if balance <= 0:
                    balance = 0
                    break
        
        results.append({
            'ID': f"TITAN_{i:03d}",
            'MOV_GATILLO_USD': sensitivity,
            'TOTAL_TRADES': trades_count,
            'TRADES_DIA': round(trades_count / 10, 1),
            'ROI_FINAL': round(((balance - 500) / 500) * 100, 2),
            'EQUITY': round(balance, 2)
        })

    final_df = pd.DataFrame(results).sort_values(by='TOTAL_TRADES', ascending=False)
    final_df.to_csv('REPORTE_GUERRA_MAESTRO_2026.csv', index=False)
    
    print("\n✅ REPORTE HFT GENERADO CON ÉXITO:")
    print(final_df.head(10).to_string(index=False))

if __name__ == "__main__":
    run_brutal_hft_audit()
