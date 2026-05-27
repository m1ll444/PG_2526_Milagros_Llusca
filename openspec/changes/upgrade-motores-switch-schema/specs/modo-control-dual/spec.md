## ADDED Requirements

### Requirement: Conmutación de modo de control
El sistema SHALL soportar dos modos de operación mutuamente excluyentes: Modo Web y Modo Manual. Solo uno de los dos modos SHALL estar activo en cualquier momento. El modo por defecto al encender el sistema SHALL ser Modo Manual.

#### Scenario: Cambio de modo mediante botón físico
- **WHEN** El operador presiona el botón físico del joystick conectado al pin D6 del Arduino.
- **THEN** El Arduino SHALL conmutar el modo de control (de Manual a Web o viceversa) y enviar el nuevo estado al ESP32 vía UART.

#### Scenario: Cambio de modo mediante switch en la interfaz web
- **WHEN** El operador activa el switch de modo en la interfaz web.
- **THEN** El ESP32 SHALL enviar el comando de cambio de modo al Arduino vía UART y actualizar la interfaz para reflejar el nuevo estado.

### Requirement: Comportamiento en Modo Manual
Cuando el sistema está en Modo Manual, el Arduino SHALL responder exclusivamente a los joysticks analógicos y SHALL ignorar todos los comandos de movimiento recibidos por UART desde la web.

#### Scenario: Comando web ignorado en Modo Manual
- **WHEN** El sistema está en Modo Manual y se recibe un comando web `F` (Adelante) por UART.
- **THEN** El Arduino SHALL ignorar el comando y los motores SHALL responder únicamente a los joysticks.

### Requirement: Comportamiento en Modo Web
Cuando el sistema está en Modo Web, el Arduino SHALL responder exclusivamente a los comandos recibidos por UART desde la interfaz web y SHALL ignorar las lecturas de los joysticks analógicos.

#### Scenario: Joystick ignorado en Modo Web
- **WHEN** El sistema está en Modo Web y el joystick de carro lee 200 (fuera de zona muerta).
- **THEN** El Arduino SHALL ignorar la lectura del joystick y los motores SHALL responder únicamente a los comandos web.

### Requirement: Indicador visual de modo en la interfaz web
La interfaz web SHALL mostrar un switch toggle y un indicador textual que refleje claramente el modo de control activo (Web o Manual). El switch SHALL sincronizarse con el estado real del Arduino.

#### Scenario: Visualización del modo activo
- **WHEN** El modo de control cambia a Modo Web (por cualquier fuente).
- **THEN** La interfaz web SHALL mostrar el switch en posición "Web" y un indicador visual que confirme el modo activo.
