## ADDED Requirements

### Requirement: Archivo de diagrama de conexiones electrónicas
El proyecto SHALL incluir un archivo `Schema.html` en la raíz del repositorio que documente visualmente todas las conexiones electrónicas del sistema.

#### Scenario: Visualización del diagrama de conexiones
- **WHEN** El usuario abre el archivo `Schema.html` en un navegador web.
- **THEN** El archivo SHALL mostrar un diagrama de bloques visual organizado por subsistemas (ESP32, Arduino, drivers, motores, joysticks, alimentación) con líneas de conexión coloreadas por tipo de señal.

### Requirement: Tabla pin-a-pin detallada
El archivo `Schema.html` SHALL incluir una tabla detallada que liste cada conexión física del sistema con columna de origen, destino, tipo de señal y observaciones.

#### Scenario: Consulta de conexión específica en la tabla
- **WHEN** El usuario busca la conexión del motor de carro en la tabla pin-a-pin.
- **THEN** La tabla SHALL mostrar los pines de origen en el Arduino (D2, D4, D3), el destino en el driver TB6612FNG (AIN1, AIN2, PWMA), el tipo de señal (Digital/PWM) y las observaciones relevantes.
