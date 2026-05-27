# Tasks

Plan de tareas estructurado para la renovación del esquema electrónico interactivo `Schema.html` de la grúa torre.

---

## Tarea 1: Rediseño Estético de Componentes y Ruteo del SVG

- [ ] **Estructurar la sección de definiciones (`<defs>`)**:
  - [ ] Crear gradientes de fondo premium para los bloques de hardware.
  - [ ] Declarar el filtro de brillo SVG (`#glow-effect`) para destacar cables activos.
  - [ ] Definir los marcadores (`markers`) de inicio/fin de cables para conectar limpiamente en los pines.
- [ ] **Rediseñar los Bloques de Hardware**:
  - [ ] **ESP32 DevKit V1**: Agregar ilustración digital moderna con pines físicos etiquetados (TX2, RX2, VIN, GND) y el LED de comunicación de estado.
  - [ ] **Arduino Nano**: Rediseñar la placa con pines etiquetados y ordenados (D0-D12, A0-A2, VIN, GND, 5V).
  - [ ] **Drivers TB6612FNG (1 y 2)**: Agregar etiquetas detalladas para pines de entrada (VCC, GND, Ctrl, PWM, STBY) y pines de salida a motores.
  - [ ] **Joysticks (1 y 2)**: Agregar representación circular con joystick y botones, etiquetando 5V, GND, VRX, VRY y SW.
  - [ ] **Fuente 12V**: Ilustrar un módulo de fuente de alimentación con regletas de terminales etiquetadas.
  - [ ] **Motores DC (Carro, Elevación, Giro)**: Crear ilustraciones técnicas estilizadas de motores con bornes positivos/negativos.
- [ ] **Realizar el Trazado Manhattan Ortogonal (25 Cables)**:
  - [ ] Corregir conexión `Joy1 VRY` (Giro) $\rightarrow$ Arduino `A2` (Giro).
  - [ ] Corregir conexión `Joy2 VRX` (Elevación) $\rightarrow$ Arduino `A1` (Elevación).
  - [ ] Trazar las 6 nuevas líneas de alimentación (12V a VIN Arduino, 5V a ESP32, drivers logic, STBY pins, Joysticks logic).
  - [ ] Trazar el bus de tierra común (`GND`) interconectando todas las placas hacia la fuente.
  - [ ] Asegurar que todos los cables viajen en ángulos de 90° y desemboquen exactamente en los círculos de pin correspondientes.

---

## Tarea 2: Implementación de CSS Premium y Glassmorphism

- [ ] **Definir Variables de Tema Dinámicas**:
  - [ ] Actualizar colores en `:root` y `.dark-mode` con paleta HSL premium para modo claro y modo oscuro profundo.
  - [ ] Agregar variable CSS `--active-wire-color` para teñir los bordes dinámicamente.
- [ ] **Estilizar la Tarjeta de Información e Interacción**:
  - [ ] Estilizar el `.info-panel` con un glassmorphism translúcido de alta definición (desenfoque `backdrop-filter: blur(16px)`).
  - [ ] Crear estructura interna del panel (cabecera con "badges" dinámicos, columnas "¿Qué hace?" y "¿Por qué?").
  - [ ] Diseñar el botón premium de restablecer selección ("Liberar Selección ✕").
- [ ] **Estilos Interactivos para Cables Activos**:
  - [ ] Agregar clase CSS `.active` con animación fluida de flujo (`pulseFlow` con `stroke-dasharray` y `stroke-dashoffset`).
  - [ ] Definir transición suave de brillo para cables al hacer hover y click.

---

## Tarea 3: Desarrollo de Lógica JavaScript Interactiva y Sincronización

- [ ] **Desarrollar Base de Datos del Cableado en JS**:
  - [ ] Crear el objeto `connectionData` en JavaScript con descripciones completas, justificaciones técnicas y colores para cada uno de los 25 cables.
- [ ] **Implementar Mecanismo "Click & Lock"**:
  - [ ] Añadir escuchas de eventos de clic a cada ruta de cable.
  - [ ] Al hacer clic, fijar la selección, aplicar brillo/animación de flujo y actualizar el panel de información de forma persistente.
  - [ ] Deshabilitar temporalmente los efectos visuales del hover común en otros cables mientras el actual esté bloqueado.
  - [ ] Programar el botón "Liberar Selección ✕" y clic en el fondo del SVG para limpiar el estado y restaurar textos por defecto.
- [ ] **Sincronizar Bidireccionalmente SVG $\leftrightarrow$ Tabla**:
  - [ ] Al hacer clic en un cable, resaltar la fila correspondiente en la tabla pin-a-pin y hacer scroll suave (`scrollIntoView`).
  - [ ] Al escribir en la caja de búsqueda, filtrar las filas de la tabla y añadir la clase `.inactive-wire` (opacidad del 15% y escala de grises) a las rutas SVG cuyos datos no coincidan con el texto de búsqueda.

---

## Tarea 4: Actualización de la Tabla Pin-a-Pin

- [ ] **Ampliar la Estructura de la Tabla**:
  - [ ] Agregar las 6 conexiones de alimentación, lógica y tierras nuevas en la estructura `<tbody>`.
  - [ ] Actualizar nombres de pines corregidos (A2 para Joystick 1 VRY y A1 para Joystick 2 VRX).
  - [ ] Totalizar las 25 conexiones físicas reales del circuito electrónico.
  - [ ] Aplicar estilo premium a las filas, celdas y etiquetas (`.tag-vcc`, `.tag-gnd`, `.tag-power`, etc.) alineados al nuevo diseño.

---

## Tarea 5: Validación Técnica y Pruebas

- [ ] **Validación de Funcionalidad e Interactividad**:
  - [ ] Verificar que cada uno de los 25 cables sea cliqueable y active su brillo y animación de flujo de forma correcta.
  - [ ] Comprobar que el texto "¿Qué hace?" y "¿Por qué?" describa con precisión y profesionalismo cada conexión.
  - [ ] Probar el botón de liberar selección y el clic de fondo.
  - [ ] Validar que la sincronización bidireccional funcione (el buscador atenúe los cables inactivos y el clic resalte la fila).
- [ ] **Pruebas de Visualización**:
  - [ ] Comprobar que el diseño responsivo se adapte correctamente a pantallas de escritorio y teléfonos móviles.
  - [ ] Validar la consistencia y transiciones de colores entre Modo Claro y Modo Oscuro.
  - [ ] Comprobar la ausencia total de cruces caóticos o cables descentrados del pin en el SVG.
