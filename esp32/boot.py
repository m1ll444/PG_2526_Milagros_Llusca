import sys
import uselect
import time
import network
import machine

# Configuración WiFi
SSID = 'Cudy-0138'
PASSWORD = '41659458'

def menu_inicio(timeout_segundos=5):
    """Muestra un menú para interceptar el arranque y evitar bucles."""
    print("\n" + "="*40)
    print("      SISTEMA DE CONTROL - GRÚA TORRE")
    print("="*40)
    print("1. Iniciar sistema normalmente")
    print("2. Detener en modo programación (REPL)")
    print(f"Selecciona una opción (Auto-inicio en {timeout_segundos}s)...")
    
    poller = uselect.poll()
    poller.register(sys.stdin, uselect.POLLIN)
    
    tiempo_inicio = time.time()
    while (time.time() - tiempo_inicio) < timeout_segundos:
        if poller.poll(100):
            caracter = sys.stdin.read(1)
            if caracter == '1':
                return True
            elif caracter == '2':
                print("\n-> Modo programación activo. REPL liberado.")
                return False
    return True

def conectar_wifi(ssid, password, timeout=15):
    """Conecta a WiFi e imprime la IP asignada."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f'Conectando a {ssid}...')
        wlan.connect(ssid, password)
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")
        print("")
        
    if wlan.isconnected():
        config = wlan.ifconfig()
        print("\n" + "*"*40)
        print(" CONEXIÓN EXITOSA")
        print(f" IP Local: {config[0]}")
        print(f" Acceso Web: http://{config[0]}")
        print("*"*40 + "\n")
        return True
    else:
        print("\n Fallo al conectar a WiFi.")
        return False

# --- FLUJO PRINCIPAL ---
if menu_inicio(timeout_segundos=5):
    conectar_wifi(SSID, PASSWORD)
else:
    sys.exit()
