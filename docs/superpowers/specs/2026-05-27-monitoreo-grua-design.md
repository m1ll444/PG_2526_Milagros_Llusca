# Diseño de Monitoreo de Grúa Torre con Animación 2.5D y Telemetría

Este documento detalla el diseño técnico para añadir un panel de monitoreo de grúa interactivo en 2.5D a la derecha de los controles en la interfaz web, reflejando el movimiento de la grúa en tiempo real tanto en modo de control web como manual (joystick físico).

---

## 1. Arquitectura y Flujo de Datos

El sistema consta de tres componentes principales: el firmware del Arduino, el firmware del ESP32 y la interfaz web ejecutada en el navegador.

```
+------------------+         UART Serial         +---------------+
|   Arduino Uno    | --------------------------> |     ESP32     |
| (Control Motores|  "S:W,F,S,R\n" (100ms)      | (Servidor Web)|
|  y Joysticks)    |                             +---------------+
+------------------+                                     |
                                                         | HTTP GET /status (150ms)
                                                         v
                                                 +---------------+
                                                 | Interfaz Web  |
                                                 | (index.html)  |
                                                 +---------------+
```

### Flujo de datos paso a paso:
1. El **Arduino** lee las entradas analógicas de los joysticks (modo manual) o almacena el comando web activo (modo web).
2. Cada 100 ms, el Arduino transmite el estado combinado de movimiento al ESP32 vía UART utilizando la cadena: `S:<modo>,<carro>,<elev>,<giro>\n`.
3. El **ESP32** recibe esta cadena de forma asíncrona, la procesa para extraer la telemetría actual y el modo de control, y actualiza sus variables globales en memoria.
4. El **Navegador Web** realiza consultas rápidas (polling) al endpoint `/status` del ESP32 cada 150 ms para obtener el estado más reciente.
5. El código **JavaScript** de la interfaz web utiliza este estado de movimiento activo para simular e interpolar de forma suave el ángulo de rotación, la posición del carro y la altura del gancho, actualizando un gráfico SVG 2.5D a 60 FPS mediante `requestAnimationFrame`.

---

## 2. Modificaciones de Software por Archivo

### A. Arduino Firmware: `grua_arduino/grua_arduino.ino`
- **Telemetría Frecuente**: Añadir una lógica de temporizador sin bloqueo basada en `millis()` para transmitir el estado de la grúa cada 100 ms.
- **Detección de Movimientos**: Crear variables de estado de dirección para cada eje:
  - **Carro**: `F` (Avanzar), `B` (Retroceder), `S` (Parar).
  - **Elevación**: `U` (Subir), `D` (Bajar), `S` (Parar).
  - **Giro**: `R` (Derecha/Horario), `L` (Izquierda/Antihorario), `S` (Parar).
- **Formateador Serial**: Ensamblar el string `S:<modo>,<carro>,<elev>,<giro>\n` y enviarlo a través de `Serial.write()`.

### B. ESP32 Firmware: `esp32/main.py`
- **Recepción UART por Línea**: Modificar `leer_uart_modo()` para acumular datos del buffer UART hasta detectar un carácter de nueva línea (`\n`).
- **Procesamiento de Telemetría**: Si la línea comienza con `S:`, dividirla por comas para actualizar:
  - `current_mode` (a partir de la primera letra `W` o `J`).
  - `current_telemetry` (guardando la cadena formateada como `modo,carro,elev,giro`).
- **Endpoint `/status`**: Añadir un controlador de ruta para la petición `GET /status`. Responderá con la telemetría actual en texto plano y con cabeceras CORS (`Access-Control-Allow-Origin: *`).

### C. Mock Server: `test_server.py`
- **Simulación de Estados**: Añadir variables internas de estado para `carro_dir`, `elev_dir`, y `giro_dir` en el mock.
- **Soporte `/status`**: Cuando el cliente pida `/status`, responder con `WEB,<carro>,<elev>,<giro>` según el comando activo actual enviado por los controles (por ejemplo, si se presionó "F", responder con `WEB,F,S,S`). Si el modo simulado es manual, responder con `MANUAL,S,S,S`.

### D. Interfaz Web: `esp32/index.html`
- **Estructura Grid Responsiva**:
  - Encapsular todo el cuerpo en un contenedor principal `.dashboard-container`.
  - Crear dos columnas principales: `.controls-column` (izquierda) y `.monitoring-column` (derecha).
  - Usar Media Queries para apilar verticalmente en pantallas de ancho inferior a 768px.
- **Diseño del Panel de Monitoreo**:
  - Contenedor con estética dark glassmorphic similar al actual panel de control.
  - Título: "Monitoreo de Operación".
  - Gráfico SVG para la Grúa en Perspectiva 2.5D.
  - Indicadores numéricos de telemetría:
    - Giro: `Angle°`
    - Carro: `Distance%`
    - Gancho: `Height%`
- **Implementación del SVG 2.5D**:
  - **Estructura Fija**:
    - Líneas del mástil vertical y la base de apoyo con un diseño de rejilla brillante (color gris/azul con un brillo sutil).
  - **Estructura Rotativa (Jib/Pluma)**:
    - Calculada trigonométricamente desde el centro del mástil superior:
      - `x_extremo = x_centro + cos(angulo) * largo`
      - `y_extremo = y_centro + sin(angulo) * largo * 0.5`
    - Color azul neón brillante (`#3b82f6`) con filtro SVG `drop-shadow`.
    - Pluma y Contrapluma alineadas en el mismo eje de rotación.
  - **Carro**:
    - Un rectángulo o círculo pequeño que se mueve a lo largo del segmento calculado de la pluma.
  - **Cable y Gancho**:
    - Cable: Línea vertical desde el carro hacia abajo.
    - Gancho: Pequeño gancho dibujado con un trazo grueso en el extremo inferior del cable.
- **Lógica de Simulación de Física en JavaScript**:
  - Bucle `requestAnimationFrame` que simula el cambio de posición en base al estado activo:
    - Si el carro se mueve adelante (`F`), aumentar distancia; si retrocede (`B`), disminuirla.
    - Si la elevación sube (`U`), reducir la longitud del cable (subir gancho); si baja (`D`), aumentarla.
    - Si el giro es derecha (`R`), sumar ángulo; si es izquierda (`L`), restar ángulo.
  - Limitar físicamente las variables (ej: carro entre 10% y 95% del largo de la pluma; gancho sin sobrepasar el suelo o la altura de la pluma).
  - Reemplazar el polling de `/mode` por consultas a `/status` cada 150 ms para refrescar el modo de control y la dirección actual de los motores.

---

## 3. Plan de Verificación

### Pruebas Automatizadas y de Simulación
1. Ejecutar `python test_server.py` localmente.
2. Abrir la página en un navegador y verificar que la estructura responsiva cambie al reducir el tamaño de la ventana.
3. Presionar botones de dirección (adelante, atrás, subir, bajar, girar) y comprobar que el modelo 2.5D de la grúa se anime suavemente en la dirección correspondiente en tiempo real.
4. Alternar al modo MANUAL y simular telemetría manual para verificar que el gráfico responda correctamente.

### Pruebas de Hardware (Manual)
1. Cargar el firmware modificado en el Arduino.
2. Cargar el script de MicroPython en el ESP32.
3. Conectar el ESP32 a la red local y acceder a la interfaz.
4. Mover la grúa con el joystick analógico físico y verificar en la pantalla que el gráfico dinámico gire, desplace el carro y suba/baje el gancho en concordancia con el movimiento físico real.
