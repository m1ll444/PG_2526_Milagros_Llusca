# Capacidad: Servidor Web e Interfaz de Usuario (ESP32)

## Purpose
Define la interfaz web responsiva alojada en el ESP32, el servidor web asíncrono que la sirve y el endpoint HTTP de control de comandos.

## Requirements

### Requirement: Servidor Web Asíncrono
El ESP32 SHALL inicializar un servidor web asíncrono utilizando `uasyncio` en MicroPython que escuche en el puerto 80. El servidor SHALL gestionar conexiones concurrentes sin bloquear otras tareas del procesador.

#### Scenario: Carga de la interfaz web
- **WHEN** El usuario ingresa a `http://<IP_ESP32>/` en su navegador.
- **THEN** El servidor web SHALL leer y devolver el contenido de `index.html` con cabeceras `200 OK` y tipo de contenido `text/html`.

#### Scenario: Ruta no encontrada
- **WHEN** El usuario solicita una ruta inexistente en el servidor.
- **THEN** El servidor SHALL devolver una respuesta `404 Not Found`.

### Requirement: Interfaz de Control (UI) con Switch de Modo Dual
La interfaz web SHALL servirse como un archivo HTML estático (`index.html`) con las siguientes características:
- Estética premium con tema oscuro (fondo `#0f172a`), gradientes dinámicos y glassmorphism.
- Indicador de estado visual (punto verde brillante) que indica "Sistema Online".
- Un switch toggle estilizado para cambiar el modo de control (WEB / MANUAL) con su respectiva etiqueta indicadora.
- Botones grandes y responsivos para control táctil en dispositivos móviles, organizados por eje: Carro, Elevación y Giro.
- Botón de parada de emergencia prominente y diferenciado visualmente en color rojo.

#### Scenario: Envío continuo de comandos por evento táctil
- **WHEN** El usuario mantiene presionado un botón de control de movimiento en la pantalla y el modo activo es `WEB`.
- **THEN** El navegador SHALL realizar peticiones HTTP GET recurrentes al endpoint `/cmd?action=<COMMAND>` cada 100 milisegundos.

#### Scenario: Parada al soltar un botón de control
- **WHEN** El usuario suelta un botón de control de movimiento.
- **THEN** El navegador SHALL enviar inmediatamente una petición HTTP GET a `/cmd?action=S` para detener el movimiento.

#### Scenario: Deshabilitación visual en modo manual
- **WHEN** El modo de control retornado por el servidor es `MANUAL`.
- **THEN** La interfaz web SHALL deshabilitar visualmente el panel de control de movimiento (opacidad reducida, cursor no permitido y bloqueo de eventos táctiles o clic), mostrando una advertencia del sistema.

### Requirement: API HTTP del Servidor
El servidor SHALL exponer los siguientes endpoints para el control y consulta del estado:
- `GET /cmd?action=<COMMAND>`: Recibe los comandos (como `F`, `B`, `S`, o `M`) desde el frontend y los canaliza a la interfaz UART.
- `GET /mode`: Devuelve el modo actual de control (`WEB` o `MANUAL`) en texto plano.

#### Scenario: Envío de comando HTTP para cambiar modo
- **WHEN** El usuario acciona el switch de modo en el navegador.
- **THEN** El navegador SHALL realizar una petición HTTP GET a `/cmd?action=M` para solicitar la conmutación de modo.

#### Scenario: Consulta periódica del modo activo (Polling)
- **WHEN** Transcurren 2 segundos desde la última consulta de modo.
- **THEN** La interfaz web SHALL realizar una petición HTTP GET a `/mode` para actualizar el estado del switch y el panel de control de forma sincronizada con el Arduino.

#### Scenario: Petición sin parámetro de acción en /cmd
- **WHEN** Se recibe una petición GET en `/cmd` sin el parámetro `action`.
- **THEN** El servidor SHALL devolver una respuesta `400 Bad Request` con el mensaje "Missing action".
