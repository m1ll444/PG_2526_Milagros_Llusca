## ADDED Requirements

### Requirement: Trazas de depuración de motores por SoftwareSerial
El Arduino SHALL emitir trazas de depuración por el canal SoftwareSerial (pin D13 TX) que informen del estado operativo de los motores cuando se producen cambios de estado relevantes.

#### Scenario: Log al iniciar movimiento de un motor
- **WHEN** Un motor pasa del estado detenido a un estado de movimiento (por comando web o joystick).
- **THEN** El Arduino SHALL enviar una traza por SoftwareSerial como `[MOT] Carro: Adelante (PWM=255)`.

#### Scenario: Log al detener un motor por timeout web
- **WHEN** El timeout de seguridad web (500ms) se activa y detiene los motores.
- **THEN** El Arduino SHALL enviar una traza `[SAFE] Timeout web - motores detenidos` por SoftwareSerial.
