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
- **Carro**: Movimiento horizontal izquierda/derecha (Motor DC N20)
- **Elevación**: Movimiento vertical arriba/abajo (Motor DC N20)
- **Giro**: Rotación continua (Motor Stepper NEMA 17)

### Interfaz de Usuario
- Panel de control moderno con gradientes y efectos glassmorphism
- Joystick virtual para control intuitivo
- Indicador de estado en tiempo real
- Diseño responsive adaptable a móviles

### Comunicación
- Protocolo HTTP/REST entre ESP32 y cliente web
- Comunicación UART entre ESP32 y Arduino
- Control por comandos simples (F, B, L, R, U, D, CW, CCW)

---

## 🔧 Requisitos Técnicos

### Hardware
- **ESP32** (módulo WiFi)
- **Arduino Uno**
- **2x Motor DC N20** (12V) con reducción
- **1x Motor Stepper NEMA 17** (12V, 1.9A)
- **Driver TB6612FNG** (para motores DC)
- **Driver DRV8825** (para motor stepper)
- **2x Joystick analógicos**
- **Fuente de alimentación 12V**

### Software
- MicroPython (ESP32)
- Arduino IDE (Arduino Uno)
- Python 3.x (para servidor de pruebas)
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
├── test_server.py         # Servidor de pruebas (simulación)
└── README.md             # Este archivo
```

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

**Arduino - Motors:**
- Pin 2, 4, 3: Motor Carro (TB6612FNG)
- Pin 7, 8, 5: Motor Elevación (TB6612FNG)
- Pin 9, 10: Motor Giro (DRV8825)

**Arduino - Joysticks:**
- A0: Joystick X (Carro)
- A1: Joystick Y (Elevación)
- A2: Joystick Z (Giro)

### Usar la Interfaz Web

1. **Conectarse a la Red WiFi:**
   - El ESP32 crea una red WiFi o se conecta a una existente
   - Abrir navegador y acceder a `http://<IP_ESP32>:8080`

2. **Controlar la Grúa:**
   - Usar los botones direccionales o joystick virtual
   - **Arriba/Abajo**: Elevar/Bajar
   - **Izquierda/Derecha**: Mover carro
   - **CW/CCW**: Girar en sentido horario/antihorario
   - **STOP**: Detener todos los movimientos

3. **Indicadores:**
   - Punto verde indica conexión activa
   - Latencia visible en tiempo real

### Modo de Prueba

Para pruebas sin hardware:
```bash
python test_server.py
# Se abrirá localhost:8080 con servidor simulado
```

---

## ⚙️ Configuración Avanzada

### Parámetros del ESP32 (`main.py`)
- `BAUDRATE`: 9600 (velocidad UART con Arduino)
- `PUERTO`: 8080 (puerto web)

### Parámetros del Arduino (`grua_arduino.ino`)
- `DEADBAND_LOW/HIGH`: 400/600 (zona muerta del joystick)
- `WEB_TIMEOUT_MS`: 500 (timeout para comandos web)
- `MAX_SPEED`: 1000 pasos/seg (motor stepper)

### Velocidades de Motores
Modificables en el código Arduino en `MOTOR_SPEED_*` constantes

---

## 📡 API de Comandos

### Endpoint
```
GET /cmd?action=<COMMAND>
```

### Comandos Disponibles
| Comando | Descripción |
|---------|-----------|
| `F` | Carro Adelante |
| `B` | Carro Atrás |
| `L` | Mover Izquierda |
| `R` | Mover Derecha |
| `U` | Elevar |
| `D` | Bajar |
| `CW` | Girar Horario |
| `CCW` | Girar Antihorario |
| `S` | Stop/Detener |

### Ejemplo
```
http://192.168.1.100:8080/cmd?action=U
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

