## Why

El sistema de grúa torre necesita tres cambios fundamentales para mejorar su operabilidad y documentación:

1. **Motor de giro:** El motor paso a paso NEMA 17 con driver DRV8825 se reemplaza por un motoreductor DC de 30RPM controlado por un segundo módulo TB6612FNG. Esto simplifica el hardware (elimina la dependencia de AccelStepper), reduce costo y unifica el tipo de control para los tres ejes a PWM + dirección.
2. **Modo de control dual (Web/Manual):** Actualmente ambos modos coexisten simultáneamente con prioridad del joystick. Se necesita un mecanismo explícito de conmutación (switch en la interfaz web + botón físico del joystick) que permita activar exclusivamente un modo u otro, evitando interferencias no deseadas.
3. **Diagrama de conexiones:** No existe un recurso visual que documente las conexiones electrónicas del proyecto. Se necesita un archivo `Schema.html` interactivo con diagrama de bloques y tabla pin-a-pin.

## What Changes

- **Eliminar** soporte para motor paso a paso NEMA 17 y driver DRV8825 del firmware Arduino
- **Agregar** control de motoreductor DC 30RPM para giro, usando un segundo módulo TB6612FNG (un solo canal)
- **Agregar** constantes de velocidad máxima configurables por motor en el firmware Arduino (`MAX_SPEED_CARRO`, `MAX_SPEED_ELEVACION`, `MAX_SPEED_GIRO`)
- **Agregar** switch de modo de control (Web / Manual) en la interfaz web del ESP32
- **Agregar** lectura de botón físico de joystick (pin D6) en Arduino para conmutar modo de control
- **Agregar** sincronización del estado de modo entre ESP32 y Arduino vía UART
- **Crear** archivo `Schema.html` con diagrama de bloques visual por subsistema y tabla detallada pin-a-pin
- **BREAKING**: Los comandos UART se amplían para incluir comandos de cambio de modo

## Capabilities

### New Capabilities
- `modo-control-dual`: Conmutación explícita entre control Web y control Manual mediante switch en la interfaz web y botón físico del joystick. Incluye sincronización del estado entre ESP32 y Arduino.
- `schema-conexiones`: Archivo HTML interactivo con diagrama de bloques visual de las conexiones electrónicas y tabla pin-a-pin detallada.

### Modified Capabilities
- `control-motores`: Se elimina el motor paso a paso NEMA 17 + DRV8825 y se reemplaza por un motoreductor DC 30RPM con segundo TB6612FNG. Se agregan constantes de velocidad máxima configurables por cada motor.
- `comunicacion-uart`: Se amplía el protocolo de comandos para incluir el cambio de modo de control (Web/Manual).
- `servidor-web`: Se añade el switch de modo de control en la interfaz web y un nuevo endpoint para gestionar el estado del modo.
- `control-prioridad-seguridad`: La lógica de prioridad cambia de "joystick siempre tiene prioridad" a "solo se ejecuta la fuente activa según el modo seleccionado".

## Impact

- **Firmware Arduino** (`grua_arduino/grua_arduino.ino`): Cambios significativos — eliminación de AccelStepper, nuevo driver de giro DC, nueva lógica de modo, lectura de botón físico, constantes de velocidad configurables.
- **Firmware ESP32** (`esp32/main.py`): Nuevo endpoint para modo de control, transmisión de comandos de modo por UART.
- **Interfaz Web** (`esp32/index.html`): Nuevo componente switch de modo Web/Manual con indicador visual.
- **Nuevo archivo** (`Schema.html`): Diagrama de conexiones electrónicas completo.
- **Dependencias eliminadas**: Biblioteca `AccelStepper` ya no es necesaria.
- **Hardware**: Pines D9 y D10 quedan libres (se liberan del DRV8825). Se ocupan nuevos pines para el segundo TB6612FNG y el botón del joystick.
- **Especificaciones OpenSpec**: Se actualizan 4 specs existentes y se crean 2 specs nuevas.
