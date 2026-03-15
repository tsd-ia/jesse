import os
import sys
import pandas as pd

# Inyectamos el entorno para que Jesse encuentre sus archivos
sys.path.insert(0, os.getcwd())

from jesse.research import backtest
import jesse.helpers as jh

def final_certified_audit():
    print("🚀 EJECUTANDO AUDITORÍA SOMBRA (ORO 2026)")
    
    # Configuración de guerra para Oro
    exchange = 'Binance Perpetual Futures'
    symbol = 'PAXG-USDT'
    
    config = {
        'starting_balance': 500,
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 20,
        'exchange': exchange,
        'warm_up_candles': 210
    }
    
    # Rango de Marzo 2026
    start_date = '2026-03-01'
    finish_date = '2026-03-12'

    try:
        # Corremos el motor puro de Jesse
        res = backtest(config, [
            {'exchange': exchange, 'symbol': symbol, 'timeframe': '1m', 'strategy': 'MasterWarrior2026'}
        ], [
            {'exchange': exchange, 'symbol': symbol, 'timeframe': '1m'}
        ], start_date=start_date, finish_date=finish_date)

        metrics = res['metrics']
        trades = res['trades']

        print(f"\n✅ AUDITORÍA COMPLETA")
        print(f"Total Trades: {len(trades)}")
        print(f"Net Profit: {metrics['net_profit_percentage']}%")
        print(f"Win Rate: {metrics['win_rate'] * 100}%")

        # Guardamos los resultados reales
        df_trades = pd.DataFrame(trades)
        df_trades.to_csv('REPORTE_GUERRA_FINAL_ORO.csv', index=False)
        
    except Exception as e:
        print(f"❌ Error en el motor: {e}")

if __name__ == "__main__":
    final_certified_audit()
