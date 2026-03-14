# fix_network.py - Parche Antigravity para bypass de DNS (2026)
import socket

# Coordenadas exactas obtenidas via Satelite (Browser Subagent)
JESSE_IPS = ['104.26.0.214', '104.26.1.214', '172.67.71.108']

# Guardamos la funcion original por seguridad
original_getaddrinfo = socket.getaddrinfo

def ghost_getaddrinfo(*args, **kwargs):
    host = args[0]
    if host in ['jesse.trade', 'api.jesse.trade', 'updates.jesse.trade']:
        # Forzamos la resolucion al primer bunker de Cloudflare
        print(f"[ANTIGRAVITY] Bypass DNS para: {host} -> {JESSE_IPS[0]}")
        return original_getaddrinfo(JESSE_IPS[0], *args[1:], **kwargs)
    return original_getaddrinfo(*args, **kwargs)

# Aplicar el parche al nucleo de Python
socket.getaddrinfo = ghost_getaddrinfo

print("¡Parche de Red Antigravity ACTIVO! (Bypass de DNS para Jesse)")
