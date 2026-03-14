import sqlite3
conn = sqlite3.connect('jesse_db.sqlite')
cursor = conn.cursor()
# Cambiar todo a 'Binance Spot' para consistencia con el Dashboard
cursor.execute("UPDATE Candle SET exchange = 'Binance Spot'")
conn.commit()
conn.close()
print("DB: Todo sincronizado a 'Binance Spot'")
