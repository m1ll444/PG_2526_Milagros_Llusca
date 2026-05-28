## MODIFIED Requirements

### Requirement: Configuración de Interfaz Serie Bidireccional
La comunicación física SHALL realizarse mediante dos canales serie independientes:
- **Canal Principal (Serial hardware, USB):** Comunicación bidireccional entre el Arduino y el navegador web vía cable USB a 9600 bps. Pines D0 (RX) y D1 (TX) del Arduino.
- **Canal Secundario (SoftwareSerial, depuración):** Comunicación unidireccional desde el Arduino (TX en pin D13) hacia el ESP32 (RX en GPIO 16) a 9600 bps para trazas de depuración.

#### Scenario: Inicialización de ambos canales serie
- **WHEN** El Arduino arranca en su rutina `setup()`.
- **THEN** El sistema SHALL inicializar `Serial` (hardware) a 9600 bps para comunicación USB con el navegador, y `SoftwareSerial` en pines D10/D13 a 9600 bps para envío de logs al ESP32.

### Requirement: Protocolo y Set de Comandos de Movimiento y Modo
El protocolo de comandos de movimiento y modo SHALL operar por el canal Serial hardware (USB). Los comandos válidos son:
- **Comandos de movimiento (Navegador → Arduino):** `F`, `B`, `U`, `D`, `L`, `R`, `S`
- **Comando de cambio de modo (Navegador → Arduino):** `M`
- **Telemetría (Arduino → Navegador):** Tramas en formato `S:<modo>,<carro>,<elev>,<giro>\n` cada 100ms.

#### Scenario: Recepción de comando por USB desde Web Serial
- **WHEN** El navegador envía el byte `F` por Web Serial API al Arduino.
- **THEN** El Arduino SHALL almacenar el comando en la variable `webCommand`, actualizar `lastWebCommandTime`, y enviar una traza `[CMD] Recibido: F` por SoftwareSerial al ESP32.

#### Scenario: Envío de telemetría por USB al navegador
- **WHEN** Transcurren 100ms desde la última trama de telemetría.
- **THEN** El Arduino SHALL enviar una trama `S:W,F,S,S\n` por el Serial hardware USB para que el navegador la lea vía Web Serial API.
