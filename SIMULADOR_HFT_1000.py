import pandas as pd
import sqlite3
import random

def run_titan_hft_1000_trades():
    print("🩸 INICIANDO SIMULACIÓN TITÁN HFT (1000 TRADES/DÍA TARGET)")
    
    conn = sqlite3.connect('jesse_db.sqlite')
    # Cargamos marzo 2026 completo de BTC
    df = pd.read_sql_query("SELECT close FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    if df.empty:
        print("❌ Error: No hay munición (velas).")
        return

    prices = df['close'].values
    results = []
    # Balance de $1M para no morir por comisiones y ver la frecuencia real
    initial_balance = 1000000.0
    fee_rate = 0.0004 # 0.04% Binance Taker
    
    for i in range(200):
        # Gatillos ultra-sensibles para forzar HFT ($1 a $10 USD de movimiento en BTC)
        trigger = 0.5 + (i * 0.5)
        balance = initial_balance
        trades_count = 0
        total_pnl = 0
        
        for j in range(1, len(prices)):
            price_change = abs(prices[j] - prices[j-1])
            
            if price_change > trigger:
                trades_count += 1
                # Simulación de un trade HFT rápido
                # Comisión de apertura y cierre (0.04% * 2) sobre 1 BTC
                fee_cost = (prices[j] * 1.0) * (fee_rate * 2)
                # Resultado aleatorio 51/49 (ventaja mínima)
                win = random.random() < 0.51
                pnl = (price_change * 1.0) if win else (-price_change * 1.0)
                
                balance += (pnl - fee_cost)
                
                if balance <= 0:
                    balance = 0
                    break
        
        results.append({
            'ID': f"TITAN_{i:03d}",
            'DISPARO_USD': trigger,
            'TOTAL_TRADES': trades_count,
            'TRADES_DIA': round(trades_count / 14, 1), # ~14 días de data
            'ROI_FINAL': round(((balance - initial_balance) / initial_balance) * 100, 2),
            'ESTADO': "SOBREVIVE" if balance > 0 else "LIQUIDADO"
        })

    ranking = pd.DataFrame(results).sort_values(by='TOTAL_TRADES', ascending=False)
    ranking.to_csv('REPORT_HFT_1000_REAL.csv', index=False)
    
    print("\n✅ RANKING HFT GENERADO (AMETRALLADORA):")
    print(ranking.head(10).to_string(index=False))

if __name__ == "__main__":
    run_titan_hft_1000_trades()
