// ============================================================
// Grúa Torre - Firmware Arduino
// Control de 3 motores DC con modo dual (Web / Manual)
// ============================================================

// ---- Velocidades Máximas Configurables (PWM 0-255) ----
const int MAX_SPEED_CARRO = 255;
const int MAX_SPEED_ELEVACION = 255;
const int MAX_SPEED_GIRO = 200;

// ---- Pines Joysticks ----
const int JOY_X_PIN = A0;   // Carro
const int JOY_Y_PIN = A1;   // Elevación
const int JOY_Z_PIN = A2;   // Giro

// ---- Pines TB6612FNG #1 (Motores DC N20: Carro y Elevación) ----
const int AIN1_PIN = 2;     // Motor A - Dirección 1 (Carro)
const int AIN2_PIN = 4;     // Motor A - Dirección 2 (Carro)
const int PWMA_PIN = 3;     // Motor A - PWM (Carro)

const int BIN1_PIN = 7;     // Motor B - Dirección 1 (Elevación)
const int BIN2_PIN = 8;     // Motor B - Dirección 2 (Elevación)
const int PWMB_PIN = 5;     // Motor B - PWM (Elevación)

// ---- Pines TB6612FNG #2 (Motoreductor DC 30RPM: Giro) ----
const int CIN1_PIN = 11;    // Motor C - Dirección 1 (Giro)
const int CIN2_PIN = 12;    // Motor C - Dirección 2 (Giro)
const int PWMC_PIN = 9;     // Motor C - PWM (Giro)

// ---- Pin Botón de Modo (Joystick Button) ----
const int BUTTON_MODE_PIN = 6;

// ---- Constantes de Control ----
const int DEADBAND_LOW = 400;
const int DEADBAND_HIGH = 600;
const unsigned long WEB_TIMEOUT_MS = 500;

// ---- Constantes de Debounce ----
const unsigned long DEBOUNCE_MS = 50;

// ---- Variables de Estado ----
char webCommand = 'S';
unsigned long lastWebCommandTime = 0;
bool modoWeb = false;               // false = Manual, true = Web
unsigned long lastTelemetryTime = 0;
const unsigned long TELEMETRY_INTERVAL_MS = 100;

// ---- Variables de Debounce del Botón ----
bool lastButtonState = HIGH;         // Pull-up: reposo = HIGH
bool buttonState = HIGH;
unsigned long lastDebounceTime = 0;

void setup() {
  Serial.begin(9600);

  // Configuración de Pines Motores DC (TB6612FNG #1)
  pinMode(AIN1_PIN, OUTPUT);
  pinMode(AIN2_PIN, OUTPUT);
  pinMode(PWMA_PIN, OUTPUT);

  pinMode(BIN1_PIN, OUTPUT);
  pinMode(BIN2_PIN, OUTPUT);
  pinMode(PWMB_PIN, OUTPUT);

  // Configuración de Pines Motor Giro DC (TB6612FNG #2)
  pinMode(CIN1_PIN, OUTPUT);
  pinMode(CIN2_PIN, OUTPUT);
  pinMode(PWMC_PIN, OUTPUT);

  // Configuración del Botón de Modo
  pinMode(BUTTON_MODE_PIN, INPUT_PULLUP);

  // Inicialmente apagados
  detenerCarro();
  detenerElevacion();
  detenerGiro();

  // Enviar estado de modo inicial al ESP32
  Serial.print("S:J,S,S,S\n"); // Telemetría inicial: Manual, detenido
}

void loop() {
  leerComandoWeb();
  leerBotonModo();

  // Lectura de Joysticks
  int joyX = analogRead(JOY_X_PIN);
  int joyY = analogRead(JOY_Y_PIN);
  int joyZ = analogRead(JOY_Z_PIN);

  controlarCarro(joyX);
  controlarElevacion(joyY);
  controlarGiro(joyZ);

  enviarTelemetria(joyX, joyY, joyZ);
}

// ============================================================
// Envío de Telemetría Serial al ESP32
// ============================================================
void enviarTelemetria(int joyX, int joyY, int joyZ) {
  if (millis() - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = millis();
    
    char carroDir = 'S';
    char elevDir = 'S';
    char giroDir = 'S';
    
    if (modoWeb) {
      if (webCommand == 'F') carroDir = 'F';
      else if (webCommand == 'B') carroDir = 'B';
      
      if (webCommand == 'U') elevDir = 'U';
      else if (webCommand == 'D') elevDir = 'D';
      
      if (webCommand == 'L') giroDir = 'L';
      else if (webCommand == 'R') giroDir = 'R';
    } else {
      if (joyX < DEADBAND_LOW) carroDir = 'F';
      else if (joyX > DEADBAND_HIGH) carroDir = 'B';
      
      if (joyY < DEADBAND_LOW) elevDir = 'D';
      else if (joyY > DEADBAND_HIGH) elevDir = 'U';
      
      if (joyZ < DEADBAND_LOW) giroDir = 'L';
      else if (joyZ > DEADBAND_HIGH) giroDir = 'R';
    }
    
    Serial.print("S:");
    Serial.print(modoWeb ? 'W' : 'J');
    Serial.print(",");
    Serial.print(carroDir);
    Serial.print(",");
    Serial.print(elevDir);
    Serial.print(",");
    Serial.println(giroDir);
  }
}

// ============================================================
// Lectura de comandos UART desde ESP32
// ============================================================
void leerComandoWeb() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();

    // Comando de cambio de modo
    if (cmd == 'M') {
      modoWeb = !modoWeb;
      Serial.write(modoWeb ? 'W' : 'J');
      // Al cambiar de modo, detener todos los motores por seguridad
      webCommand = 'S';
      detenerCarro();
      detenerElevacion();
      detenerGiro();
      return;
    }

    // Comandos de movimiento (solo válidos en modo web)
    if (cmd == 'F' || cmd == 'B' || cmd == 'U' || cmd == 'D' ||
        cmd == 'L' || cmd == 'R' || cmd == 'S') {
      webCommand = cmd;
      lastWebCommandTime = millis();
    }
  }

  // Verificar Timeout Web (solo en modo web)
  if (modoWeb && (millis() - lastWebCommandTime > WEB_TIMEOUT_MS)) {
    webCommand = 'S';
  }
}

// ============================================================
// Lectura del botón físico con debounce
// ============================================================
void leerBotonModo() {
  bool reading = digitalRead(BUTTON_MODE_PIN);

  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > DEBOUNCE_MS) {
    if (reading != buttonState) {
      buttonState = reading;

      // Flanco de bajada (botón presionado con pull-up)
      if (buttonState == LOW) {
        modoWeb = !modoWeb;
        Serial.write(modoWeb ? 'W' : 'J');
        // Al cambiar de modo, detener todos los motores por seguridad
        webCommand = 'S';
        detenerCarro();
        detenerElevacion();
        detenerGiro();
      }
    }
  }

  lastButtonState = reading;
}

// ============================================================
// Control del Carro (Motor DC A - TB6612FNG #1)
// ============================================================
void controlarCarro(int joyVal) {
  if (modoWeb) {
    // Modo Web: solo comandos UART
    if (webCommand == 'F') moverCarro(true, MAX_SPEED_CARRO);
    else if (webCommand == 'B') moverCarro(false, MAX_SPEED_CARRO);
    else detenerCarro();
  } else {
    // Modo Manual: solo joystick
    if (joyVal < DEADBAND_LOW) {
      int velocidad = map(joyVal, DEADBAND_LOW, 0, 0, MAX_SPEED_CARRO);
      moverCarro(true, velocidad);
    } else if (joyVal > DEADBAND_HIGH) {
      int velocidad = map(joyVal, DEADBAND_HIGH, 1023, 0, MAX_SPEED_CARRO);
      moverCarro(false, velocidad);
    } else {
      detenerCarro();
    }
  }
}

void moverCarro(bool adelante, int velocidad) {
  digitalWrite(AIN1_PIN, adelante ? HIGH : LOW);
  digitalWrite(AIN2_PIN, adelante ? LOW : HIGH);
  analogWrite(PWMA_PIN, velocidad);
}

void detenerCarro() {
  digitalWrite(AIN1_PIN, LOW);
  digitalWrite(AIN2_PIN, LOW);
  analogWrite(PWMA_PIN, 0);
}

// ============================================================
// Control de Elevación (Motor DC B - TB6612FNG #1)
// ============================================================
void controlarElevacion(int joyVal) {
  if (modoWeb) {
    // Modo Web: solo comandos UART
    if (webCommand == 'U') moverElevacion(true, MAX_SPEED_ELEVACION);
    else if (webCommand == 'D') moverElevacion(false, MAX_SPEED_ELEVACION);
    else detenerElevacion();
  } else {
    // Modo Manual: solo joystick
    if (joyVal < DEADBAND_LOW) {
      int velocidad = map(joyVal, DEADBAND_LOW, 0, 0, MAX_SPEED_ELEVACION);
      moverElevacion(false, velocidad);
    } else if (joyVal > DEADBAND_HIGH) {
      int velocidad = map(joyVal, DEADBAND_HIGH, 1023, 0, MAX_SPEED_ELEVACION);
      moverElevacion(true, velocidad);
    } else {
      detenerElevacion();
    }
  }
}

void moverElevacion(bool subir, int velocidad) {
  digitalWrite(BIN1_PIN, subir ? HIGH : LOW);
  digitalWrite(BIN2_PIN, subir ? LOW : HIGH);
  analogWrite(PWMB_PIN, velocidad);
}

void detenerElevacion() {
  digitalWrite(BIN1_PIN, LOW);
  digitalWrite(BIN2_PIN, LOW);
  analogWrite(PWMB_PIN, 0);
}

// ============================================================
// Control de Giro (Motoreductor DC C - TB6612FNG #2)
// ============================================================
void controlarGiro(int joyVal) {
  if (modoWeb) {
    // Modo Web: solo comandos UART
    if (webCommand == 'L') moverGiro(false, MAX_SPEED_GIRO);
    else if (webCommand == 'R') moverGiro(true, MAX_SPEED_GIRO);
    else detenerGiro();
  } else {
    // Modo Manual: solo joystick
    if (joyVal < DEADBAND_LOW) {
      int velocidad = map(joyVal, DEADBAND_LOW, 0, 0, MAX_SPEED_GIRO);
      moverGiro(false, velocidad);
    } else if (joyVal > DEADBAND_HIGH) {
      int velocidad = map(joyVal, DEADBAND_HIGH, 1023, 0, MAX_SPEED_GIRO);
      moverGiro(true, velocidad);
    } else {
      detenerGiro();
    }
  }
}

void moverGiro(bool horario, int velocidad) {
  digitalWrite(CIN1_PIN, horario ? HIGH : LOW);
  digitalWrite(CIN2_PIN, horario ? LOW : HIGH);
  analogWrite(PWMC_PIN, velocidad);
}

void detenerGiro() {
  digitalWrite(CIN1_PIN, LOW);
  digitalWrite(CIN2_PIN, LOW);
  analogWrite(PWMC_PIN, 0);
}
