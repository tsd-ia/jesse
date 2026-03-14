import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuracion de los datos (XAUUSD)
symbol = 'XAUUSD'
exchange = 'Bybit'
start_date = datetime(2026, 3, 6)
end_date = datetime.now()

print(f"Generando datos sinteticos para {symbol} desde {start_date}...")

# Conectar a la DB de Jesse
conn = sqlite3.connect('jesse_db.sqlite')
cursor = conn.cursor()

# Crear tabla si no existe (Estructura de Jesse)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Candle (
    id TEXT PRIMARY KEY,
    symbol TEXT,
    exchange TEXT,
    timestamp INTEGER,
    open REAL,
    close REAL,
    high REAL,
    low REAL,
    volume REAL
)
''')

# Generar velas de 1 minuto
current_time = start_date
price = 2150.0 # Precio base del Oro en 2026
candles = []

while current_time < end_date:
    ts = int(current_time.timestamp() * 1000)
    change = np.random.normal(0, 0.5) # Volatilidad del Oro
    o = price
    c = price + change
    h = max(o, c) + abs(np.random.normal(0, 0.2))
    l = min(o, c) - abs(np.random.normal(0, 0.2))
    v = np.random.uniform(10, 100)
    
    candles.append((f"{ts}-{symbol}-{exchange}", symbol, exchange, ts, o, c, h, l, v))
    
    price = c
    current_time += timedelta(minutes=1)

# Insertar datos masivamente
cursor.executemany('INSERT OR REPLACE INTO Candle VALUES (?,?,?,?,?,?,?,?,?)', candles)
conn.commit()
conn.close()

print(f"¡Exito! Se han inyectado {len(candles)} velas en la base de datos local.")
