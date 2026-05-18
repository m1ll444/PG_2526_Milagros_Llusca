import network
import time
import machine

# LED de estado por defecto (GPIO2 funciona en muchas placas ESP32)
try:
    led = machine.Pin(2, machine.Pin.OUT)
except Exception:
    led = None

def _led_blink(on=True):
    if led is None:
        return
    led.value(1 if on else 0)

def connect(ssid, password, timeout=10, ap_ssid='ESP32_AP', ap_password='12345678'):
    """Conecta a una red WiFi en modo STA. Si falla, levanta un AP como fallback.

    Devuelve la tupla de ifconfig del adaptador activo (STA o AP).
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        _led_blink(True)
        return wlan.ifconfig()

    print('Conectando a WiFi:', ssid)
    wlan.connect(ssid, password)
    while not wlan.isconnected() and timeout > 0:
        # parpadeo mientras intenta
        if led is not None:
            led.value(not led.value())
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print('Conexión WiFi establecida.')
        _led_blink(True)
        return wlan.ifconfig()

    # fallback: iniciar Access Point
    print('Fallo al conectar. Iniciando Access Point:', ap_ssid)
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    try:
        ap.config(essid=ap_ssid, password=ap_password)
    except Exception:
        # algunas builds no aceptan password corto o config; ignorar si falla
        pass
    _led_blink(False)
    return ap.ifconfig()
