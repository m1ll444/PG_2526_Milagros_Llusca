# Roadmap - Sistema de Control de Grúa Torre

> [!NOTE]
> **Alineación con OpenSpec:** Las características de la versión 1.0.0 están especificadas formalmente bajo la estructura de capacidades de OpenSpec en `openspec/specs/`. Las futuras características planificadas se diseñarán y verificarán mediante nuevas propuestas de cambio (`openspec change`) dentro de este marco de trabajo.

## 📅 Versión: 1.0.0 - Versión Base Funcional

**Estado**: ✅ Completado  
**Fecha**: Mayo 2026

### Características Implementadas

#### Core Functionality
- ✅ Servidor HTTP en ESP32 en puerto 8080
- ✅ Interfaz web responsiva con controles visuales
- ✅ Comunicación UART ESP32 ↔ Arduino (9600 baud)
- ✅ Joystick virtual en interfaz web
- ✅ Parada de emergencia (comando STOP)
- ✅ Indicador visual de conexión en tiempo real

#### Control de Motores
- ✅ Motor DC Carro (izquierda/derecha)
- ✅ Motor DC Elevación (arriba/abajo)
- ✅ Motor Stepper Giro (horario/antihorario)
- ✅ Control por drivers dedicados (TB6612FNG, DRV8825)
- ✅ Deadband configurado para joysticks analógicos

#### Hardware Support
- ✅ Soporte ESP32 (WiFi integrado)
- ✅ Soporte Arduino Uno (control de motores)
- ✅ 3 joysticks analógicos
- ✅ Fuente de alimentación dual (ESP32 + motores)

---

## 🚀 Versión 2.0.0 - Mejoras de Seguridad y Monitoreo

**Estado**: 🔄 Planeado  
**Timeline**: Q3 2026

### Nuevas Funcionalidades

#### Seguridad Avanzada
- [ ] Autenticación básica (usuario/contraseña)
- [ ] Certificado SSL/TLS para conexiones HTTPS
- [ ] Rate limiting en API de comandos
- [ ] Timeout de inactividad (auto-desconexión)
- [ ] Verificación de integridad de comandos

#### Monitoreo y Telemetría
- [ ] Sensores de límite (fin de carrera)
- [ ] Monitoreo de temperatura de motores
- [ ] Medición de corriente consumida
- [ ] Historial de comandos ejecutados
- [ ] Logs de errores y excepciones

#### Mejoras de Control
- [ ] Perfiles de velocidad configurables
- [ ] Aceleración gradual de motores
- [ ] Control de precisión para movimientos pequeños
- [ ] Secuencias programadas de movimientos

---

## 🔌 Versión 2.1.0 - Conectividad Mejorada

**Estado**: 🔄 Planeado  
**Timeline**: Q3 2026

### Nuevas Características

#### Opciones de Conexión
- [ ] Conexión WiFi automática en reboot
- [ ] Soporte para múltiples redes WiFi
- [ ] Fallback a modo Access Point si falla conexión
- [ ] Sincronización de hora NTP
- [ ] API REST mejorada con versionado

#### Comunicación Bidireccional
- [ ] WebSocket para feedback en tiempo real
- [ ] Publicación de estado en MQTT (opcional)
- [ ] Endpoint para obtener estado del sistema
- [ ] Notificaciones de eventos

---

## 📊 Versión 3.0.0 - Dashboard Profesional

**Estado**: 📋 Diseño  
**Timeline**: Q4 2026

### Interfaz Mejorada
- [ ] Dashboard con estadísticas en tiempo real
- [ ] Gráficas de uso de motores
- [ ] Heatmap de posiciones
- [ ] Panel administrativo
- [ ] Tema oscuro/claro personalizable
- [ ] Soporte para múltiples idiomas (ES/EN)

### Funcionalidades Avanzadas
- [ ] Grabación de sesiones
- [ ] Reproducción de movimientos guardados
- [ ] Calibración automática de límites
- [ ] Detección automática de hardware
- [ ] Firmware update OTA

---

## 🤖 Versión 3.1.0 - Automatización

**Estado**: 📋 Diseño  
**Timeline**: Q4 2026

### Características de Automatización
- [ ] Scheduler de tareas programadas
- [ ] Secuencias de movimiento parametrizables
- [ ] Triggers basados en sensores
- [ ] Integración con IFTTT
- [ ] API para automatización externa
- [ ] Escenarios predefinidos

---

## 🔧 Versión 4.0.0 - Arquitectura Escalable

**Estado**: 📋 Investigación  
**Timeline**: 2027

### Mejoras de Arquitectura
- [ ] Microservicios para componentes críticos
- [ ] Base de datos para historial
- [ ] Cluster de ESP32 para múltiples grúas
- [ ] Sistema de eventos distribuido
- [ ] API Gateway
- [ ] Caché distribuido

### DevOps
- [ ] CI/CD Pipeline
- [ ] Containerización (Docker)
- [ ] Testing automatizado
- [ ] Documentación API (Swagger)
- [ ] Monitoreo centralizado

---

## 📱 Versión 4.1.0 - Aplicación Móvil

**Estado**: 📋 Planeado  
**Timeline**: 2027

### Aplicación Nativa
- [ ] App iOS nativa (SwiftUI)
- [ ] App Android nativa (Jetpack Compose)
- [ ] Sincronización de datos
- [ ] Notificaciones push
- [ ] Geolocalización
- [ ] Modo offline

---

## 🎯 Cambios Futuros Considerados

### Optimizaciones
- [ ] Reducción de consumo de energía en ESP32
- [ ] Optimización de velocidad de respuesta
- [ ] Compresión de datos en comunicación
- [ ] Caché local en cliente web

### Expansión de Características
- [ ] Soporte para múltiples tipos de grúa
- [ ] Calibración de precisión con encoder óptico
- [ ] Control por visión (cámara)
- [ ] Integración con AR para visualización
- [ ] Machine Learning para predicción de fallas

### Hardware Adicional
- [ ] Cámara IP integrada
- [ ] Sensor de peso
- [ ] Sistema de iluminación LED
- [ ] Panel de control táctil independiente
- [ ] Batería UPS para ESP32

---

## 📈 Métricas de Seguimiento

### Hitos Completados (v1.0.0)
- ✅ Comunicación ESP32-Arduino establecida
- ✅ Interfaz web funcional
- ✅ Control de 3 ejes de movimiento
- ✅ Feedback visual de estado
- ✅ Servidor de pruebas para desarrollo

### KPIs a Monitorear
- **Latencia**: < 100ms (objetivo)
- **Uptime**: > 99% (objetivo)
- **Precisión de movimiento**: ±5mm (objetivo)
- **Alcance WiFi**: > 50m (objetivo)
- **Consumo de energía**: < 100W en reposo

---

## 🔄 Proceso de Cambios

### Workflow de Versiones
1. **Feature Branch**: Desarrollo de nuevas características
2. **Testing**: Validación en laboratorio
3. **Alpha Release**: Distribución limitada
4. **Beta Release**: Pruebas amplias
5. **Production Release**: Lanzamiento oficial

### Política de Versionado
- **Mayor.Menor.Patch** (ej: 1.0.0)
- Mayor: Cambios incompatibles
- Menor: Nuevas características compatibles
- Patch: Bug fixes

---

## 📞 Contacto y Feedback

Para sugerencias o reportar bugs:
- GitHub Issues: [Proyecto]
- Email: milagros.llusca@universidad.edu
- Discord: [Comunidad del Proyecto]

---

## 📄 Historial de Cambios

### v1.0.0 (Mayo 2026)
- **Release**: Sistema base funcional
- **Cambios principales**: Todas las características iniciales implementadas
- **Commits**: 15
- **Autora**: Milagros Llusca

### v0.9.0 (Abril 2026)
- **Beta**: Pruebas preliminares
- **Cambios**: Optimización de código Arduino

### v0.5.0 (Marzo 2026)
- **Alpha**: Integración ESP32-Arduino
- **Cambios**: Protocolo de comunicación UART

---

**Última actualización**: Mayo 22, 2026  
**Próxima revisión**: Agosto 2026
