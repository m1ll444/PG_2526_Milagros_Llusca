## MODIFIED Requirements

### Requirement: Prioridad del Control Manual (Joystick Override)
El sistema SHALL operar en modo mutuamente excluyente. En Modo Manual, el Arduino SHALL responder exclusivamente a los joysticks analógicos. En Modo Web, el Arduino SHALL responder exclusivamente a los comandos UART. La conmutación entre modos SHALL realizarse mediante el botón físico del joystick (pin D6) o el switch de la interfaz web.

#### Scenario: Modo Manual activo con comando web recibido
- **WHEN** El sistema está en Modo Manual y se recibe un comando web `F` (Carro adelante) por UART.
- **THEN** El Arduino SHALL ignorar el comando web y los motores SHALL responder únicamente a los joysticks.

#### Scenario: Modo Web activo con joystick movido
- **WHEN** El sistema está en Modo Web y el joystick de carro lee 200 (fuera de zona muerta).
- **THEN** El Arduino SHALL ignorar la lectura del joystick y los motores SHALL responder únicamente a los comandos web.

### Requirement: Temporización de Seguridad de Red (Web Timeout)
El sistema SHALL implementar un mecanismo de temporización de seguridad. Si no se recibe ningún comando web válido en un lapso mayor a 500 ms mientras el sistema está en Modo Web, los motores SHALL detenerse automáticamente. En Modo Manual, el timeout de red SHALL estar desactivado.

#### Scenario: Detención por pérdida de comunicación en Modo Web
- **WHEN** El sistema está en Modo Web ejecutando el comando `U` (Subir) y transcurren más de 500 ms sin recibir ningún mensaje serie nuevo.
- **THEN** El Arduino SHALL detener todos los motores inmediatamente.

#### Scenario: Timeout no aplica en Modo Manual
- **WHEN** El sistema está en Modo Manual y no se reciben comandos web durante más de 500 ms.
- **THEN** El Arduino SHALL continuar respondiendo normalmente a los joysticks sin detenerse.
