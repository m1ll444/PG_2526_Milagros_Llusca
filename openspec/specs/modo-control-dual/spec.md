# Capacidad: Modo de Control Dual (Web / Manual)

## Purpose
Define la capacidad de conmutar entre el modo de control web y el modo manual (joystick) utilizando un botón físico en el joystick o un switch en la interfaz web, asegurando una transición segura donde los motores se detienen y el estado se sincroniza bidireccionalmente.

## Requirements

### Requirement: Conmutación por Botón Físico
El sistema SHALL permitir alternar el modo de control mediante el botón pulsador del joystick conectado al pin `BUTTON_MODE_PIN` (D6) del Arduino Nano/Uno con resistencia pull-up interna activa y filtro anti-rebote (debounce) de al menos 50 ms.

#### Scenario: Pulsación del botón de modo físico
- **WHEN** El operador presiona el botón físico del joystick (flanco de bajada detectado tras el debounce).
- **THEN** El Arduino Nano/Uno SHALL conmutar la variable global `modoWeb`, detener todos los motores inmediatamente, y enviar el nuevo estado (`W` para Web, `J` para Manual) por UART al ESP32.

### Requirement: Conmutación por Interfaz Web
El sistema SHALL permitir alternar el modo de control desde el navegador web mediante un switch virtual.

#### Scenario: Clic en el switch de la interfaz web
- **WHEN** El usuario acciona el switch en la página web.
- **THEN** El navegador SHALL realizar una petición `GET /cmd?action=M` al ESP32, el cual transmitirá el byte `M` por UART al Arduino. Al recibirlo, el Arduino Nano/Uno SHALL alternar `modoWeb`, detener todos los motores inmediatamente, y responder enviando `W` o `J` de vuelta por UART para confirmar el cambio.

### Requirement: Sincronización de Estado Bidireccional
El ESP32 y la interfaz web SHALL sincronizar su estado con la confirmación enviada por el Arduino.

#### Scenario: Recepción de confirmación en ESP32
- **WHEN** El ESP32 recibe el byte `W` o `J` a través de la interfaz UART desde el Arduino.
- **THEN** El ESP32 SHALL actualizar su variable de estado interna `current_mode` a `WEB` o `MANUAL` respectivamente, de modo que al ser consultada vía `/mode` se retorne el valor correcto.
