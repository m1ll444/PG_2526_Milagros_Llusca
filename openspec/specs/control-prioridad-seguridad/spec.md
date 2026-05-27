# Capacidad: Lógica de Control Dual y Seguridad

## Purpose
Describe las reglas de negocio para integrar de forma segura el control por joysticks analógicos y la interfaz web remota, protegiendo al hardware ante pérdidas de señal o conflictos de entrada.

## Requirements

### Requirement: Zona Muerta de Joysticks (Deadband)
El sistema SHALL establecer una zona muerta central en los joysticks analógicos (rango de lectura 0-1023) para evitar movimientos espurios por ruido eléctrico. El rango de inactividad SHALL ser de 400 a 600. Cualquier valor inferior a 400 o superior a 600 se considera una entrada manual activa.

#### Scenario: Joystick en zona muerta sin comando web
- **WHEN** El joystick de un eje lee un valor entre 400 y 600 y no hay comando web activo.
- **THEN** El motor correspondiente a ese eje SHALL permanecer detenido.

#### Scenario: Joystick fuera de zona muerta
- **WHEN** El joystick de carro lee un valor de 200 (inferior a 400).
- **THEN** El sistema SHALL interpretar la lectura como una entrada manual activa y mover el carro con velocidad proporcional al desplazamiento.

### Requirement: Modo de Control Exclusivo (Web o Manual/Joystick)
El sistema SHALL operar en un modo de control exclusivo (Web o Manual) determinado por el estado de `modoWeb`. Las entradas del canal inactivo SHALL ser ignoradas por completo para evitar conflictos de control.

#### Scenario: Control por Web Activo
- **WHEN** El estado de control es Web (`modoWeb == true`).
- **THEN** El Arduino Nano/Uno SHALL responder únicamente a los comandos UART provenientes del ESP32 e ignorar por completo las lecturas analógicas de los joysticks (incluso si están fuera de la zona muerta).

#### Scenario: Control por Joystick Activo
- **WHEN** El estado de control es Manual (`modoWeb == false`).
- **THEN** El Arduino Nano/Uno SHALL responder únicamente a los desplazamientos de los joysticks e ignorar cualquier comando de movimiento web recibido por UART.

### Requirement: Temporización de Seguridad de Red (Web Timeout)
El sistema SHALL implementar un mecanismo de temporización de seguridad. Si no se recibe ningún comando web válido en un lapso mayor a 500 ms y el modo de control activo es Web, la variable `webCommand` SHALL restablecerse automáticamente a `S` (Stop).

#### Scenario: Detención por pérdida de comunicación web
- **WHEN** El estado es Web (`modoWeb == true`), se estaba ejecutando el comando web `U` (Subir) y transcurren más de 500 ms sin recibir ningún mensaje serie nuevo.
- **THEN** El Arduino SHALL actualizar `webCommand` a `S` y detener el motor de elevación inmediatamente.

#### Scenario: Renovación de timeout por comando continuo
- **WHEN** El cliente web envía el comando `U` cada 100 ms de forma continua.
- **THEN** La marca de tiempo `lastWebCommandTime` SHALL actualizarse con cada comando recibido, manteniendo el movimiento activo sin interrupciones por timeout.

#### Scenario: Timeout desactivado en modo manual
- **WHEN** El estado de control es Manual (`modoWeb == false`).
- **THEN** El mecanismo de temporización de seguridad por pérdida de comunicación web SHALL desactivarse para evitar la detención de los movimientos manuales por falta de comandos de red.

