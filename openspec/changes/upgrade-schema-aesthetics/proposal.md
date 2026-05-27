## Why

El esquema de conexiones electrónicas interactivo del sistema de grúa torre (`Schema.html`) necesita una renovación integral tanto en precisión técnica como en estética visual por las siguientes razones:

1. **Discrepancias de Cableado (Errores de Señal):** En el diagrama SVG actual, los cables físicos de control analógico para Giro (`Joy1 VRY`) y Elevación (`Joy2 VRX`) están cruzados en relación con el firmware y la tabla (Giro se dibujaba en A1 y Elevación en A2, cuando en la práctica es al revés). Esto confunde la lectura técnica.
2. **Conexiones Críticas Ausentes (Alimentación y Lógica):** Faltan las líneas físicas de alimentación de los microcontroladores (12V a Arduino VIN, 5V de Arduino a ESP32 VIN), la energía lógica de los drivers (`VCC`), el pin indispensable de habilitación `STBY` de ambos puentes H (que deben estar puenteados a 5V) y la tierra común indispensable para el acoplamiento UART.
3. **Limitación de Interactividad (Click & Lock):** El sistema actual solo muestra información técnica al pasar el cursor (hover). Al retirar el cursor, la información desaparece. Se requiere que al presionar (hacer clic) en un cable, la selección quede "bloqueada" y activa para permitir una lectura tranquila, junto con una explicación clara de **qué hace** y **por qué se conectó así**.
4. **Calidad Estética Básica:** El diagrama SVG original conecta líneas simples a los bordes exteriores de los bloques en lugar de apuntar a los pines específicos etiquetados de los componentes. Se necesita un aspecto premium, limpio y de calidad profesional para el proyecto.

## What Changes

- **Corregir** la conexión de los Joysticks en el SVG: `Joy1 VRY` (Giro) va a `A2` y `Joy2 VRX` (Elevación) va a `A1`.
- **Agregar** cableado de alimentación principal de 12V desde la fuente al pin `VIN` del Arduino Nano.
- **Agregar** bus de alimentación lógica de 5V desde el pin `5V` de Arduino hacia:
  - Pin `VIN` de ESP32.
  - Pines `VCC` y `STBY` de ambos drivers TB6612FNG.
  - Pines `5V` de Joystick 1 y Joystick 2.
- **Agregar** bus de tierra común (`GND`) interconectando la fuente, Arduino, ESP32, ambos drivers y joysticks.
- **Rediseñar** visualmente los componentes del SVG para representar placas reales con pines específicos, conectando cada cable ortogonalmente (giros de 90°) directo a sus respectivos círculos de pin.
- **Agregar** filtros de brillo de neón SVG (`feGaussianBlur`) y clase CSS `.active` para iluminar cables seleccionados.
- **Agregar** animación de pulsos de luz en movimiento (`stroke-dashoffset` animado) para indicar la dirección y flujo del cable activo.
- **Agregar** interactividad de clic y bloqueo ("Click & Lock") en JavaScript para mantener la información seleccionada y mostrar un botón para liberar el bloqueo.
- **Renovar** el panel `.info-panel` con un diseño glassmorphic de alto contraste, bordes que cambian de color dinámicamente según el cable seleccionado, y secciones claras: "¿Qué hace?" y "¿Por qué?".
- **Sincronizar** bidireccionalmente el SVG y la Tabla: al hacer clic en un cable se resalta su fila en la tabla, y al buscar/filtrar en la tabla se atenúan los cables no coincidentes en el SVG.
- **Expandir** la tabla de asignación de pines de 19 a 25 filas para incluir detalladamente todas las nuevas conexiones de alimentación lógica, STBY y tierras comunes.

## Capabilities

### New Capabilities
- `schema-conexiones-premium`: Visualización y documentación interactiva avanzada del conexionado electrónico que permite bloquear selecciones por clic, observar animaciones dinámicas del flujo de señales, y comprender a nivel de ingeniería la función y el porqué de cada cableado físico, con un diseño glassmorphism de alta estética y sincronización bidireccional de tabla.

### Modified Capabilities
- `schema-conexiones`: Sustituida y superada por la nueva capacidad premium con precisión del 100% en los pines físicos de los microcontroladores y drivers.

## Impact

- **Archivo Web de Conexiones** (`Schema.html`): Reemplazo completo del archivo en la raíz con un nuevo diseño estético espectacular, SVG con 25 cables ortogonales perfectos, estilos CSS modernos para modo claro/oscuro y lógica JS mejorada para interactividad de clic y bloqueo.
- **Documentación física**: Se alinea al 100% con los pines configurados en el firmware real del Arduino (`grua_arduino.ino`) y ESP32 (`main.py`), eliminando las discrepancias de control de motores y modos.
