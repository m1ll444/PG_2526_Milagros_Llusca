# Capacidad: Esquema de Conexiones Electrónicas (Schema.html)

## Purpose
Define el documento interactivo autocontenido `Schema.html` que visualiza el diagrama de bloques del hardware y la tabla detallada de conexiones pin-a-pin del sistema de control de la grúa torre.

## Requirements

### Requirement: Documento Web Autocontenido y Responsivo
El sistema SHALL contar con un archivo `Schema.html` en la raíz del proyecto estructurado de la siguiente forma:
- Un diseño responsivo con tema oscuro y glassmorphism.
- Fuente tipográfica Inter de Google.
- Un diagrama de bloques en formato SVG inline interactivo y escalable.
- Una tabla de conexiones pin-a-pin con motor de búsqueda y filtrado dinámico en tiempo real implementado en JavaScript vanilla.

#### Scenario: Visualización del diagrama de bloques
- **WHEN** El usuario abre `Schema.html` en cualquier navegador web moderno.
- **THEN** Se SHALL renderizar un diagrama SVG que muestre los bloques de ESP32, Arduino, los dos drivers TB6612FNG, los tres motores, los joysticks y la fuente de alimentación, conectados con líneas de colores representativos según el tipo de señal (UART, PWM, Digital, Analógica, Potencia).

#### Scenario: Filtrado en la tabla de conexiones pin-a-pin
- **WHEN** El usuario ingresa un término de búsqueda (ej. "D3" o "UART") en la caja de texto superior.
- **THEN** Las filas de la tabla de conexiones SHALL filtrarse instantáneamente por JavaScript para mostrar únicamente las conexiones que contengan dicho término, ocultando las demás mediante estilos CSS (`display: none`).
