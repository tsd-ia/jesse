import pandas as pd
import sqlite3

def run_honest_audit():
    print("🛡️ AUDITORÍA HONESTA: CÁLCULO REAL SOBRE VELAS DB")
    
    # 1. Velas Reales
    conn = sqlite3.connect('jesse_db.sqlite')
    df = pd.read_sql_query("SELECT open, high, low, close FROM Candle WHERE symbol='PAXG-USDT' AND timestamp >= 1772323200000", conn)
    conn.close()
    
    # 2. Lógica GoldWarrior (EMA 5/10)
    df['ema5'] = df['close'].rolling(5).mean()
    df['ema10'] = df['close'].rolling(10).mean()
    
    balance = 500
    fee = 0.0004 # 0.04% taker fee
    position = 0
    trades = []
    
    for i in range(10, len(df)):
        price = df.iloc[i]['close']
        ema5 = df.iloc[i]['ema5']
        ema10 = df.iloc[i]['ema10']
        
        # Entrada Long
        if position == 0 and ema5 > ema10:
            position = (balance * 50) / price # 50x leverage
            entry_price = price
            balance -= (balance * 50) * fee
            trades.append({'type': 'LONG', 'entry': price})
            
        # Salida Long / Entrada Short
        elif position > 0 and ema5 < ema10:
            profit = (price - entry_price) * position
            balance += profit
            balance -= (abs(profit) + (entry_price * position)) * fee
            position = 0
            trades[-1]['exit'] = price
            trades[-1]['profit'] = profit

    roi = ((balance - 500) / 500) * 100
    print(f"\n✅ AUDITORÍA FINALIZADA")
    print(f"Total Trades: {len(trades)}")
    print(f"Balance Final: ${balance:.2f}")
    print(f"ROI REAL: {roi:.2f}%")
    
    pd.DataFrame(trades).to_csv('RANKING_HONESTO_2026.csv', index=False)

if __name__ == "__main__":
    run_honest_audit()
