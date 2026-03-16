import sqlite3
import pandas as pd
import os
import sys

def verify_and_audit():
    print("🚀 INICIANDO CERTIFICACIÓN DE DATOS BTC 2026")
    conn = sqlite3.connect('jesse_db.sqlite')
    count = conn.execute("SELECT count(*) FROM Candle WHERE symbol='BTC-USDT' AND timestamp >= 1772323200000").fetchone()[0]
    conn.close()
    
    print(f"Munición: {count} velas de 1m encontradas.")
    
    if count < 1440:
        print("❌ Error: No hay suficientes velas para un día de trading HFT.")
        return

    print("🔥 LANZANDO AUDITORÍA SOMBRA (1000+ TRADES TARGET)")
    # El script que antes falló, ahora lo ejecutaremos con la MasterWarrior HFT corregida
    os.system(f"{sys.executable} BTC_FINANCIAL_REALITY_200.py")

if __name__ == "__main__":
    verify_and_audit()
