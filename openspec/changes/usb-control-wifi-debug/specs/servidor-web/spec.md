## MODIFIED Requirements

### Requirement: Servidor Web Asíncrono
El ESP32 SHALL inicializar un servidor web asíncrono utilizando `uasyncio` en MicroPython que escuche en el puerto 80. El servidor SHALL servir exclusivamente una página de depuración ultraliviana generada dinámicamente con las últimas 50 líneas de logs recibidos del Arduino.

#### Scenario: Carga de la página de depuración
- **WHEN** Un usuario ingresa a `http://<IP_ESP32>/` en su navegador (incluido un celular).
- **THEN** El servidor SHALL generar dinámicamente una página HTML de terminal retro (fondo negro `#0a0a0a`, texto verde `#00ff41`, fuente monoespaciada) con las líneas del buffer circular y cabecera `200 OK`.

#### Scenario: Ruta no encontrada
- **WHEN** El usuario solicita una ruta inexistente en el servidor.
- **THEN** El servidor SHALL devolver una respuesta `404 Not Found`.

## REMOVED Requirements

### Requirement: Interfaz de Control (UI) con Switch de Modo Dual
**Reason**: La interfaz de control se carga localmente en el navegador del PC desde el sistema de archivos, no desde el ESP32. El ESP32 ya no sirve archivos de control.
**Migration**: Abrir `index.html` directamente desde la carpeta `/web_server/` del proyecto en el navegador Chrome/Edge.

### Requirement: API HTTP del Servidor
**Reason**: Los endpoints `/cmd` y `/mode` ya no son necesarios como canal principal porque el control se realiza por Web Serial API (USB directo). El ESP32 se dedica exclusivamente a depuración.
**Migration**: Si se necesita fallback HTTP, el ESP32 puede re-habilitarse como gateway de control alternativo mediante configuración.
