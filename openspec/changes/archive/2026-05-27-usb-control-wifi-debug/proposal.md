## Why

El módulo ESP32 experimenta cuellos de botella e inestabilidades de memoria (OutOfMemory) al intentar servir la interfaz web pesada (~50KB HTML) y procesar simultáneamente las solicitudes HTTP de control. Esto degrada la experiencia de control en tiempo real y provoca desconexiones esporádicas. Se necesita desacoplar el canal de control principal (USB directo al Arduino) del canal de depuración inalámbrica (ESP32 como monitor de logs), eliminando la carga del ESP32 como gateway de control y permitiendo una interfaz web local más rica sin restricciones de memoria.

## What Changes

- **BREAKING**: El ESP32 deja de ser el gateway de control principal. Ya no sirve `index.html` ni enruta comandos HTTP→UART al Arduino.
- Se incorpora la **Web Serial API** en la interfaz web para enviar comandos y recibir telemetría JSON directamente del Arduino por USB a 9600 bps desde Chrome/Edge.
- Se añade un **canal secundario SoftwareSerial** (pines D10/D13) en el Arduino para enviar trazas de depuración al ESP32.
- El ESP32 se reconvierte en un **monitor de depuración inalámbrico**: lee logs del Arduino por su UART RX, los almacena en un buffer circular de 50 líneas y sirve una página HTML ultraliviana con estética de terminal retro (auto-refresco cada 2s) accesible desde un celular.
- Se mantiene el fallback HTTP (`fetch`) en la interfaz web como método alternativo si el USB no está conectado.
- Se añaden **enlaces de navegación cruzada** entre `index.html` y `schema.html` en el encabezado de ambas páginas.
- Se reorganizan los archivos del proyecto en tres directorios: `/arduino/`, `/esp32/` y `/web_server/`, eliminando archivos huérfanos de la raíz.

## Capabilities

### New Capabilities
- `web-serial-control`: Control de la grúa desde el navegador vía Web Serial API (USB directo al Arduino), incluyendo envío de comandos, recepción de telemetría JSON y botón de conexión/desconexión en la UI.
- `debug-monitor-wifi`: Monitor de depuración inalámbrico en el ESP32 que recibe logs por SoftwareSerial desde el Arduino y los expone en una interfaz web ultraliviana con estética de terminal retro.
- `navegacion-cruzada`: Enlaces de navegación interactivos en el encabezado de `index.html` y `schema.html` para navegar bidireccionalmente entre ambas páginas.

### Modified Capabilities
- `comunicacion-uart`: El canal UART principal (Serial hardware, D0/D1) pasa de comunicarse con el ESP32 a comunicarse directamente con el navegador vía USB. Se añade un canal secundario SoftwareSerial (D10/D13) exclusivo para enviar logs de depuración al ESP32.
- `servidor-web`: El ESP32 deja de servir la interfaz de control y pasa a servir únicamente una página de depuración de logs ultraliviana. La interfaz de control se carga localmente desde el sistema de archivos del PC.
- `control-motores`: Se añade la integración de SoftwareSerial para emitir trazas de depuración del estado de los motores por el canal secundario.

## Impact

- **Arduino (`grua_arduino.ino`)**: Incluir `SoftwareSerial.h`, inicializar puerto secundario en pines D10 (RX) y D13 (TX), redirigir logs de depuración a este puerto y mantener Serial hardware para comandos y telemetría USB.
- **ESP32 (`main.py`)**: Reescribir completamente — leer logs por UART RX (GPIO 16), almacenar en buffer circular (50 líneas), servir HTML ultraliviano de depuración con auto-refresco.
- **Interfaz web (`index.html`)**: Incorporar Web Serial API con botón de conexión, leer telemetría asíncrona del Arduino, mantener fallback HTTP, añadir navegación cruzada.
- **Schema.html**: Añadir barra de navegación cruzada y actualizar diagrama de conexiones con el nuevo canal SoftwareSerial.
- **Estructura de archivos**: Migrar archivos a `/arduino/`, `/esp32/`, `/web_server/` y limpiar raíz del proyecto. **BREAKING**: las rutas de archivos cambian.
- **Pines disponibles**: Se ocupan D10 (RX SoftwareSerial, no usado actualmente) y D13 (TX SoftwareSerial, no usado actualmente).
