import sqlite3
import datetime

conn = sqlite3.connect('jesse_db.sqlite')
c = conn.cursor()
c.execute('SELECT timestamp, open, close, high, low, volume FROM candle WHERE symbol="PAXG-USDT" ORDER BY timestamp DESC LIMIT 20')
rows = c.fetchall()
print("Últimas 20 velas de PAXG-USDT en DB:")
for r in rows:
    dt = datetime.datetime.fromtimestamp(r[0]/1000)
    print(f"{dt} | O:{r[1]} C:{r[2]} H:{r[3]} L:{r[4]} V:{r[5]}")
conn.close()
