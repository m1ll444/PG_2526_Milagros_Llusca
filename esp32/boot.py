import wifi_connector

# Configuración WiFi (modifica con tus credenciales)
SSID = 'TU_SSID'
PASSWORD = 'TU_PASSWORD'

# Intentar conexión usando el conector simple
try:
    cfg = wifi_connector.connect(SSID, PASSWORD)
    print('Ifconfig:', cfg)
except Exception as e:
    print('Error al conectar WiFi:', e)

