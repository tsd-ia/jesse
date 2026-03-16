import pandas as pd
import sqlite3

def run_vampire_1000_audit():
    print("🩸 OPERACIÓN VAMPIRO: GENERANDO 1000 TRADES DIARIOS")
    
    conn = sqlite3.connect('jesse_db.sqlite')
    # Cargamos 10 días de marzo 2026
    df = pd.read_sql_query("SELECT close, open FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    if df.empty:
        print("❌ Error: No hay velas.")
        return

    prices = df['close'].values
    opens = df['open'].values
    results = []
    
    # Balance de $10,000 para soportar la ráfaga
    balance = 10000.0
    trades_count = 0
    fee = 0.0004 # 0.04% fee
    
    trades_log = []

    for i in range(len(prices)):
        # Condición HFT: El precio se movió más de $1 desde la apertura de la vela
        if abs(prices[i] - opens[i]) > 1.0:
            trades_count += 1
            # Costo operativo real por trade
            costo_fee = (prices[i] * 0.5) * (fee * 2) 
            balance -= costo_fee
            
            if trades_count % 1000 == 0:
                print(f"Alcanzados {trades_count} trades...")
            
            if balance <= 0:
                balance = 0
                break

    roi = ((balance - 10000.0) / 10000.0) * 100
    
    reporte = {
        'TOTAL_TRADES': trades_count,
        'TRADES_POR_DIA': round(trades_count / 14, 1),
        'BALANCE_FINAL': round(balance, 2),
        'ROI': round(roi, 2)
    }
    
    pd.DataFrame([reporte]).to_csv('REPORTE_TITAN_VAMPIRO_1000.csv', index=False)
    print("\n✅ REPORTE GENERADO:")
    print(reporte)

if __name__ == "__main__":
    run_vampire_1000_audit()
