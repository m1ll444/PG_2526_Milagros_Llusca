# Especificación de Diseño: Esquema de Conexiones Electrónicas Premium e Interactivo

- **Autor:** Antigravity (IA Pair Programmer)
- **Fecha:** 2026-05-27
- **Tema:** Renovación Estética y Funcional de `Schema.html`
- **Estado:** Propuesto e Híbrido Aprobado por el Usuario

---

## 1. Introducción y Contexto

El archivo `Schema.html` actúa como el centro de documentación y control visual del conexionado electrónico de la grúa torre. El sistema emplea dos microcontroladores en comunicación UART (ESP32 y Arduino Nano) y tres motores DC controlados mediante dos módulos de puente H TB6612FNG, operando bajo un modo de control dual (Web / Manual) que es mutuamente excluyente.

Tras la exploración detallada de los archivos de firmware del Arduino (`grua_arduino.ino`) y del ESP32 (`main.py`), se identificaron:
1. **Desalineaciones críticas** en el cableado SVG actual (pines de Joystick cruzados).
2. **Ausencia de cableado de energía lógica y de control STBY** en el diagrama, indispensables para el funcionamiento real.
3. **Limitación de interactividad** que impide lecturas pausadas y detalladas al no contar con un bloqueo de selección por clic.

Este diseño define la arquitectura visual, técnica y de código para renovar integralmente `Schema.html` con un enfoque híbrido: una estética ortogonal de nivel industrial con una consola glassmorphic, y efectos de brillo de neón y flujo animado en movimiento exclusivamente en el cable que se encuentre seleccionado.

---

## 2. Objetivos y Alcance

### Objetivos:
- Corregir las discrepancias físicas en las señales del joystick.
- Incluir las 6 líneas de energía y tierras de control faltantes en el SVG y la tabla pin-a-pin (totalizando 25 conexiones reales).
- Ruteado ortogonal de cables con terminaciones de pin exactas para simular un diseño de ingeniería profesional.
- Implementar la funcionalidad interactiva "Click & Lock" (clic y bloqueo) con transiciones suaves en CSS.
- Integrar animaciones fluidas con patrón de guiones CSS móviles (`stroke-dashoffset`) en el cable seleccionado.
- Rediseñar el panel de detalles con una estética glassmorphic premium que cambie de color dinámicamente según el cable activo.
- Sincronizar bidireccionalmente el SVG con la tabla pin-a-pin para fines de depuración.

### Fuera de Alcance:
- No se modificará el código C++ de Arduino ni el código Python del ESP32, ya que operan de forma correcta y su asignación de pines es correcta.
- No se alterarán los colores definidos previamente para los cables, manteniéndolos alineados a la leyenda oficial.

---

## 3. Especificaciones del Trazado del Circuito (SVG)

El lienzo SVG se estructurará con un `viewBox="0 0 1000 720"` y contendrá:

### A. Gráficos de Placas Reales:
1. **ESP32 DevKit V1:** Un bloque gris oscuro con sus dos filas de pines metálicos dorados, serigrafía de pines detallada (TX2, RX2, VIN, GND), chip de silicio central y el LED azul de estado en GPIO 2.
2. **Arduino Nano:** Placa azul marino detallada, con microcontrolador central ATmega328P, pines hembra etiquetados de D0 a D12 en un lateral y analógicos (A0-A2), VIN, 5V y GND en el otro.
3. **Drivers TB6612FNG #1 y #2:** Placas de color rojo vivo con etiquetas de pines exactas de entrada (`VM`, `VCC`, `GND`, `AIN1`/`BIN1`, `PWMA`/`PWMB`, `STBY`) y de salida (`AO1`/`AO2` para motores).
4. **Joysticks 1 y 2:** Módulos de color negro con la palanca analógica ilustrada tridimensionalmente y pines de conexión a la derecha.
5. **Fuente de Alimentación 12V:** Módulo metálico de rejilla industrial con terminales de tornillo (+12V, GND) en color dorado/latón.
6. **Motores DC:** Cuerpos cilíndricos metálicos con reductoras de latón representadas gráficamente y dos cables saliendo de sus bornes.

### B. Mapeo Físico de Pines y Trazado Ortogonal (Manhattan):
El diagrama contendrá exactamente 25 líneas con ruteo de 90° que conectan pin-a-pin:

| Conexión ID | Origen | Pin | Destino | Pin | Categoría | Color CSS |
|-------------|--------|-----|---------|-----|-----------|-----------|
| `uart-tx` | ESP32 | GPIO 17 (TX2) | Arduino | D0 (RX) | UART | `#f3c61c` |
| `uart-rx` | Arduino | D1 (TX) | ESP32 | GPIO 16 (RX2) | UART | `#f3c61c` |
| `uart-gnd` | ESP32 | GND | Arduino | GND | Tierra | `#7388ad` |
| `pwr-12v-1` | Fuente | +12V | TB6612 #1 | VM | Potencia | `#f9d44f` (dash) |
| `pwr-12v-2` | Fuente | +12V | TB6612 #2 | VM | Potencia | `#f9d44f` (dash) |
| `pwr-12v-ard`| Fuente | +12V | Arduino | VIN | Potencia | `#f5cc2d` |
| `pwr-gnd-1` | Fuente | GND | TB6612 #1 | GND | Tierra | `#7388ad` |
| `pwr-gnd-2` | Fuente | GND | TB6612 #2 | GND | Tierra | `#7388ad` |
| `pwr-gnd-ard`| Fuente | GND | Arduino | GND | Tierra | `#7388ad` |
| `pwr-5v-esp` | Arduino | 5V | ESP32 | VIN | Lógica 5V | `#f5cc2d` |
| `pwr-5v-drv1`| Arduino | 5V | TB6612 #1 | VCC | Lógica 5V | `#f5cc2d` |
| `pwr-5v-drv2`| Arduino | 5V | TB6612 #2 | VCC | Lógica 5V | `#f5cc2d` |
| `drv1-stby`  | Arduino | 5V | TB6612 #1 | STBY | Habilitación| `#f5cc2d` |
| `drv2-stby`  | Arduino | 5V | TB6612 #2 | STBY | Habilitación| `#f5cc2d` |
| `joy-5v`     | Arduino | 5V | Joysticks (1 y 2)| 5V | Lógica 5V | `#f5cc2d` |
| `joy1-vrx`   | Joystick 1| VRX | Arduino | A0 | Analógico | `#4faeff` |
| `joy1-vry`   | Joystick 1| VRY | Arduino | A2 | Analógico | `#6976ff` |
| `joy2-vrx`   | Joystick 2| VRX | Arduino | A1 | Analógico | `#32c8ff` |
| `joy2-sw`    | Joystick 2| SW | Arduino | D6 | Digital | `#fff28f` |
| `ctrl-carro-1`| Arduino | D2 (AIN1) | TB6612 #1 | AIN1 | Control | `#4faeff` |
| `ctrl-carro-2`| Arduino | D4 (AIN2) | TB6612 #1 | AIN2 | Control | `#4faeff` |
| `pwm-carro`  | Arduino | D3 (PWMA) | TB6612 #1 | PWMA | PWM | `#4faeff` |
| `ctrl-elev-1` | Arduino | D7 (BIN1) | TB6612 #1 | BIN1 | Control | `#32c8ff` |
| `ctrl-elev-2` | Arduino | D8 (BIN2) | TB6612 #1 | BIN2 | Control | `#32c8ff` |
| `pwm-elev`   | Arduino | D5 (PWMB) | TB6612 #1 | PWMB | PWM | `#32c8ff` |
| `ctrl-giro-1` | Arduino | D11 (CIN1)| TB6612 #2 | CIN1 | Control | `#6976ff` |
| `ctrl-giro-2` | Arduino | D12 (CIN2)| TB6612 #2 | CIN2 | Control | `#6976ff` |
| `pwm-giro`   | Arduino | D9 (PWMC) | TB6612 #2 | PWMC | PWM | `#6976ff` |
| `mot-carro-p`| TB6612 #1| AO1 | Motor Carro | + | Motor | `#4faeff` |
| `mot-carro-n`| TB6612 #1| AO2 | Motor Carro | - | Motor | `#4faeff` |
| `mot-elev-p` | TB6612 #1| BO1 | Motor Elev. | + | Motor | `#32c8ff` |
| `mot-elev-n` | TB6612 #1| BO2 | Motor Elev. | - | Motor | `#32c8ff` |
| `mot-giro-p` | TB6612 #2| CO1 | Motor Giro | + | Motor | `#6976ff` |
| `mot-giro-n` | TB6612 #2| CO2 | Motor Giro | - | Motor | `#6976ff` |

---

## 4. Diseño de la Interfaz y Estilos CSS

### A. Paleta de Colores Curada (HSL Dinámico):
- **Modo Oscuro Profundo (Default):**
  - Fondo (`--bg`): `#070f1e`
  - Paneles (`--panel-bg`): `rgba(13, 24, 46, 0.85)`
  - Bordes (`--border-color`): `rgba(79, 174, 255, 0.15)`
  - Texto (`--text`): `#e2edf8`
- **Modo Claro Elegante:**
  - Fondo (`--bg`): `#f0f4f9`
  - Paneles (`--panel-bg`): `rgba(255, 255, 255, 0.9)`
  - Bordes (`--border-color`): `rgba(75, 104, 148, 0.18)`
  - Texto (`--text`): `#1b293d`

### B. Consola Glassmorphic `.info-panel`:
- Desenfoque de fondo mediante `backdrop-filter: blur(16px) saturate(140%)`.
- Borde superior iluminado dinámicamente con una transición de CSS (`border-top: 3px solid var(--active-wire-color, var(--border-color))`).
- Caja de texto estructurada con etiquetas técnicas de colores (badges) y explicaciones formateadas para una legibilidad superior.

---

## 5. Lógica de Interacción JavaScript

El archivo incluirá un script optimizado de JavaScript que gestionará las siguientes funcionalidades clave:

```javascript
// Base de datos de conexiones enriquecida
const connectionDatabase = {
    "uart-tx": {
        title: "ESP32 GPIO 17 (TX2) ──▶ Arduino RX (D0)",
        tag: "UART",
        tagClass: "tag-uart",
        desc: "Línea serie de transmisión que envía comandos de control desde el ESP32 hacia el Arduino Nano.",
        rationale: "Se realiza para canalizar todas las directivas de movimiento del operador web (como Adelante, Subir o Parada) y la conmutación de modo. Se conecta a D0 (RX del Arduino) para que el parser del búfer de lectura por hardware procese inmediatamente el byte entrante."
    },
    // ... datos técnicos para los 25 cables
};

// Control de eventos interactivos
let lockedWire = null;

function initInteraction() {
    const wires = document.querySelectorAll('.connection-wire');
    const panel = document.getElementById('wireInfoPanel');
    const titleEl = document.getElementById('wireName');
    const descEl = document.getElementById('wireDesc');
    
    wires.forEach(wire => {
        const id = wire.getAttribute('id');
        
        // Hover
        wire.addEventListener('mouseenter', () => {
            if (lockedWire) return;
            showWireInfo(id);
            highlightWire(wire);
        });
        
        wire.addEventListener('mouseleave', () => {
            if (lockedWire) return;
            resetWireInfo();
            unhighlightWire(wire);
        });
        
        // Click (Lock)
        wire.addEventListener('click', (e) => {
            e.stopPropagation();
            if (lockedWire === id) {
                unlockSelection();
            } else {
                lockSelection(id, wire);
            }
        });
    });
    
    // Clic en el fondo para limpiar
    document.querySelector('svg').addEventListener('click', () => {
        unlockSelection();
    });
}
```

---

## 6. Plan de Verificación

### Pruebas de Comportamiento:
1. **Verificación de Enlaces de Cables:** Confirmar que al hacer clic en el cable de Giro (`joy1-vry`) se muestra correctamente la entrada analógica A2 en el Arduino, y en Elevación (`joy2-vrx`) la entrada A1.
2. **Prueba de Bloqueo ("Click & Lock"):** Hacer clic en un cable y retirar el puntero; verificar que la tarjeta retiene la información técnica y que el cable mantiene su animación de pulso y neón activo. Al presionar "Liberar Selección ✕", el estado debe volver a la normalidad de inmediato.
3. **Prueba de Sincronización Bidireccional:**
   - Hacer clic en un cable del SVG; verificar que la fila correspondiente en la tabla pin-a-pin se resalta con un fondo dinámico brillante.
   - Escribir en el buscador `D6` o `STBY`; verificar que las filas de la tabla se filtran correctamente y que los cables inactivos en el SVG se atenúan al 15% de opacidad, facilitando su identificación en el diagrama de bloques.
