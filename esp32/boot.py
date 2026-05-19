import wifi_connector

# Configuración WiFi (modifica con tus credenciales)
SSID = 'Cudy-0138'
PASSWORD = '41659458'

# Intentar conexión usando el conector simple
try:
    cfg = wifi_connector.connect(SSID, PASSWORD)
    print('Ifconfig:', cfg)
except Exception as e:
    print('Error al conectar WiFi:', e)

