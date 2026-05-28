## Context

El sistema de control de la Grúa Torre actualmente opera con un ESP32 como gateway entre la interfaz web y el Arduino. El ESP32 sirve un archivo HTML de ~50KB, procesa solicitudes HTTP concurrentes y las traduce a comandos UART. Esto provoca OutOfMemory y bloqueos bajo carga. El Arduino controla 3 motores DC mediante dos puentes H TB6612FNG, lee 3 joysticks analógicos y gestiona un botón de modo (D6). La comunicación actual es: Navegador → WiFi → ESP32 HTTP → UART → Arduino.

El Arduino ya emite telemetría en formato `S:W,F,S,S\n` por el Serial hardware a 9600 bps, y el ESP32 la parsea para exponerla vía endpoints HTTP.

## Goals / Non-Goals

**Goals:**
- Eliminar el ESP32 como gateway de control, trasladando toda la comunicación de control al cable USB directo (Navegador ↔ Arduino via Web Serial API).
- Reutilizar el ESP32 exclusivamente como monitor inalámbrico de depuración, sirviendo una página HTML ultraliviana (<2KB) que muestre los logs del Arduino.
- Añadir un canal SoftwareSerial secundario en el Arduino (pines D10 RX / D13 TX) para enviar trazas de log al ESP32 sin interferir con el Serial hardware USB.
- Mantener el fallback HTTP como alternativa cuando no hay USB disponible.
- Reorganizar archivos en `/arduino/`, `/esp32/` y `/web_server/`.

**Non-Goals:**
- No se implementará WebSocket en tiempo real desde el ESP32 (se usa auto-refresco HTTP simple cada 2s).
- No se cambiará la lógica de control de motores, joysticks ni el protocolo de comandos de movimiento existente.
- No se soportarán navegadores que no implementen Web Serial API (Safari, Firefox) como canal primario; estos usarán el fallback HTTP.
- No se implementará autenticación ni cifrado en ningún canal.

## Decisions

### 1. Web Serial API como canal principal de control
**Decisión**: Usar la Web Serial API nativa de Chrome/Edge para comunicación directa USB ↔ Arduino a 9600 bps.

**Alternativas consideradas**:
- *Node.js serial server*: Requiere instalar software adicional, más complejidad.
- *Mantener ESP32 como gateway*: Perpetúa el problema de memoria y latencia.

**Rationale**: La Web Serial API es nativa del navegador, no requiere drivers ni software adicional, y elimina completamente la latencia WiFi. Chrome/Edge cubren >80% de los navegadores de escritorio.

### 2. SoftwareSerial en pines D10 (RX) y D13 (TX) para canal de depuración
**Decisión**: Usar SoftwareSerial a 9600 bps en pines que no están ocupados por motores ni joysticks.

**Alternativas consideradas**:
- *Segundo hardware UART (Arduino Mega)*: Requiere cambiar de microcontrolador.
- *I2C para logs*: Mayor complejidad, no aporta beneficios para texto plano unidireccional.

**Rationale**: D10 y D13 están libres en la asignación actual de pines (D0-D9, D11-D12, A0-A2 están asignados). SoftwareSerial es adecuado para tráfico unidireccional de baja frecuencia (logs textuales).

### 3. Buffer circular de 50 líneas en ESP32 con auto-refresco HTTP
**Decisión**: El ESP32 almacena las últimas 50 líneas de log en una lista Python y sirve un HTML de terminal retro con `<meta http-equiv="refresh" content="2">`.

**Alternativas consideradas**:
- *WebSocket para streaming en tiempo real*: Más complejo y consume más memoria en el ESP32.
- *Server-Sent Events (SSE)*: MicroPython no lo soporta nativamente.

**Rationale**: El auto-refresco HTTP es la solución más liviana posible. No requiere JavaScript complejo en el cliente ni mantener conexiones abiertas. El HTML generado dinámicamente es <2KB, resolviendo el problema de memoria del ESP32.

### 4. Fallback HTTP transparente
**Decisión**: La interfaz web detecta si Web Serial está disponible y conectado. Si no, usa `fetch()` contra el ESP32 (que en este escenario también debería re-enrutar comandos si se conecta como gateway alternativo).

**Rationale**: Garantiza usabilidad desde dispositivos móviles o navegadores sin Web Serial.

### 5. Navegación cruzada en encabezados
**Decisión**: Añadir una barra de navegación consistente en la parte superior de `index.html` y `schema.html` con enlaces bidireccionales, integrada en el diseño visual existente.

### 6. Organización de archivos en tres carpetas
**Decisión**: `/arduino/grua_arduino.ino`, `/esp32/boot.py` + `/esp32/main.py`, `/web_server/index.html` + `/web_server/schema.html`.

**Rationale**: Separa claramente las responsabilidades (firmware MCU, firmware ESP32, frontend web) y elimina ambigüedad sobre qué archivo desplegar en qué dispositivo.

## Risks / Trade-offs

- **Web Serial API no soportada en todos los navegadores** → Mitigación: fallback HTTP funcional y documentación clara de requisitos de navegador.
- **SoftwareSerial consume CPU en el Arduino** → Mitigación: transmisión de logs a baja frecuencia (máximo 1 línea cada 200ms), unidireccional TX-only.
- **D13 es el pin del LED integrado del Arduino** → Mitigación: El LED parpadeará con la actividad de log, lo cual puede servir como indicador visual de actividad. Si interfiere, se puede cambiar a otro pin libre.
- **Reorganización de archivos rompe rutas existentes** → Mitigación: actualizar README.md, requirements.md, y toda referencia interna en una sola operación atómica.
- **Pérdida de logs si el ESP32 se reinicia** → Aceptable: los logs de depuración son efímeros por naturaleza.
