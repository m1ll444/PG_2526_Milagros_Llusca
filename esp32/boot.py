import network
import time
import machine

# Configuración WiFi
SSID = 'TU_SSID'
PASSWORD = 'TU_PASSWORD'

# Configuración del LED de estado
led = machine.Pin(2, machine.Pin.OUT)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red...')
        wlan.connect(SSID, PASSWORD)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            led.value(not led.value()) # Parpadeo mientras conecta
            time.sleep(1)
            timeout -= 1
    
    if wlan.isconnected():
        print('Conexión WiFi establecida.')
        print('Configuración de red:', wlan.ifconfig())
        led.value(1) # LED encendido fijo si está conectado
    else:
        print('Fallo al conectar al WiFi. Iniciando modo Access Point...')
        # Opcional: Levantar AP si falla
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid='GruaTorre_AP', password='password123')
        print('Access Point activo. IP:', ap.ifconfig()[0])
        led.value(0) # LED apagado si está en modo AP

connect_wifi()
