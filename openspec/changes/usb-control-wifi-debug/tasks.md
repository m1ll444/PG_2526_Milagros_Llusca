## 1. Reorganización de Archivos del Proyecto

- [x] 1.1 Mover `grua_arduino/grua_arduino.ino` a `arduino/grua_arduino/grua_arduino.ino` y eliminar el directorio `grua_arduino/` original
- [x] 1.2 Mover `index.html` (raíz) y `Schema.html` a `web_server/index.html` y `web_server/schema.html`
- [x] 1.3 Verificar que `esp32/boot.py`, `esp32/main.py` permanecen en su lugar
- [x] 1.4 Eliminar archivos huérfanos de la raíz (`test_server.py`, `index.html`, `Schema.html`)
- [x] 1.5 Actualizar `README.md` con la nueva estructura de directorios

## 2. Firmware Arduino — Canal SoftwareSerial de Depuración

- [x] 2.1 Incluir `SoftwareSerial.h` y declarar instancia en pines D10 (RX) y D13 (TX) a 9600 bps
- [x] 2.2 Inicializar SoftwareSerial en `setup()` con mensaje de arranque `[BOOT] Sistema iniciado`
- [x] 2.3 Añadir traza de log `[MODE] Cambiado a WEB/MANUAL` en `leerComandoWeb()` y `leerBotonModo()` al cambiar de modo
- [x] 2.4 Añadir traza de log `[CMD] Recibido: <cmd>` al recibir un comando de movimiento válido en `leerComandoWeb()`
- [x] 2.5 Añadir traza de log `[SAFE] Timeout web - motores detenidos` cuando se activa el timeout de seguridad

## 3. Firmware Arduino — Compatibilidad Serial USB

- [x] 3.1 Verificar que `Serial.begin(9600)` se mantiene para comunicación USB con el navegador
- [x] 3.2 Verificar que las tramas de telemetría `S:<modo>,<carro>,<elev>,<giro>\n` se envían por Serial hardware (sin cambios en formato)
- [x] 3.3 Verificar que los comandos de entrada (`F`,`B`,`U`,`D`,`L`,`R`,`S`,`M`) se leen por Serial hardware (sin cambios)

## 4. Firmware ESP32 — Monitor de Depuración Inalámbrico

- [x] 4.1 Reescribir `esp32/main.py`: configurar UART RX-only (GPIO 16) a 9600 bps para recibir logs del Arduino
- [x] 4.2 Implementar buffer circular de 50 líneas en una lista Python
- [x] 4.3 Implementar tarea asíncrona `leer_logs()` que lea líneas del UART y las almacene en el buffer
- [x] 4.4 Implementar handler HTTP que genere dinámicamente HTML de terminal retro (fondo negro, texto verde monoespacio, <2KB)
- [x] 4.5 Incorporar `<meta http-equiv="refresh" content="2">` para auto-refresco
- [x] 4.6 Devolver 404 para rutas no reconocidas
- [x] 4.7 Actualizar `esp32/boot.py` si es necesario (WiFi AP/STA config)

## 5. Interfaz Web — Web Serial API

- [x] 5.1 Añadir botón de conexión/desconexión USB con indicador visual de estado (verde=conectado, rojo/gris=desconectado)
- [x] 5.2 Implementar función `conectarUSB()` que abra el puerto serial a 9600 bps y configure ReadableStream
- [x] 5.3 Implementar función `desconectarUSB()` que cierre el puerto serial y actualice el indicador visual
- [x] 5.4 Implementar bucle de lectura asíncrona de telemetría que parsee tramas `S:<modo>,<carro>,<elev>,<giro>\n`
- [x] 5.5 Actualizar la UI en tiempo real con los datos de telemetría recibidos por USB
- [x] 5.6 Modificar funciones de envío de comandos para escribir bytes por Web Serial cuando está conectado
- [x] 5.7 Implementar fallback HTTP (`fetch`) cuando Web Serial no está conectado o no está disponible
- [x] 5.8 Detectar desconexión inesperada del cable USB y activar fallback automáticamente

## 6. Navegación Cruzada

- [x] 6.1 Añadir barra de navegación en el encabezado de `web_server/index.html` con enlace a `schema.html`
- [x] 6.2 Añadir barra de navegación en el encabezado de `web_server/schema.html` con enlace a `index.html`
- [x] 6.3 Mantener consistencia visual de la barra de navegación con el diseño existente de cada página

## 7. Actualización de Documentación y Schema

- [x] 7.1 Actualizar `web_server/schema.html` con las nuevas conexiones SoftwareSerial (D10→no conectado, D13→GPIO16 ESP32)
- [x] 7.2 Actualizar la tabla de conexiones del schema con las nuevas asignaciones de pines
- [x] 7.3 Actualizar `README.md` con instrucciones de uso de Web Serial API, nueva estructura y requisitos de navegador
- [x] 7.4 Actualizar `requirements.md` si es necesario con los nuevos requisitos de hardware y software
