import sqlite3
conn = sqlite3.connect('jesse_db.sqlite')
cursor = conn.cursor()
cursor.execute("UPDATE Candle SET exchange = 'Binance Perpetual Futures'")
conn.commit()
conn.close()
print("DB: Todo sincronizado a 'Binance Perpetual Futures'")
