# Sistema de Control de Grúa Torre - PG_2526

## 📋 Descripción del Proyecto

Sistema integral de control remoto para una grúa torre con componentes IoT. Permite el control en tiempo real de movimientos (carro, elevación y giro) mediante una interfaz web responsiva.

**Componentes principales:**
- **ESP32**: Servidor web y gateway de comunicación
- **Arduino Uno**: Controlador de motores y procesamiento de sensores
- **Interfaz Web**: Aplicación web moderna y responsiva para control remoto

---

## 🎯 Características Principales

### Control de Movimientos
- **Carro**: Movimiento horizontal adelante/atrás (Motor DC N20 con reductora 12V)
- **Elevación**: Movimiento vertical subir/bajar (Motor DC N20 con reductora 12V)
- **Giro**: Rotación horaria/antihoraria (Motoreductor DC 30RPM 12V)

### Interfaz de Usuario e Interacción
- Panel de control moderno con gradientes y efectos glassmorphism.
- Switch toggle para control dual (Web / Manual) que inhabilita los controles web en modo manual.
- Indicador visual del modo de control activo y sincronización en tiempo real vía polling (2s).
- Botones táctiles grandes y responsivos para control remoto.
- Botón de parada de emergencia prominente.

### Comunicación
- Protocolo HTTP/REST expuesto por el ESP32.
- Comunicación serie UART bidireccional entre ESP32 (GPIO 17/16) y Arduino (D0/D1).
- Transmisión serie de comandos simples de movimiento y estado de modo (`F`, `B`, `U`, `D`, `L`, `R`, `S`, `M`, `W`, `J`).

---

## 🔧 Requisitos Técnicos

### Hardware
- **ESP32 DevKit V1** (módulo WiFi y servidor asíncrono)
- **Arduino Uno/Nano** (controlador principal de motores y entradas)
- **2x Motor DC N20** (12V) para carro y elevación
- **1x Motoreductor DC de 30RPM** (12V) para giro
- **2x Driver TB6612FNG** (el primero para Carro y Elevación, el segundo para canal de Giro)
- **3x Joysticks analógicos** (o joystick multieje) con botón pulsador integrado
- **Fuente de alimentación 12V** (con regulador a 5V para lógica)

### Software
- MicroPython (ESP32)
- Arduino IDE / C++ (Arduino Uno/Nano)
- Python 3.x (para servidor de pruebas opcional)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

---

## 📦 Estructura del Proyecto

```
PG_2526_Milagros_Llusca/
├── esp32/                 # Código del ESP32
│   ├── boot.py           # Configuración inicial
│   ├── main.py           # Servidor HTTP y WebSocket
│   └── index.html        # Interfaz web
├── grua_arduino/          # Código del Arduino
│   └── grua_arduino.ino  # Control de motores
├── openspec/              # Especificaciones basadas en comportamiento
│   ├── config.yaml       # Configuración de OpenSpec
│   └── specs/            # Especificaciones de capacidades
├── test_server.py         # Servidor de pruebas (simulación)
└── README.md             # Este archivo
```

---

## 📖 Especificaciones del Sistema (OpenSpec) y Esquemas

Este proyecto adopta **OpenSpec** para documentar formalmente los requerimientos y comportamientos esperados del sistema mediante especificaciones ejecutables basadas en escenarios:

*   [Comunicación UART](openspec/specs/comunicacion-uart/spec.md): Protocolo serie y comandos de control bidireccionales entre ESP32 y Arduino.
*   [Servidor Web](openspec/specs/servidor-web/spec.md): Interfaz web en MicroPython, polling y endpoints HTTP.
*   [Control de Motores](openspec/specs/control-motores/spec.md): Control de hardware para los 3 motores DC y límites de velocidad.
*   [Lógica de Prioridad y Seguridad](openspec/specs/control-prioridad-seguridad/spec.md): Exclusividad de los modos y temporización de seguridad.
*   [Modo de Control Dual](openspec/specs/modo-control-dual/spec.md): Conmutación e intercambio de señales de sincronización.
*   [Esquema de Conexiones](openspec/specs/schema-conexiones/spec.md): Especificación del esquema de hardware interactivo.

Adicionalmente, puedes consultar el documento autocontenido de conexiones de hardware:
*   [Esquema Electrónico Interactivo (Schema.html)](Schema.html): Contiene el diagrama de bloques SVG y la tabla pin-a-pin interactiva.

---

## 🚀 Guía de Usuario

### Instalación Inicial

#### 1. Configurar ESP32
```bash
# Instalar MicroPython en ESP32
# Usar esptool.py o Thonny IDE
# Cargar boot.py y main.py en el ESP32
```

#### 2. Configurar Arduino
```bash
# Abrir Arduino IDE
# Cargar el código desde grua_arduino/grua_arduino.ino
# Verificar conexión de pines según el esquema
```

#### 3. Conexiones de Hardware
Para ver todas las conexiones de pines y la topología física detallada, consulta el archivo [Schema.html](Schema.html) o el especificado de conexiones.
Resumen de conexiones clave (Arduino):
- **Motor Carro (TB6612FNG #1)**: AIN1 (D2), AIN2 (D4), PWMA (D3)
- **Motor Elevación (TB6612FNG #1)**: BIN1 (D7), BIN2 (D8), PWMB (D5)
- **Motor Giro (TB6612FNG #2)**: CIN1 (D11), CIN2 (D12), PWMC (D9)
- **Joysticks**: X (Carro) -> A0, Y (Elevación) -> A1, Z (Giro) -> A2
- **Botón de Modo (Pulsador)**: D6

### Usar la Interfaz Web

1. **Conectarse a la Red WiFi:**
   - El ESP32 crea una red WiFi o se conecta a una de ellas.
   - Abrir el navegador y acceder a `http://<IP_ESP32>` (puerto 80).

2. **Controlar la Grúa:**
   - Activar el switch **WEB** en la parte superior para habilitar el control remoto. En modo **MANUAL**, los controles web estarán deshabilitados.
   - Mantener pulsado el botón de la dirección deseada para mover la grúa, y soltarlo para detenerla.
   - Presionar **PARADA / STOP** para una detención total inmediata.

3. **Indicadores:**
   - El punto verde indica "Sistema Online".
   - El indicador muestra en tiempo real el modo activo (`WEB` o `MANUAL`) y se actualiza mediante consulta (polling cada 2s) y confirmaciones UART asíncronas.

### Modo de Prueba

Para pruebas sin hardware:
```bash
python test_server.py
# Se abrirá localhost:8080 con servidor simulado
```

---

## ⚙️ Configuración Avanzada

### Parámetros del ESP32 (`main.py`)
- **Baudrate UART**: 9600 bps (TX=17, RX=16)
- **Puerto**: 80 (servidor web HTTP)

### Parámetros del Arduino (`grua_arduino.ino`)
- **Constantes de Velocidad Máxima (PWM 0-255)**:
  - `MAX_SPEED_CARRO`: 255
  - `MAX_SPEED_ELEVACION`: 255
  - `MAX_SPEED_GIRO`: 200
- **Zona Muerta del Joystick**: `DEADBAND_LOW = 400`, `DEADBAND_HIGH = 600`
- **Timeout Web**: `500` ms (solo activo en modo Web)
- **Debounce de Botón**: `50` ms

---

## 📡 API de Comandos del ESP32

### Endpoint de Envío de Comando
```
GET /cmd?action=<COMMAND>
```
Retorna `"OK"` en caso de éxito.

### Comandos de Movimiento y Control
| Comando | Acción en Arduino |
|---------|-----------|
| `F` | Mover Carro Adelante |
| `B` | Mover Carro Atrás |
| `U` | Subir Elevación (Gancho) |
| `D` | Bajar Elevación (Gancho) |
| `L` | Mover Giro Izquierda (Antihorario) |
| `R` | Mover Giro Derecha (Horario) |
| `S` | Detener todos los motores (Stop) |
| `M` | Alternar modo de control (Web <-> Manual) |

### Endpoint de Consulta de Modo
```
GET /mode
```
Retorna `"WEB"` o `"MANUAL"` según el estado sincronizado en el ESP32.

### Ejemplo
```
http://<IP_ESP32>/cmd?action=U
```

---

## 🐛 Solución de Problemas

### La interfaz web no carga
- Verificar IP y puerto del ESP32
- Comprobar conexión WiFi
- Revisar logs en el serial monitor

### Los motores no responden
- Verificar conexiones de alimentación 12V
- Revisar pines en Arduino según esquema
- Comprobar valores UART en comunicación ESP32-Arduino
- Probar con comandos individuales en serial

### Latencia alta
- Acercar el cliente al ESP32
- Revisar calidad de la red WiFi
- Reducir tráfico de red

---

## 📝 Licencia

Proyecto de Grado - Milagros Llusca

---

## 👥 Contribuciones

Reportar bugs y solicitudes de mejora en el repositorio del proyecto.

