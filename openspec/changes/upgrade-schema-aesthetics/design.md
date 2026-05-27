## Context

El esquema actual (`Schema.html`) presenta un diseño simple con cajas de componentes abstractas y cables de señal que conectan a sus bordes de manera imprecisa. Adicionalmente, cuenta con solo 19 conexiones mapeadas, tiene cables de señales cruzados y carece de detalles esenciales para que el circuito funcione físicamente (como la alimentación del ESP32, Arduino y la habilitación STBY de los drivers).

### Estado de Conexiones a Corregir y Agregar:
1. **Swap de Joystick:**
   - Giro: `Joystick 1 VRY` $\rightarrow$ Arduino `A2` (Estaba dibujado en `A1`).
   - Elevación: `Joystick 2 VRX` $\rightarrow$ Arduino `A1` (Estaba dibujado en `A2`).
2. **Conexiones Eléctricas Nuevas (Añadidas para el 100% de coherencia):**
   - `Fuente 12V (+12V)` $\rightarrow$ `Arduino VIN`
   - `Arduino 5V` $\rightarrow$ `ESP32 VIN`
   - `Arduino 5V` $\rightarrow$ `TB6612FNG #1 VCC` y `TB6612FNG #2 VCC` (Lógica de drivers)
   - `Arduino 5V` $\rightarrow$ `TB6612FNG #1 STBY` y `TB6612FNG #2 STBY` (Pines de habilitación)
   - `Tierra Común` $\rightarrow$ Interconexión de todos los GNDs (`Fuente GND`, `Arduino GND`, `ESP32 GND`, `Joysticks GND`, `Drivers GND`).

---

## Goals / Non-Goals

**Goals:**
- Asegurar 100% de precisión técnica alineada con el firmware real del Arduino y ESP32.
- Lograr una estética premium espectacular: trazado ortogonal limpio (Manhattan), bordes redondos de cables y representación detallada de placas.
- Implementar sistema "Click & Lock" interactivo en los cables, permitiendo visualizar los textos "¿Qué hace?" y "¿Por qué se conectó así?".
- Crear animaciones fluidas del flujo de señal (pulsos móviles de neón) exclusivas del cable seleccionado.
- Rediseñar el panel de detalles con glassmorphism de alta definición, bordes dinámicos que se tiñen según el color del cable y botón para liberar selección.
- Integrar la tabla de asignación de pines bidireccionalmente con el SVG (resaltado y atenuación mutua).

**Non-Goals:**
- No se modificará el firmware del Arduino (`grua_arduino.ino`) ni el del ESP32 (`main.py`), los cuales ya están implementados correctamente. El objetivo es corregir y elevar a calidad premium la interfaz interactiva `Schema.html` para representar fielmente todo el sistema.

---

## Decisions

### 1. Ruteo Ortogonal (Manhattan) de Cables
**Decisión:** Cada uno de los 25 cables del SVG se dibujará utilizando rutas ortogonales estrictas (ejes X e Y paralelos) usando el comando `path` con giros de 90° (`L` y `H` o `V`). 
**Justificación:** Evita el cruce caótico de diagonales y proporciona un aspecto limpio e industrial, emulando programas de diseño de circuitos profesionales como KiCAD o Altium. Cada cable se conectará en el círculo de pin correspondiente.

### 2. Filtro SVG de Brillo de Neón (Glow Filter)
**Decisión:** Declarar un filtro de brillo SVG reusable en la sección `<defs>` del documento:
```xml
<filter id="glow-effect" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="blur" />
    <feComponentTransfer in="blur" result="glow">
        <feFuncA type="linear" slope="0.75"/>
    </feComponentTransfer>
    <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
    </feMerge>
</filter>
```
**Justificación:** Esto proporciona un brillo envolvente muy estético que destaca el cable activo de forma moderna y limpia sin usar librerías de terceros.

### 3. Animación Híbrida del Flujo de Señales
**Decisión:** Al hacer clic en un cable, además de la clase `.active`, se le aplicará un patrón de guiones CSS y animación de desfase (`stroke-dasharray` y `stroke-dashoffset` animado).
```css
@keyframes pulseFlow {
    from { stroke-dashoffset: 24; }
    to { stroke-dashoffset: 0; }
}
.connection-wire.active {
    stroke-width: 5.5px;
    stroke-dasharray: 8, 6;
    animation: pulseFlow 0.9s linear infinite;
    filter: url(#glow-effect);
    cursor: pointer;
}
```
**Justificación:** Solo el cable seleccionado tendrá animación activa. Esto indica claramente la dirección física de la señal (del origen al destino) y aporta dinamismo sin recargar visualmente el resto del diagrama.

### 4. Arquitectura de Datos de Cables en JS
**Decisión:** Crear un mapa estructurado de datos de cables en JavaScript con los campos `name`, `desc` (¿Qué hace?), `rationale` (¿Por qué?) y `color` para cada conexión:
```javascript
const connectionData = {
    "joy1-vrx": {
        name: "Joystick 1 VRX ──▶ Arduino A0",
        type: "ANALOG_IN",
        desc: "Línea de señal analógica que transmite la posición horizontal (eje X) del Joystick 1.",
        rationale: "Se conecta a una entrada analógica (A0) para leer la tensión variable (0-5V) generada por el potenciómetro del joystick. El firmware mapea esta lectura (0-1023) a un ciclo de trabajo PWM proporcional para controlar el sentido y la velocidad del motor del carro.",
        color: "#4faeff"
    },
    // ... así para las 25 conexiones
};
```
**Justificación:** Centraliza la información del sistema en código limpio en lugar de saturar el SVG de atributos `data-*` largos, facilitando el mantenimiento y permitiendo descripciones técnicas detalladas de alta calidad de ingeniería.

### 5. Integración Sincronizada con la Tabla Pin-a-Pin
**Decisión:** Sincronizar el SVG y la Tabla de dos maneras:
- **SVG $\rightarrow$ Tabla:** Al hacer clic en un cable, JavaScript busca la fila correspondiente en la tabla usando un identificador único (p. ej. `id="row-joy1-vrx"`), le añade una clase `.highlight-row` con fondo degradado y desplaza suavemente la tabla hasta esa fila si no está visible.
- **Tabla $\rightarrow$ SVG:** Al realizar una búsqueda en la caja de texto, JavaScript analiza qué filas coinciden y añade a los cables del SVG no coincidentes la clase `.inactive-wire` (opacidad reducida al 15% y escala de grises sutil), permitiendo aislar visualmente las conexiones filtradas directamente en el diagrama.

---

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| Consumo de rendimiento por filtros de neón en navegadores móviles | El filtro de neón se aplica **únicamente** al cable seleccionado (`.connection-wire.active`). Los 24 cables restantes usan renderizado estándar plano, lo que minimiza el impacto en la CPU/GPU. |
| Saturación visual con 25 cables ortogonales | Ruteo Manhattan ordenado en "carriles" verticales y horizontales bien espaciados. Se usa una paleta de colores curada y de baja saturación en reposo, encendiéndose solo al hacer clic o hover. |
| Incompatibilidad de ancho de pantalla en móviles | El SVG se diseña con un `viewBox` fluido de `0 0 1000 720` y estilos de contenedor responsivo, permitiendo scroll horizontal táctil suave si el dispositivo móvil es muy pequeño. |
