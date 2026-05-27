# Sistema de Control de Grúa Torre - PG_2526

## 📋 Descripción del Proyecto

Sistema integral de control remoto para una grúa torre con componentes IoT. Permite el control en tiempo real de movimientos (carro, elevación y giro) mediante una interfaz web responsiva.

**Componentes principales:**
- **Arduino Uno**: Controlador principal de motores y sensores.
- **Interfaz Web (Web Serial)**: Panel de control web local que se comunica directamente por USB.
- **ESP32**: Servidor inalámbrico de depuración y logs de la grúa.

---

## 🎯 Características Principales

### Control de Movimientos
- **Carro**: Movimiento horizontal adelante/atrás (Motor DC N20 con reductora 12V)
- **Elevación**: Movimiento vertical subir/bajar (Motor DC N20 con reductora 12V)
- **Giro**: Rotación horaria/antihoraria (Motoreductor DC 30RPM 12V)

### Interfaz de Usuario e Interacción
- Panel de control moderno con gradientes y efectos glassmorphism.
- Switch toggle para control dual (Web / Manual) que inhabilita los controles web en modo manual.
- Indicador visual del modo de control activo y sincronización en tiempo real vía Web Serial.
- Botones táctiles grandes y responsivos para control remoto.
- Botón de parada de emergencia prominente.

### Comunicación
- **Canal Principal**: Control directo desde el navegador vía **Web Serial API** conectado por cable USB al Serial Hardware del Arduino (pines D0/D1) a 9600 bps.
- **Canal de Depuración**: SoftwareSerial en Arduino (pines D10 RX / D13 TX) enviando trazas a la UART del ESP32 (GPIO 16 RX) a 9600 bps.
- **Canal de Respaldo**: Peticiones HTTP/REST al ESP32 si este actúa como gateway.

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
├── arduino/               # Código C++ para Arduino Uno
│   └── grua_arduino/
│       └── grua_arduino.ino # Firmware de control de motores y sensores
├── esp32/                 # Código MicroPython para ESP32
│   ├── boot.py           # Configuración de inicio (WiFi)
│   └── main.py           # Servidor de logs de depuración (terminal retro)
├── web_server/            # Archivos de la interfaz web
│   ├── index.html        # Panel de control (Web Serial API con fallback HTTP)
│   └── schema.html       # Esquema de conexiones electrónicas interactivo
├── openspec/              # Especificaciones basadas en comportamiento
│   ├── config.yaml       # Configuración de OpenSpec
│   └── specs/            # Especificaciones de capacidades
└── README.md             # Este archivo
```

---

## 📖 Especificaciones del Sistema (OpenSpec) y Esquemas

Este proyecto adopta **OpenSpec** para documentar formalmente los requerimientos y comportamientos esperados del sistema mediante especificaciones ejecutables basadas en escenarios:

*   [Comunicación UART](openspec/specs/comunicacion-uart/spec.md): Protocolo serie y comandos de control bidireccionales entre navegador/ESP32 y Arduino.
*   [Servidor Web](openspec/specs/servidor-web/spec.md): Terminal de logs en MicroPython expuesta por el ESP32.
*   [Control de Motores](openspec/specs/control-motores/spec.md): Control de hardware para los 3 motores DC, límites de velocidad y logs SoftwareSerial.
*   [Lógica de Prioridad y Seguridad](openspec/specs/control-prioridad-seguridad/spec.md): Exclusividad de los modos y temporización de seguridad.
*   [Modo de Control Dual](openspec/specs/modo-control-dual/spec.md): Conmutación e intercambio de señales de sincronización.
*   [Esquema de Conexiones](openspec/specs/schema-conexiones/spec.md): Especificación del esquema de hardware interactivo.

Adicionalmente, puedes consultar el documento de conexiones de hardware:
*   [Esquema Electrónico Interactivo (web_server/schema.html)](web_server/schema.html): Contiene el diagrama de bloques SVG actualizado y la tabla pin-a-pin interactiva.

---

## 🚀 Guía de Usuario

### Instalación Inicial

#### 1. Configurar ESP32
```bash
# Instalar MicroPython en ESP32 (usar esptool.py o Thonny IDE)
# Cargar boot.py y main.py de la carpeta esp32/ al ESP32
```

#### 2. Configurar Arduino
```bash
# Abrir Arduino IDE
# Cargar el código desde arduino/grua_arduino/grua_arduino.ino
# Verificar conexión de pines según el esquema
```

#### 3. Conexiones de Hardware
Para ver todas las conexiones de pines y la topología física detallada, consulta el archivo [schema.html](web_server/schema.html) o la especificación de conexiones.
Resumen de conexiones clave (Arduino):
- **Motor Carro (TB6612FNG #1)**: AIN1 (D2), AIN2 (D4), PWMA (D3)
- **Motor Elevación (TB6612FNG #1)**: BIN1 (D7), BIN2 (D8), PWMB (D5)
- **Motor Giro (TB6612FNG #2)**: CIN1 (D11), CIN2 (D12), PWMC (D9)
- **SoftwareSerial Logs (a ESP32)**: D10 (RX - libre / no conectado), D13 (TX -> GPIO 16 RX de ESP32)
- **Joysticks**: X (Carro) -> A0, Y (Elevación) -> A1, Z (Giro) -> A2
- **Botón de Modo (Pulsador)**: D6

### Usar la Interfaz Web de Control

1. **Abrir la Interfaz de Control:**
   - Abrir el archivo `web_server/index.html` localmente en un navegador compatible con Web Serial API (Google Chrome, Microsoft Edge, Opera).

2. **Conectar el Puerto USB:**
   - Hacer clic en el botón **"Conectar USB"** en el encabezado.
   - En el diálogo emergente del navegador, seleccionar el puerto serie correspondiente a la placa Arduino Uno/Nano y pulsar "Conectar". El indicador cambiará a **"USB Conectado"**.

3. **Controlar la Grúa:**
   - Activar el switch **WEB** para habilitar el control remoto. En modo **MANUAL**, los controles web estarán deshabilitados.
   - Mantener pulsado el botón de la dirección deseada para mover la grúa, y soltarlo para detenerla.
   - Presionar **PARADA / STOP** para una detención total inmediata.

### Usar la Terminal Inalámbrica de Logs (ESP32)

1. **Conectarse a la Red WiFi:**
   - Conectarse al punto de acceso WiFi emitido por el ESP32 (por defecto "Grua_Torre_Debug" o la red configurada en `boot.py`).
   - Abrir el navegador en el móvil o PC e ingresar a `http://192.168.4.1` (o la IP del ESP32).
   - Se mostrará la terminal retro verde y negra con los últimos 50 logs de operación de la grúa, auto-refrescándose cada 2 segundos.

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

