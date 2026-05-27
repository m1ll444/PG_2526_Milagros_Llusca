## ADDED Requirements

### Requirement: Canal SoftwareSerial de depuración
El Arduino SHALL configurar un puerto serie emulado por software (SoftwareSerial) en los pines D10 (RX) y D13 (TX) a 9600 bps, dedicado exclusivamente al envío de trazas de depuración hacia el ESP32.

#### Scenario: Inicialización del canal de depuración
- **WHEN** El Arduino arranca en su rutina `setup()`.
- **THEN** El sistema SHALL inicializar SoftwareSerial en los pines D10/D13 a 9600 bps y enviar una línea "[BOOT] Sistema iniciado" por este canal.

### Requirement: Envío de trazas de log por SoftwareSerial
El Arduino SHALL enviar mensajes de estado textuales, logs de eventos y cambios de modo exclusivamente por el puerto SoftwareSerial, no por el Serial hardware USB.

#### Scenario: Log de cambio de modo
- **WHEN** El modo de control cambia de Manual a Web (o viceversa) por botón físico o comando `M`.
- **THEN** El Arduino SHALL enviar una línea como `[MODE] Cambiado a WEB` o `[MODE] Cambiado a MANUAL` por el canal SoftwareSerial.

#### Scenario: Log de comando web recibido
- **WHEN** El Arduino recibe un comando de movimiento válido (`F`, `B`, `U`, `D`, `L`, `R`, `S`) por el Serial USB.
- **THEN** El Arduino SHALL enviar una línea como `[CMD] Recibido: F` por el canal SoftwareSerial.

### Requirement: Buffer circular de logs en ESP32
El ESP32 SHALL leer las líneas de texto recibidas por su UART RX (GPIO 16, conectado a D13 TX del Arduino) y almacenarlas en una lista circular de máximo 50 líneas en RAM.

#### Scenario: Almacenamiento de log recibido
- **WHEN** El ESP32 recibe una línea completa (terminada en `\n`) por su UART RX.
- **THEN** El sistema SHALL añadir la línea al final de la lista circular, descartando la línea más antigua si el buffer ya contiene 50 líneas.

### Requirement: Servidor web de depuración ultraliviano
El ESP32 SHALL servir en el puerto 80 una página HTML de depuración con estética de terminal retro (fondo negro, texto verde monoespacio) que muestre las últimas 50 líneas de log almacenadas en el buffer. La página SHALL implementar auto-refresco automático cada 2 segundos mediante `<meta http-equiv="refresh" content="2">`.

#### Scenario: Carga de la página de depuración desde el celular
- **WHEN** Un usuario accede a `http://<IP_ESP32>/` desde cualquier navegador (incluido el de un celular).
- **THEN** El ESP32 SHALL generar dinámicamente una página HTML de menos de 2KB con el contenido actual del buffer de logs, ordenado del más antiguo al más reciente, con auto-refresco configurado a 2 segundos.

#### Scenario: Visualización de logs en tiempo real
- **WHEN** La página de depuración se auto-refresca después de 2 segundos.
- **THEN** La página SHALL mostrar las líneas de log más recientes disponibles en el buffer circular, reflejando cualquier nuevo log recibido desde la última carga.
