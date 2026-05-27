## REMOVED Requirements

### Requirement: Control de Giro (Motor Paso a Paso)
**Reason**: El motor paso a paso NEMA 17 con driver DRV8825 ha sido reemplazado por un motoreductor DC de 30RPM controlado por un segundo módulo TB6612FNG.
**Migration**: Utilizar el nuevo requerimiento "Control de Giro (Motoreductor DC)" que emplea el canal A del segundo TB6612FNG con control PWM + dirección.

## ADDED Requirements

### Requirement: Control de Giro (Motoreductor DC)
El sistema SHALL controlar el motoreductor DC de 30RPM para el eje de giro mediante el canal A del segundo módulo TB6612FNG, usando los pines:
- `CIN1` (D11): Dirección 1.
- `CIN2` (D12): Dirección 2.
- `PWMC` (D9): Velocidad analógica por ciclo de trabajo (PWM, rango 0-255).

#### Scenario: Giro horario a velocidad máxima configurada
- **WHEN** El comando activo es giro horario y la velocidad solicitada es máxima.
- **THEN** El pin `CIN1` SHALL ponerse en HIGH, `CIN2` en LOW, y se SHALL generar una señal PWM igual a `MAX_SPEED_GIRO` en el pin `PWMC`.

#### Scenario: Detención del motor de giro
- **WHEN** Se invoca la función de detención del giro.
- **THEN** Los pines `CIN1` y `CIN2` SHALL ponerse en LOW y el PWM en `PWMC` SHALL ponerse en 0.

### Requirement: Velocidades máximas configurables por motor
El firmware Arduino SHALL definir constantes de velocidad máxima individuales para cada motor:
- `MAX_SPEED_CARRO`: Velocidad máxima del motor del carro (valor PWM 0-255).
- `MAX_SPEED_ELEVACION`: Velocidad máxima del motor de elevación (valor PWM 0-255).
- `MAX_SPEED_GIRO`: Velocidad máxima del motoreductor de giro (valor PWM 0-255).
Los comandos web SHALL utilizar estas constantes como velocidad de operación. Los joysticks SHALL mapear su rango analógico proporcionalmente hasta el valor máximo configurado.

#### Scenario: Comando web usa velocidad máxima configurada
- **WHEN** El sistema está en Modo Web y el comando activo es `F` (Carro adelante).
- **THEN** El motor del carro SHALL moverse con señal PWM igual a `MAX_SPEED_CARRO` (en lugar del valor fijo 255).

#### Scenario: Joystick mapea velocidad proporcional al máximo configurado
- **WHEN** El sistema está en Modo Manual y el joystick de elevación lee 1023 (máximo desplazamiento).
- **THEN** El motor de elevación SHALL moverse con señal PWM igual a `MAX_SPEED_ELEVACION`.
