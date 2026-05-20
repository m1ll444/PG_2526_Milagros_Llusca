import wifi_connector

# Configuración WiFi (modifica con tus credenciales)
SSID = 'CNT_FERNANDA'
PASSWORD = '1715#2392@'

# Intentar conexión usando el conector simple
try:
    cfg = wifi_connector.connect(SSID, PASSWORD)
    print('Ifconfig:', cfg)
except Exception as e:
    print('Error al conectar WiFi:', e)

