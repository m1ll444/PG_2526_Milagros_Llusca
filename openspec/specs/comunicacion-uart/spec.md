# Capacidad: Comunicación UART ESP32-Arduino

## Purpose
Define el protocolo de comunicación serie bidireccional y el set de comandos que permite coordinar el modo de control y enviar instrucciones de movimiento entre el ESP32 y el Arduino Nano/Uno.

## Requirements

### Requirement: Configuración de Interfaz Serie Bidireccional
La comunicación física SHALL realizarse mediante una línea serie dedicada utilizando los siguientes parámetros:
- **Baudrate:** 9600 bps
- **Canal de Transmisión (ESP32 a Arduino):** Desde ESP32 TX (GPIO 17) hacia Arduino RX (D0).
- **Canal de Recepción (Arduino a ESP32):** Desde Arduino TX (D1) hacia ESP32 RX (GPIO 16).

#### Scenario: Inicialización de la línea serie
- **WHEN** El sistema arranca de manera normal.
- **THEN** El ESP32 SHALL configurar el puerto UART2 a 9600 baudios utilizando TX (17) y RX (16). El Arduino SHALL inicializar `Serial` a 9600 baudios.

### Requirement: Protocolo y Set de Comandos de Movimiento y Modo
El protocolo SHALL consistir en enviar caracteres ASCII de un solo byte correspondientes al movimiento o al cambio de modo deseado:
- **Comandos de movimiento (ESP32 → Arduino):**
  - `F` (Forward / Adelante)
  - `B` (Backward / Atrás)
  - `U` (Up / Subir)
  - `D` (Down / Bajar)
  - `L` (Left / Izquierda)
  - `R` (Right / Derecha)
  - `S` (Stop / Parar)
- **Comando de cambio de modo (ESP32 → Arduino):**
  - `M` (Toggle Mode / Alternar Modo)
- **Estados de modo de control (Arduino → ESP32):**
  - `W` (Web Mode / Modo Web activo)
  - `J` (Joystick Mode / Modo Manual activo)

#### Scenario: Envío de comando de movimiento desde la web
- **WHEN** El usuario presiona el botón "Adelante" (F) en la interfaz web del ESP32.
- **THEN** El ESP32 SHALL escribir el byte `F` por el puerto serie.

#### Scenario: Recepción de comando de movimiento válido en Arduino
- **WHEN** El Arduino recibe el byte `U` a través del puerto serie.
- **THEN** El Arduino SHALL almacenar el comando en la variable `webCommand` y actualizar la marca de tiempo `lastWebCommandTime`.

#### Scenario: Envío de comando de parada (STOP)
- **WHEN** El usuario suelta cualquier botón de movimiento o presiona "STOP" en la interfaz.
- **THEN** El ESP32 SHALL escribir el byte `S` por el puerto serie.

#### Scenario: Sincronización bidireccional al alternar modo
- **WHEN** El ESP32 recibe una petición de cambio de modo y envía el byte `M` al Arduino, o el operador presiona el botón físico en el joystick.
- **THEN** El Arduino SHALL alternar el estado de `modoWeb` y responder inmediatamente enviando el byte `W` (si el nuevo modo es Web) o `J` (si es Manual) al ESP32 para confirmar y sincronizar el estado.

