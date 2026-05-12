#include <AccelStepper.h>

// Definición de Pines para Joysticks
const int JOY_X_PIN = A0;   // Carro
const int JOY_Y_PIN = A1;   // Elevación
const int JOY_Z_PIN = A2;   // Giro (Stepper)

// Definición de Pines para TB6612FNG (Motores DC N20)
const int AIN1_PIN = 2;     // Motor A - Dirección 1 (Carro)
const int AIN2_PIN = 4;     // Motor A - Dirección 2 (Carro)
const int PWMA_PIN = 3;     // Motor A - PWM (Carro)

const int BIN1_PIN = 7;     // Motor B - Dirección 1 (Elevación)
const int BIN2_PIN = 8;     // Motor B - Dirección 2 (Elevación)
const int PWMB_PIN = 5;     // Motor B - PWM (Elevación)

// Definición de Pines para DRV8825 (Motor a Pasos Nema 17)
const int STEP_PIN = 9;
const int DIR_PIN = 10;

// Instancia del Motor a Pasos
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

// Constantes de Control
const int DEADBAND_LOW = 400;
const int DEADBAND_HIGH = 600;
const unsigned long WEB_TIMEOUT_MS = 500; // Si no hay comando web en 500ms, detener

// Variables de Estado Web
char webCommand = 'S';
unsigned long lastWebCommandTime = 0;

void setup() {
  Serial.begin(9600);
  
  // Configuración de Pines Motores DC
  pinMode(AIN1_PIN, OUTPUT);
  pinMode(AIN2_PIN, OUTPUT);
  pinMode(PWMA_PIN, OUTPUT);
  
  pinMode(BIN1_PIN, OUTPUT);
  pinMode(BIN2_PIN, OUTPUT);
  pinMode(PWMB_PIN, OUTPUT);
  
  // Inicialmente apagados
  detenerCarro();
  detenerElevacion();
  
  // Configuración Motor a Pasos
  stepper.setMaxSpeed(1000);  // Pasos por segundo
  stepper.setAcceleration(500);
}

void loop() {
  leerComandoWeb();
  
  // Lectura de Joysticks
  int joyX = analogRead(JOY_X_PIN);
  int joyY = analogRead(JOY_Y_PIN);
  int joyZ = analogRead(JOY_Z_PIN);
  
  controlarCarro(joyX);
  controlarElevacion(joyY);
  controlarGiro(joyZ);
  
  // El motor a pasos requiere llamadas constantes a run() o runSpeed()
  stepper.runSpeed(); 
}

void leerComandoWeb() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    // Validar comandos
    if (cmd == 'F' || cmd == 'B' || cmd == 'U' || cmd == 'D' || cmd == 'L' || cmd == 'R' || cmd == 'S') {
      webCommand = cmd;
      lastWebCommandTime = millis();
    }
  }
  
  // Verificar Timeout Web
  if (millis() - lastWebCommandTime > WEB_TIMEOUT_MS) {
    webCommand = 'S';
  }
}

void controlarCarro(int joyVal) {
  int velocidad = 0;
  
  if (joyVal < DEADBAND_LOW) {
    // Adelante manual
    velocidad = map(joyVal, DEADBAND_LOW, 0, 0, 255);
    moverCarro(true, velocidad);
  } else if (joyVal > DEADBAND_HIGH) {
    // Atrás manual
    velocidad = map(joyVal, DEADBAND_HIGH, 1023, 0, 255);
    moverCarro(false, velocidad);
  } else {
    // Zona muerta joystick - Verificar Web
    if (webCommand == 'F') moverCarro(true, 255);
    else if (webCommand == 'B') moverCarro(false, 255);
    else detenerCarro();
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

void controlarElevacion(int joyVal) {
  int velocidad = 0;
  
  if (joyVal < DEADBAND_LOW) {
    // Bajar manual
    velocidad = map(joyVal, DEADBAND_LOW, 0, 0, 255);
    moverElevacion(false, velocidad);
  } else if (joyVal > DEADBAND_HIGH) {
    // Subir manual
    velocidad = map(joyVal, DEADBAND_HIGH, 1023, 0, 255);
    moverElevacion(true, velocidad);
  } else {
    // Zona muerta joystick - Verificar Web
    if (webCommand == 'U') moverElevacion(true, 255);
    else if (webCommand == 'D') moverElevacion(false, 255);
    else detenerElevacion();
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

void controlarGiro(int joyVal) {
  float velocidadStepper = 0;
  
  if (joyVal < DEADBAND_LOW) {
    // Giro Izquierda manual
    velocidadStepper = map(joyVal, DEADBAND_LOW, 0, 0, -1000); // Negativo
    stepper.setSpeed(velocidadStepper);
  } else if (joyVal > DEADBAND_HIGH) {
    // Giro Derecha manual
    velocidadStepper = map(joyVal, DEADBAND_HIGH, 1023, 0, 1000); // Positivo
    stepper.setSpeed(velocidadStepper);
  } else {
    // Zona muerta joystick - Verificar Web
    if (webCommand == 'L') stepper.setSpeed(-500); // Velocidad fija web
    else if (webCommand == 'R') stepper.setSpeed(500);
    else stepper.setSpeed(0);
  }
}
