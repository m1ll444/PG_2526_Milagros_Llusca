# navegacion-cruzada Specification

## Purpose
TBD - created by archiving change usb-control-wifi-debug. Update Purpose after archive.
## Requirements
### Requirement: Barra de navegación cruzada
Las páginas `index.html` y `schema.html` SHALL incluir una barra de navegación en la parte superior del encabezado con enlaces interactivos que permitan al usuario saltar bidireccionalmente entre la interfaz de control y el esquema de conexiones.

#### Scenario: Navegación desde la interfaz de control al esquema
- **WHEN** El usuario hace clic en el enlace "Esquema" en la barra de navegación de `index.html`.
- **THEN** El navegador SHALL cargar la página `schema.html` en la misma pestaña.

#### Scenario: Navegación desde el esquema a la interfaz de control
- **WHEN** El usuario hace clic en el enlace "Control" en la barra de navegación de `schema.html`.
- **THEN** El navegador SHALL cargar la página `index.html` en la misma pestaña.

