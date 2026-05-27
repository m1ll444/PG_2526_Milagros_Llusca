## MODIFIED Requirements

### Requirement: Protocolo y Set de Comandos
El protocolo SHALL consistir en enviar un solo carácter ASCII correspondiente a la acción deseada. Los comandos válidos son:
- `F` (Forward / Adelante): Mueve el carro hacia adelante
- `B` (Backward / Atrás): Mueve el carro hacia atrás
- `U` (Up / Subir): Eleva el gancho
- `D` (Down / Bajar): Desciende el gancho
- `L` (Left / Izquierda): Giro antihorario del brazo de la grúa
- `R` (Right / Derecha): Giro horario del brazo de la grúa
- `S` (Stop / Parar): Detiene todos los movimientos de forma inmediata
- `M` (Mode / Modo): Conmuta el modo de control entre Web y Manual
- `W` (Web status): Mensaje de estado enviado desde Arduino al ESP32 indicando que el modo actual es Web
- `J` (Joystick status): Mensaje de estado enviado desde Arduino al ESP32 indicando que el modo actual es Manual

#### Scenario: Envío de comando de cambio de modo desde la web
- **WHEN** El usuario activa el switch de modo en la interfaz web.
- **THEN** El ESP32 SHALL escribir el byte `M` por el puerto serie.

#### Scenario: Arduino informa estado de modo al ESP32
- **WHEN** El modo de control cambia (por botón físico o comando web).
- **THEN** El Arduino SHALL enviar `W` (si el nuevo modo es Web) o `J` (si el nuevo modo es Manual) por el puerto serie al ESP32.

#### Scenario: Envío de comando de movimiento desde la web
- **WHEN** El usuario presiona el botón "Adelante" (F) en la interfaz web del ESP32.
- **THEN** El ESP32 SHALL escribir el byte `F` por el puerto serie.

#### Scenario: Envío de comando de parada (STOP)
- **WHEN** El usuario suelta cualquier botón de movimiento o presiona "STOP" en la interfaz.
- **THEN** El ESP32 SHALL escribir el byte `S` por el puerto serie.
