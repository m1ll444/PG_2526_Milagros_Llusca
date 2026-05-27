## Context

El sistema de control de grúa torre actualmente opera con:
- 2 motores DC N20 (carro y elevación) controlados por un TB6612FNG
- 1 motor paso a paso NEMA 17 (giro) controlado por un DRV8825 + biblioteca AccelStepper
- Control dual simultáneo donde el joystick siempre tiene prioridad sobre los comandos web
- Sin indicador visual del modo de control activo
- Sin documentación visual de conexiones electrónicas

### Estado actual de pines Arduino

| Pin | Uso Actual |
|-----|------------|
| D0 (RX) | UART desde ESP32 |
| D2 | AIN1 - Motor Carro |
| D3 | PWMA - Motor Carro |
| D4 | AIN2 - Motor Carro |
| D5 | PWMB - Motor Elevación |
| D7 | BIN1 - Motor Elevación |
| D8 | BIN2 - Motor Elevación |
| D9 | STEP - DRV8825 (se libera) |
| D10 | DIR - DRV8825 (se libera) |
| A0 | Joystick X (Carro) |
| A1 | Joystick Y (Elevación) |
| A2 | Joystick Z (Giro) |

## Goals / Non-Goals

**Goals:**
- Reemplazar el motor paso a paso por motoreductor DC 30RPM con segundo TB6612FNG
- Implementar conmutación explícita Web/Manual mediante switch en interfaz web y botón físico
- Crear Schema.html con diagrama de bloques y tabla pin-a-pin
- Hacer las velocidades máximas de cada motor configurables

**Non-Goals:**
- No se implementa feedback de posición ni encoders
- No se implementa comunicación bidireccional completa (solo se agrega el estado de modo)
- No se rediseña la interfaz web completa, solo se agrega el switch de modo
- No se implementan perfiles de velocidad dinámicos (solo constantes fijas)

## Decisions

### 1. Asignación de pines para el segundo TB6612FNG (Motor de Giro)

**Decisión**: Usar los pines D9 (PWM), D11 y D12 para el canal del motoreductor de giro.

**Rationale**: D9 queda libre al eliminar el DRV8825 y tiene capacidad PWM (Timer 1). D11 y D12 están libres y son digitales estándar. Se evita D10 para no conflictar con SPI si se necesita en el futuro.

| Pin | Función | Nota |
|-----|---------|------|
| D11 | CIN1 (Dirección 1) | Digital output |
| D12 | CIN2 (Dirección 2) | Digital output |
| D9  | PWMC (Velocidad) | PWM via Timer 1 |

### 2. Pin del botón físico de joystick para cambio de modo

**Decisión**: Usar pin D6 con pull-up interno (INPUT_PULLUP).

**Rationale**: D6 está libre, tiene capacidad de interrupción de cambio de pin (PCINT), y no interfiere con ningún timer o periférico. Se usa debounce por software (50ms).

### 3. Protocolo UART para sincronización de modo

**Decisión**: Comunicación bidireccional limitada usando caracteres simples.

- ESP32 → Arduino: `M` (toggle modo)
- Arduino → ESP32: `W` (modo web activo) / `J` (modo manual activo)

**Rationale**: Mantiene la simplicidad del protocolo existente (1 byte). Arduino necesita informar al ESP32 cuando el botón físico cambia el modo. Se añade lectura UART en el ESP32 (pin RX=16, ya configurado pero no utilizado).

**Alternativa descartada**: Protocolo con prefijo tipo `MODE:WEB` — más explícito pero rompe la compatibilidad con el parser de 1 byte existente.

### 4. Lógica de modo mutuamente excluyente

**Decisión**: Los modos Web y Manual son mutuamente excluyentes. El modo por defecto es Manual.

**Rationale**: Elimina la complejidad de la superposición de señales anterior (donde ambas fuentes podían actuar simultáneamente). Es más seguro para el operador porque sabe exactamente qué fuente controla los motores.

```
┌─────────────────────────────────────────────────┐
│               Estado de Modo                    │
│                                                 │
│  ┌──────────┐   Botón D6    ┌──────────┐       │
│  │  MANUAL  │──────────────▶│   WEB    │       │
│  │          │◀──────────────│          │       │
│  └──────────┘   Cmd 'M'    └──────────┘       │
│       │         ó Botón D6       │              │
│       ▼                          ▼              │
│  Joysticks      ◀─ Fuente ─▶    UART           │
│  activos                     Comandos activos   │
│                              Timeout activo     │
└─────────────────────────────────────────────────┘
```

### 5. Velocidades máximas configurables

**Decisión**: Definir 3 constantes al inicio del `.ino`:

```cpp
const int MAX_SPEED_CARRO = 255;
const int MAX_SPEED_ELEVACION = 255;
const int MAX_SPEED_GIRO = 200; // Motoreductor 30RPM, menor velocidad PWM
```

**Rationale**: Permite ajuste rápido sin modificar la lógica. Los comandos web usan directamente estas constantes. Los joysticks mapean proporcionalmente `[0, MAX_SPEED_X]`.

### 6. Estructura del Schema.html

**Decisión**: Archivo HTML autocontenido (sin dependencias externas) con:
- Diagrama de bloques SVG inline, coloreado por subsistema
- Tabla HTML responsiva con todas las conexiones pin-a-pin
- Estilo visual coherente con la interfaz web existente (tema oscuro)

**Rationale**: Al ser autocontenido se puede abrir offline sin servidor. SVG inline permite escalabilidad y colores sin dependencias externas.

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| Comunicación bidireccional UART puede generar colisiones si Arduino y ESP32 envían simultáneamente | Arduino solo envía estado de modo (1 byte) tras un cambio, no de forma continua. La colisión es muy improbable. |
| Botón de joystick puede rebotar y causar toggles múltiples | Implementar debounce de 50ms por software en el Arduino |
| El motoreductor de 30RPM puede necesitar un valor PWM mínimo para arrancar (dead zone del motor) | Documentar como ajuste de `MAX_SPEED_GIRO`. Se puede agregar una constante `MIN_SPEED_GIRO` si es necesario. |
| El switch web puede quedar desincronizado si se pierde un byte UART | La interfaz web consultará `/mode` al cargar para sincronizar el estado inicial |
| D9 comparte Timer 1 con D10 — si en el futuro se usa D10 para otra función PWM, compartirán frecuencia | Aceptable. D10 queda libre y sin uso planificado. |
