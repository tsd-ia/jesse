import sqlite3

def fix():
    conn = sqlite3.connect('jesse_db.sqlite')
    c = conn.cursor()
    
    print("--- ANTES ---")
    c.execute("SELECT exchange, symbol, count(*) FROM Candle GROUP BY exchange, symbol")
    print(c.fetchall())
    
    # 1. Asegurar que tenemos 'Binance Perpetual Futures'
    # Vamos a convertir TODO a este exchange para evitar confusiones
    c.execute("UPDATE Candle SET exchange = 'Binance Perpetual Futures'")
    
    # 2. Asegurar que el simbolo es PAXG-USDT (con guion)
    c.execute("UPDATE Candle SET symbol = 'PAXG-USDT' WHERE symbol LIKE '%PAXG%USDT%'")
    
    conn.commit()
    
    print("--- DESPUES ---")
    c.execute("SELECT exchange, symbol, count(*) FROM Candle GROUP BY exchange, symbol")
    print(c.fetchall())
    
    conn.close()

if __name__ == "__main__":
    fix()
