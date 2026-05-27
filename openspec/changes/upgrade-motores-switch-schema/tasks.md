## 1. Firmware Arduino — Motor de Giro DC

- [x] 1.1 Eliminar `#include <AccelStepper.h>` y toda la lógica del motor paso a paso (instancia `stepper`, `controlarGiro()` con `setSpeed`/`runSpeed`)
- [x] 1.2 Definir pines para el segundo TB6612FNG: `CIN1_PIN` (D11), `CIN2_PIN` (D12), `PWMC_PIN` (D9)
- [x] 1.3 Configurar los nuevos pines como OUTPUT en `setup()`
- [x] 1.4 Implementar funciones `moverGiro(bool horario, int velocidad)` y `detenerGiro()` con la misma lógica que los otros motores DC
- [x] 1.5 Actualizar `controlarGiro()` para usar `moverGiro()` y `detenerGiro()` en lugar de AccelStepper

## 2. Firmware Arduino — Velocidades Máximas Configurables

- [x] 2.1 Definir constantes `MAX_SPEED_CARRO`, `MAX_SPEED_ELEVACION`, `MAX_SPEED_GIRO` al inicio del archivo (valores por defecto: 255, 255, 200)
- [x] 2.2 Actualizar `controlarCarro()` para mapear joystick a `[0, MAX_SPEED_CARRO]` en lugar de `[0, 255]`
- [x] 2.3 Actualizar `controlarElevacion()` para mapear joystick a `[0, MAX_SPEED_ELEVACION]`
- [x] 2.4 Actualizar `controlarGiro()` para mapear joystick a `[0, MAX_SPEED_GIRO]`
- [x] 2.5 Actualizar comandos web para usar `MAX_SPEED_*` en lugar del valor fijo 255

## 3. Firmware Arduino — Modo de Control Dual

- [x] 3.1 Definir pin `BUTTON_MODE_PIN` (D6) y configurar como `INPUT_PULLUP` en `setup()`
- [x] 3.2 Implementar variable global `bool modoWeb = false` (modo por defecto: Manual)
- [x] 3.3 Implementar lectura del botón con debounce de 50ms en `loop()` para conmutar `modoWeb`
- [x] 3.4 Al cambiar modo por botón físico, enviar `W` o `J` por Serial al ESP32
- [x] 3.5 Agregar comando `M` en `leerComandoWeb()` para conmutar modo desde la web y enviar `W` o `J` de confirmación
- [x] 3.6 Modificar `controlarCarro()`, `controlarElevacion()` y `controlarGiro()` para ejecutar solo la fuente activa según `modoWeb`
- [x] 3.7 Desactivar timeout de seguridad web cuando `modoWeb == false`

## 4. Firmware ESP32 — Soporte de Modo Bidireccional

- [x] 4.1 Agregar variable global `current_mode = 'MANUAL'` en `main.py`
- [x] 4.2 Implementar lectura UART asíncrona (pin RX=16 ya configurado) para recibir `W` y `J` del Arduino y actualizar `current_mode`
- [x] 4.3 Agregar endpoint `/mode` en el servidor web que devuelva `current_mode` como texto plano
- [x] 4.4 Verificar que el comando `M` se envía por UART al recibir `/cmd?action=M`

## 5. Interfaz Web — Switch de Modo

- [x] 5.1 Agregar componente switch toggle estilizado (estilo glassmorphism coherente) en la parte superior del panel de control en `index.html`
- [x] 5.2 Implementar lógica JavaScript para enviar `/cmd?action=M` al hacer toggle y actualizar estado visual
- [x] 5.3 Implementar polling periódico a `/mode` (cada 2 segundos) para sincronizar el switch con el estado real del Arduino
- [x] 5.4 Deshabilitar visualmente los botones de movimiento cuando el modo es Manual (opacidad reducida, sin eventos de clic)
- [x] 5.5 Agregar indicador textual del modo activo junto al switch

## 6. Schema.html — Diagrama de Conexiones Electrónicas

- [x] 6.1 Crear archivo `Schema.html` en la raíz del proyecto
- [x] 6.2 Implementar diagrama de bloques SVG inline organizado por subsistemas: ESP32, Arduino, TB6612FNG #1, TB6612FNG #2, motores, joysticks, alimentación
- [x] 6.3 Colorear líneas de conexión por tipo de señal (digital, PWM, analógica, UART, alimentación)
- [x] 6.4 Implementar tabla HTML responsiva con todas las conexiones pin-a-pin (origen, destino, tipo, observaciones)
- [x] 6.5 Aplicar estilo visual oscuro coherente con la interfaz web del ESP32

## 7. Documentación y Especificaciones

- [x] 7.1 Actualizar `openspec/specs/control-motores/spec.md` con los cambios del motor de giro y velocidades configurables
- [x] 7.2 Actualizar `openspec/specs/comunicacion-uart/spec.md` con los nuevos comandos M, W, J
- [x] 7.3 Actualizar `openspec/specs/servidor-web/spec.md` con el switch de modo y endpoint `/mode`
- [x] 7.4 Actualizar `openspec/specs/control-prioridad-seguridad/spec.md` con la lógica de modo exclusivo
- [x] 7.5 Crear `openspec/specs/modo-control-dual/spec.md` con la nueva capacidad
- [x] 7.6 Crear `openspec/specs/schema-conexiones/spec.md` con la nueva capacidad
- [x] 7.7 Actualizar `README.md` con los cambios de hardware y nueva documentación
- [x] 7.8 Actualizar `requirements.md` con los cambios de requerimientos

## 8. Verificación

- [x] 8.1 Validar que `openspec validate --specs` pase para todas las especificaciones actualizadas
- [x] 8.2 Verificar compilación del firmware Arduino (sin errores de sintaxis)
- [x] 8.3 Verificar que `Schema.html` se renderiza correctamente en un navegador
- [x] 8.4 Verificar que `index.html` muestra el switch y los controles se deshabilitan en modo manual
