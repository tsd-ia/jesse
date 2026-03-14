import sqlite3
import ccxt
import time
import uuid
from datetime import datetime, timedelta

# Configuración
symbol = 'PAXG/USDT' # El Oro en Binance
jesse_symbol = 'PAXG-USDT'
exchange_id = 'Binance Spot'
timeframe = '1m'
since_date = datetime(2026, 2, 10) # 20 dias antes para el warmup

print(f"--- INICIANDO DESCARGA DE ORO REAL (PAXG) ---")

exchange = ccxt.binance()
since = int(since_date.timestamp() * 1000)
all_candles = []

try:
    while since < int(time.time() * 1000):
        print(f"Descargando velas desde: {datetime.fromtimestamp(since/1000)}")
        candles = exchange.fetch_ohlcv(symbol, timeframe, since, limit=1000)
        if not candles:
            break
        all_candles.extend(candles)
        since = candles[-1][0] + 60000 
        time.sleep(0.2)
except Exception as e:
    print(f"Error descargando: {e}")

print(f"Total velas obtenidas: {len(all_candles)}")

# Inyeccion en la DB de Jesse con SCHEMA CORRECTO (1.13.7)
# (id, timestamp, open, close, high, low, volume, exchange, symbol, timeframe)
conn = sqlite3.connect('jesse_db.sqlite')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Candle (
    id TEXT PRIMARY KEY,
    timestamp INTEGER,
    open REAL,
    close REAL,
    high REAL,
    low REAL,
    volume REAL,
    exchange TEXT,
    symbol TEXT,
    timeframe TEXT
)
''')

jesse_data = []
for c in all_candles:
    ts = c[0]
    jesse_data.append((
        str(uuid.uuid4()), # id
        ts, 
        c[1], # Open
        c[4], # Close
        c[2], # High
        c[3], # Low
        c[5], # Volume
        exchange_id,
        jesse_symbol,
        timeframe
    ))

cursor.executemany('INSERT OR REPLACE INTO Candle VALUES (?,?,?,?,?,?,?,?,?,?)', jesse_data)
conn.commit()
conn.close()

print(f"¡EXITO CRITICO! Datos de Oro Real inyectados con el esquema oficial.")
