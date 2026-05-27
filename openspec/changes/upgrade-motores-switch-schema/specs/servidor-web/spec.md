## ADDED Requirements

### Requirement: Switch de modo de control en la interfaz web
La interfaz web SHALL incluir un componente switch toggle que permita al usuario cambiar entre Modo Web y Modo Manual. El switch SHALL estar posicionado de forma visible en la parte superior del panel de control.

#### Scenario: Activación de Modo Web desde la interfaz
- **WHEN** El usuario activa el switch de modo a posición "Web" en la interfaz.
- **THEN** La interfaz SHALL enviar una petición HTTP GET a `/cmd?action=M` y actualizar el estado visual del switch.

#### Scenario: Deshabilitación de controles en Modo Manual
- **WHEN** El modo activo es Manual.
- **THEN** La interfaz web SHALL mostrar los botones de movimiento visualmente deshabilitados (opacidad reducida) y SHALL impedir el envío de comandos de movimiento.

### Requirement: Endpoint de estado del modo
El servidor web del ESP32 SHALL exponer el endpoint `GET /mode` que devuelva el estado actual del modo de control en texto plano (`WEB` o `MANUAL`).

#### Scenario: Consulta del estado de modo
- **WHEN** La interfaz web realiza una petición GET a `/mode`.
- **THEN** El servidor SHALL devolver el estado actual del modo (`WEB` o `MANUAL`) con cabecera `200 OK`.
