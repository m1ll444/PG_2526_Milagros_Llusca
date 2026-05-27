# Capacidad: Servidor Web e Interfaz de Usuario (ESP32)

## Purpose
Define la interfaz web responsiva alojada en el ESP32, el servidor web asíncrono que la sirve y el endpoint HTTP de control de comandos.
## Requirements
### Requirement: Servidor Web Asíncrono
El ESP32 SHALL inicializar un servidor web asíncrono utilizando `uasyncio` en MicroPython que escuche en el puerto 80. El servidor SHALL servir exclusivamente una página de depuración ultraliviana generada dinámicamente con las últimas 50 líneas de logs recibidos del Arduino.

#### Scenario: Carga de la página de depuración
- **WHEN** Un usuario ingresa a `http://<IP_ESP32>/` en su navegador (incluido un celular).
- **THEN** El servidor SHALL generar dinámicamente una página HTML de terminal retro (fondo negro `#0a0a0a`, texto verde `#00ff41`, fuente monoespaciada) con las líneas del buffer circular y cabecera `200 OK`.

#### Scenario: Ruta no encontrada
- **WHEN** El usuario solicita una ruta inexistente en el servidor.
- **THEN** El servidor SHALL devolver una respuesta `404 Not Found`.

