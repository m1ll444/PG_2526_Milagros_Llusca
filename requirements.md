# Proyecto Grúa Torre: Requerimientos Técnicos para Generación de Código (v3)

> [!NOTE]
> **Adopción de OpenSpec:** Los requerimientos funcionales y técnicos de este documento han sido formalizados en especificaciones de comportamiento ubicadas en `openspec/specs/`. Consulta los enlaces para ver los escenarios detallados de cada capacidad:
> - [Comunicación UART](openspec/specs/comunicacion-uart/spec.md)
> - [Servidor Web e Interfaz](openspec/specs/servidor-web/spec.md)
> - [Control de Actuadores y Motores](openspec/specs/control-motores/spec.md)
> - [Lógica de Control Dual y Seguridad](openspec/specs/control-prioridad-seguridad/spec.md)
> - [Modo de Control Dual](openspec/specs/modo-control-dual/spec.md)
> - [Esquema de Conexiones Electrónicas](openspec/specs/schema-conexiones/spec.md)

## Contexto del Proyecto
Este documento está optimizado para su procesamiento por agentes de IA. El objetivo es detallar el firmware y la interfaz para una grúa torre con control dual exclusivo (Manual vía Joysticks o Remoto vía Web) utilizando comunicación serial bidireccional entre un ESP32 y un Arduino Nano/Uno.

---

## 1. Arquitectura de Hardware y Pines

### Controlador A: Arduino Nano/Uno (Actuador Principal)
- **Framework:** Arduino / C++
- **Responsabilidad:** Leer joysticks analógicos, controlar los puentes H de los motores DC, gestionar la conmutación de modo (botón físico con debounce) y comunicarse de forma bidireccional vía UART con el ESP32.
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
  - **Comunicación UART:** RX (D0) desde el TX del ESP32, TX (D1) hacia el RX del ESP32.

### Controlador B: ESP32 DevKit V1 (Interfaz Web)
- **Framework:** MicroPython (uasyncio)
- **Responsabilidad:** Servidor web asíncrono para index.html, enrutamiento de comandos HTTP hacia UART, recepción asíncrona del estado del modo desde Arduino y exposición del endpoint `/mode`.
- **Asignación de Pines:**
  - **UART TX:** GPIO 17 (Conectado a RX D0 de Arduino).
  - **UART RX:** GPIO 16 (Conectado a TX D1 de Arduino).
  - **LED Status:** GPIO 2 (Activo según el estado de la comunicación).

---

## 2. Requerimientos de Software (Backlog para Agente)

### Tarea 1: Firmware Arduino (grua_arduino.ino)
- **Modo de Control Exclusivo:** Variable `modoWeb` que conmuta entre `true` (Web) y `false` (Manual/Joystick). Al alternar el modo, se deben detener todos los motores inmediatamente por seguridad.
- **Debounce y Botón Físico:** Leer el pin D6 (botón del joystick) con un filtro anti-rebote de 50 ms. Al presionarlo, alternar `modoWeb` y enviar `W` o `J` por serial.
- **Protocolo Serial Bidireccional:**
  - Recibe comandos web de movimiento (`F`, `B`, `U`, `D`, `L`, `R`, `S`) y de alternancia de modo (`M`).
  - Envía la confirmación del modo activo (`W` para Web, `J` para Manual) inmediatamente al conmutar.
- **Velocidades Máximas Configurables:**
  - Constantes editables `MAX_SPEED_CARRO` (255), `MAX_SPEED_ELEVACION` (255), y `MAX_SPEED_GIRO` (200) para acotar la velocidad máxima del PWM.
  - Mapear las entradas de joystick analógicas (`0 - DEADBAND_LOW` y `DEADBAND_HIGH - 1023`) proporcionalmente hacia `0` y su respectiva constante de velocidad máxima.
- **Timeout de Seguridad:** Si no se recibe ningún comando en modo Web en 500 ms, detener todos los motores. Desactivar este timeout al estar en modo Manual.

### Tarea 2: Firmware ESP32 (main.py)
- **Servidor Web Asíncrono:** Servir el archivo `index.html` en el puerto 80.
- **API y Enrutamiento UART:**
  - Endpoint `/cmd?action=<COMMAND>`: Envía el carácter del comando recibido (como `F`, `B`, `S` o `M`) al Arduino a través de UART.
  - Endpoint `/mode`: Retorna el modo activo actual (`WEB` o `MANUAL`) en texto plano.
- **Lectura de UART Asíncrona:** Hilo/tarea asíncrona para leer bytes desde el Arduino. Si recibe `W` actualizar `current_mode = 'WEB'`, y si recibe `J` actualizar `current_mode = 'MANUAL'`.

### Tarea 3: Interfaz Web (index.html)
- **Switch Toggle de Modo:** Un switch estilizado de tema glassmorphism para alternar el modo. Al accionarlo envía `/cmd?action=M`.
- **Polling de Estado:** Consultar `/mode` cada 2 segundos para sincronizar el estado visual del switch con el estado real del Arduino.
- **Deshabilitación de Controles:** Si el modo es `MANUAL`, deshabilitar visualmente y funcionalmente todos los botones de movimiento (opacidad reducida, bloqueo de clics) e informar del estado al usuario.
- **Estética:** Mantener el tema oscuro (`#0f172a`), bordes translúcidos con desenfoque de fondo y transiciones suaves de color.

### Tarea 4: Esquema de Conexiones (Schema.html)
- Documento autoventilado y responsivo en la raíz del proyecto.
- Diagrama de bloques en SVG inline que detalla la conexión de alimentación de 12V y 5V, los dos microcontroladores, los dos puentes H, los 3 motores DC y los joysticks.
- Tabla interactiva con motor de filtrado por texto en JS para buscar conexiones (origen, pin, destino, pin, tipo y observaciones).

---

## 3. Consideraciones Técnicas y de Seguridad
- **Baudrate:** Configurar ambos controladores a 9600 bps.
- **Exclusividad del Canal:** En modo Web, ignorar por completo las lecturas físicas del joystick para evitar movimientos indeseados. En modo Manual, ignorar comandos web de movimiento.

