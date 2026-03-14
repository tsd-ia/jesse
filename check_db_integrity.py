import sqlite3
from datetime import datetime
conn = sqlite3.connect('jesse_db.sqlite')
c = conn.cursor()
c.execute('SELECT MIN(timestamp), MAX(timestamp), exchange, timeframe FROM Candle WHERE symbol="PAXG-USDT" GROUP BY exchange, timeframe')
res = c.fetchall()
for r in res:
    print(f"Exchange: {r[2]} | TF: {r[3]} | Start: {datetime.fromtimestamp(r[0]/1000)} | End: {datetime.fromtimestamp(r[1]/1000)}")
conn.close()
