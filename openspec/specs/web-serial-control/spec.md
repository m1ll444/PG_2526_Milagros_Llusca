# web-serial-control Specification

## Purpose
TBD - created by archiving change usb-control-wifi-debug. Update Purpose after archive.
## Requirements
### Requirement: Conexión Web Serial desde el navegador
El sistema SHALL permitir al usuario conectar su navegador (Chrome/Edge) directamente al Arduino vía USB utilizando la Web Serial API a 9600 bps. La interfaz SHALL mostrar un botón de conexión/desconexión claramente visible que indique el estado actual de la conexión.

#### Scenario: Conexión exitosa por Web Serial
- **WHEN** El usuario hace clic en el botón "Conectar USB" y selecciona el puerto serial del Arduino en el diálogo del navegador.
- **THEN** El sistema SHALL abrir el puerto a 9600 bps, iniciar la lectura asíncrona de telemetría, cambiar el indicador visual a "USB Conectado" (verde) y habilitar el envío de comandos por el canal USB.

#### Scenario: Desconexión de Web Serial
- **WHEN** El usuario hace clic en el botón "Desconectar" o el cable USB se desconecta físicamente.
- **THEN** El sistema SHALL cerrar el puerto serial, cambiar el indicador visual a "Desconectado" (gris/rojo) y activar automáticamente el fallback HTTP si está configurado.

### Requirement: Envío de comandos de movimiento por Web Serial
El sistema SHALL enviar caracteres ASCII simples de un solo byte (`F`, `B`, `U`, `D`, `L`, `R`, `S`, `M`) directamente al Arduino por el puerto serial USB cuando el usuario interactúe con los botones de control o presione teclas mapeadas.

#### Scenario: Envío de comando de movimiento por USB
- **WHEN** El usuario mantiene presionado el botón "Adelante" en la interfaz web con Web Serial conectado.
- **THEN** El navegador SHALL escribir el byte `F` en el puerto serial USB cada 100ms mientras se mantenga la presión.

#### Scenario: Envío de comando de parada al soltar botón
- **WHEN** El usuario suelta cualquier botón de movimiento con Web Serial conectado.
- **THEN** El navegador SHALL escribir el byte `S` inmediatamente en el puerto serial USB.

### Requirement: Recepción y procesamiento de telemetría USB
El sistema SHALL leer asíncronamente las tramas de telemetría enviadas por el Arduino en formato `S:<modo>,<carro>,<elev>,<giro>\n` por el puerto serial USB y actualizar en tiempo real los indicadores visuales de la interfaz.

#### Scenario: Actualización de UI por telemetría recibida
- **WHEN** El navegador recibe la trama `S:W,F,U,S\n` por Web Serial.
- **THEN** La interfaz SHALL actualizar el indicador de modo a "WEB", el indicador de carro a "Adelante", el de elevación a "Subir" y el de giro a "Detenido".

### Requirement: Fallback HTTP cuando no hay USB
El sistema SHALL mantener el mecanismo de control por llamadas HTTP (`fetch`) como método de respaldo. Si Web Serial no está disponible o no está conectado, los comandos SHALL enviarse al ESP32 vía WiFi.

#### Scenario: Activación automática de fallback HTTP
- **WHEN** El navegador no soporta Web Serial API o el usuario no ha conectado un puerto USB.
- **THEN** Los botones de control SHALL enviar comandos mediante peticiones HTTP GET a `/cmd?action=<COMMAND>` dirigidas al ESP32 y consultar `/status` para actualizar la telemetría.

