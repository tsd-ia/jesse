import os
import subprocess
import pandas as pd
import time

def run_brute_force_audit():
    print("🚀 INICIANDO BOMBARDEO DE BACKTESTS BTC (MOTOR PURO JESSE)")
    results = []
    
    # Período exacto según los timestamps detectados
    start_date = "2026-03-01"
    end_date = "2026-03-13"

    for i in range(1, 21): # Empecemos con los top 20 para certificar éxito
        print(f"Probando variante {i}...")
        # Modificamos la estrategia vía variables de entorno o archivos si fuera necesario,
        # pero por ahora usaremos el motor directo para ver un ROI real.
        
        cmd = f"jesse backtest {start_date} {end_date}"
        try:
            # Ejecutamos jesse backtest real
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=60)
            
            # Buscamos el ROI en la salida de consola de Jesse
            # Jesse imprime algo como: "Net Profit | 1.25 %"
            for line in stdout.split('\n'):
                if "Net Profit" in line and "%" in line:
                    roi = line.split('|')[1].replace('%', '').strip()
                    results.append({'Variante': i, 'ROI': float(roi), 'Status': 'SUCCESS'})
                    print(f"✅ Éxito: {roi}%")
                    break
        except Exception as e:
            print(f"❌ Error en variante {i}: {e}")

    df = pd.DataFrame(results)
    df.to_csv('RANKING_BTC_BRUTO_2026.csv', index=False)
    print("\nRanking generado con éxito.")

if __name__ == "__main__":
    run_brute_force_audit()
