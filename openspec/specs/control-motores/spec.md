# Capacidad: Control de Actuadores y Motores (Arduino)

## Purpose
Define cómo el Arduino procesa los comandos físicos y lógicos para regular la dirección y velocidad de los tres motores de la grúa torre.

## Requirements

### Requirement: Control del Carro (Motor DC A)
El sistema SHALL controlar el motor DC N20 (12V) del carro mediante la mitad A del driver puente H TB6612FNG con los siguientes pines:
- `AIN1` (D2) y `AIN2` (D4): Dirección.
- `PWMA` (D3): Velocidad analógica por ciclo de trabajo (PWM, rango 0-255).

#### Scenario: Movimiento del carro adelante a máxima velocidad
- **WHEN** El comando activo es adelante y la velocidad solicitada es máxima.
- **THEN** El pin `AIN1` SHALL ponerse en HIGH, `AIN2` en LOW, y se SHALL generar una señal PWM de valor 255 en el pin `PWMA`.

#### Scenario: Detención del motor del carro
- **WHEN** Se invoca la función de detención del carro.
- **THEN** Los pines `AIN1` y `AIN2` SHALL ponerse en LOW y el PWM en `PWMA` SHALL ponerse en 0.

### Requirement: Control de Elevación (Motor DC B)
El sistema SHALL controlar el motor DC N20 (12V) de elevación mediante la mitad B del driver puente H TB6612FNG con los siguientes pines:
- `BIN1` (D7) y `BIN2` (D8): Dirección.
- `PWMB` (D5): Velocidad analógica por ciclo de trabajo (PWM, rango 0-255).

#### Scenario: Elevación del gancho a máxima velocidad
- **WHEN** El comando activo es subir y la velocidad solicitada es máxima.
- **THEN** El pin `BIN1` SHALL ponerse en HIGH, `BIN2` en LOW, y se SHALL generar una señal PWM de valor 255 en el pin `PWMB`.

#### Scenario: Detención del motor de elevación
- **WHEN** Se invoca la función de detención de elevación.
- **THEN** Los pines `BIN1` y `BIN2` SHALL ponerse en LOW y el PWM en `PWMB` SHALL ponerse en 0.

### Requirement: Control de Giro (Motorreductor DC)
El sistema SHALL controlar el motorreductor DC de giro (30RPM, 12V) mediante el canal C de un segundo driver puente H TB6612FNG con los siguientes pines:
- `CIN1` (D11) y `CIN2` (D12): Dirección.
- `PWMC` (D9): Velocidad analógica por ciclo de trabajo (PWM, rango 0-MAX_SPEED_GIRO).

#### Scenario: Giro manual con joystick hacia la derecha
- **WHEN** El joystick Z se desplaza a la derecha (lectura superior a 600) en modo manual.
- **THEN** El pin `CIN1` SHALL ponerse en HIGH, `CIN2` en LOW, y se SHALL generar una señal PWM proporcional al desplazamiento en el pin `PWMC` (mapeada en el rango 0-MAX_SPEED_GIRO).

#### Scenario: Giro por comando web a velocidad fija
- **WHEN** El modo activo es Web y el comando web activo es `R` (giro horario).
- **THEN** El pin `CIN1` SHALL ponerse en HIGH, `CIN2` en LOW, y se SHALL generar una señal PWM de valor `MAX_SPEED_GIRO` en el pin `PWMC`.

### Requirement: Velocidades Máximas Configurables
El sistema SHALL permitir configurar de forma independiente el límite superior de velocidad (rango PWM de 0 a 255) para cada motor mediante constantes configurables en el firmware:
- `MAX_SPEED_CARRO` para el motor del carro (por defecto 255).
- `MAX_SPEED_ELEVACION` para el motor de elevación (por defecto 255).
- `MAX_SPEED_GIRO` para el motor de giro (por defecto 200).

#### Scenario: Límite de velocidad en comando web
- **WHEN** Se ejecuta un comando web de movimiento (por ejemplo, `F` o `R`).
- **THEN** La velocidad máxima aplicada al pin PWM correspondiente SHALL estar limitada por la constante `MAX_SPEED_*` respectiva.

