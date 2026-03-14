# ExnessExecutor - El brazo ejecutor de Antigravity (2026)
# Este script conecta Jesse con Exness via MetaTrader 5

import MetaTrader5 as mt5
import time
import sys

# --- CONFIGURACION DE EXNESS ---
ACCOUNT_LOGIN = 0  # Tu numero de cuenta Exness
ACCOUNT_PASSWORD = "" # Tu contraseña
ACCOUNT_SERVER = "" # Ejem: Exness-MT5Trial6
# ------------------------------

def initialize_mt5():
    """Inicializa la conexion con MetaTrader 5"""
    print("Iniciando conexion con Exness (MT5)...")
    if not mt5.initialize():
        print(f"Error al inicializar MT5: {mt5.last_error()}")
        return False
    
    # Intento de login si hay credenciales
    if ACCOUNT_LOGIN != 0:
        authorized = mt5.login(ACCOUNT_LOGIN, password=ACCOUNT_PASSWORD, server=ACCOUNT_SERVER)
        if not authorized:
            print(f"Fallo de login en Exness: {mt5.last_error()}")
            return False
            
    print("¡Conexion con Exness Exitosa!")
    account_info = mt5.account_info()._asdict()
    print(f"Cuenta: {account_info['login']} | Balance: {account_info['balance']} {account_info['currency']}")
    return True

def run_executor():
    """Bucle principal de ejecucion"""
    if not initialize_mt5():
        sys.exit()
        
    try:
        while True:
            # Aqui es donde leeriamos las señales de Jesse
            # Por ahora, solo mantenemos la conexion viva
            print("Esperando señales de Antigravity Core...")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Cerrando ejecutor...")
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    run_executor()
