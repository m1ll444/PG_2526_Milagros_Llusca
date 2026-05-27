# Proyecto Grúa Torre: Requerimientos Técnicos para Generación de Código (v4)

> [!NOTE]
> **Adopción de OpenSpec:** Los requerimientos funcionales y técnicos de este documento han sido formalizados en especificaciones de comportamiento ubicadas en `openspec/specs/`. Consulta los enlaces para ver los escenarios detallados de cada capacidad:
> - [Comunicación UART](openspec/specs/comunicacion-uart/spec.md)
> - [Servidor Web e Interfaz](openspec/specs/servidor-web/spec.md)
> - [Control de Actuadores y Motores](openspec/specs/control-motores/spec.md)
> - [Lógica de Control Dual y Seguridad](openspec/specs/control-prioridad-seguridad/spec.md)
> - [Modo de Control Dual](openspec/specs/modo-control-dual/spec.md)
> - [Esquema de Conexiones Electrónicas](openspec/specs/schema-conexiones/spec.md)

## Contexto del Proyecto
Este documento está optimizado para su procesamiento por agentes de IA. El objetivo es detallar el firmware y la interfaz para una grúa torre con control dual exclusivo (Manual vía Joysticks o Remoto vía Web) utilizando comunicación directa USB (Web Serial API) con el Arduino y depuración inalámbrica ESP32 (SoftwareSerial a UART).

---

## 1. Arquitectura de Hardware y Pines

### Controlador A: Arduino Nano/Uno (Actuador Principal)
- **Framework:** Arduino / C++
- **Responsabilidad:** Leer joysticks analógicos, controlar los puentes H de los motores DC, gestionar la conmutación de modo (botón físico con debounce), comunicarse bidireccionalmente vía USB Serial con el navegador, y enviar logs de depuración unidireccionales vía SoftwareSerial al ESP32.
- **Asignación de Pines:**
  - **Joysticks:** X (Carro) -> A0, Y (Elevación) -> A1, Z (Giro) -> A2.
  - **Botón de Modo (Pulsador físico):** Joystick button -> D6 (INPUT_PULLUP).
  - **Driver TB6612FNG #1 (Motores DC N20 - Carro y Elevación):**
    - Motor A (Carro): AIN1 (D2), AIN2 (D4), PWMA (D3).
    - Motor B (Elevación): BIN1 (D7), BIN2 (D8), PWMB (D5).
    - STBY -> VCC (5V).
  - **Driver TB6612FNG #2 (Motoreductor DC 30RPM - Giro):**
    - Motor C (Giro): CIN1 (D11), CIN2 (D12), PWMC (D9).
    - STBY -> VCC (5V).
  - **Comunicación Principal (USB Serial):** RX (D0) y TX (D1) conectados al puerto USB nativo hacia la PC.
  - **Canal de Logs (SoftwareSerial):** D10 (RX - libre), D13 (TX - conectado al RX GPIO 16 del ESP32).

### Controlador B: ESP32 DevKit V1 (Monitor Inalámbrico de Logs)
- **Framework:** MicroPython (uasyncio)
- **Responsabilidad:** Recibir trazas de depuración de Arduino por UART a 9600 bps, almacenarlas en un buffer circular en RAM (últimas 50 líneas) y servir dinámicamente un HTML liviano (<2KB) de terminal retro en el puerto 80 con auto-refresco de 2s.
- **Asignación de Pines:**
  - **UART RX:** GPIO 16 (Conectado a TX SoftwareSerial D13 de Arduino).
  - **LED Status:** GPIO 2 (Parpadea con la actividad del servidor).


---

## 2. Requerimientos de Software (Backlog para Agente)

### Tarea 1: Firmware Arduino (grua_arduino.ino)
- **Modo de Control Exclusivo:** Variable `modoWeb` que conmuta entre `true` (Web) y `false` (Manual/Joystick). Al alternar el modo, se deben detener todos los motores inmediatamente por seguridad.
- **Debounce y Botón Físico:** Leer el pin D6 (botón del joystick) con un filtro anti-rebote de 50 ms. Al presionarlo, alternar `modoWeb` y enviar `W` o `J` por Serial USB y registrar el evento por SoftwareSerial.
- **Protocolo Serial Directo (USB):**
  - Recibe comandos web de movimiento (`F`, `B`, `U`, `D`, `L`, `R`, `S`) y de alternancia de modo (`M`) sobre Serial USB.
  - Envía la confirmación del modo activo (`W` para Web, `J` para Manual) inmediatamente al conmutar y telemetría periódica (`S:<modo>,<carro>,<elev>,<giro>\n`) cada 100ms.
- **Canal de Logs (SoftwareSerial D10/D13):**
  - Transmitir logs con etiquetas estructuradas (`[BOOT]`, `[MODE]`, `[CMD]`, `[MOT]`, `[SAFE]`) hacia el ESP32 para monitorización remota.
- **Velocidades Máximas Configurables:**
  - Constantes editables `MAX_SPEED_CARRO` (255), `MAX_SPEED_ELEVACION` (255), y `MAX_SPEED_GIRO` (200).
- **Timeout de Seguridad:** Si no se recibe ningún comando en modo Web en 500 ms, detener todos los motores y loguear `[SAFE] Timeout web`.

### Tarea 2: Firmware ESP32 (main.py)
- **Terminal Inalámbrica de Logs:** Servir una página HTML dinámica en el puerto 80.
- **Buffer Circular en RAM:** Mantener las últimas 50 líneas de log recibidas del Arduino por su UART (GPIO 16) a 9600 bps.
- **Diseño del Terminal:** Estilo visual retro de consola (fondo negro, texto verde monoespacio, auto-refresco HTTP de 2s, tamaño <2KB).

### Tarea 3: Interfaz Web de Control (web_server/index.html)
- **Conexión Directa USB:** Botón interactivo para iniciar/detener la conexión mediante **Web Serial API** a 9600 bps.
- **Procesamiento de Telemetría:** Leer asíncronamente las tramas de telemetría USB y actualizar el simulador 2.5D, los indicadores de dirección de motores y los medidores/barras de posición en tiempo real.
- **Fallback HTTP:** Si no hay puerto USB conectado o no es soportado, usar peticiones `fetch` contra la API del ESP32 como respaldo.
- **Barra de Navegación Cruzada:** Enlace "Esquema" integrado en el header hacia `schema.html`.

### Tarea 4: Esquema de Conexiones (web_server/schema.html)
- Diagrama interactivo SVG y tabla pin-a-pin con filtro dinámico JS, actualizado con el nuevo pin de SoftwareSerial (D13) de logs hacia el ESP32 (GPIO 16) y barra de navegación hacia `index.html`.

---

## 3. Consideraciones Técnicas y de Seguridad
- **Baudrate:** Configurar todos los puertos serie (Serial USB, SoftwareSerial, UART ESP32) a 9600 bps.
- **Estabilidad de Memoria:** El ESP32 no procesa archivos pesados ni sirve la página de control, evitando bloqueos por OutOfMemory.
- **Aislamiento de Entradas:** En modo Web se ignoran joysticks físicos, y en modo Manual se ignoran comandos web.

