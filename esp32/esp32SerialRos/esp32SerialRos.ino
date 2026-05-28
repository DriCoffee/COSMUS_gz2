#include <Arduino.h>

String inputBuffer = "";

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("COSMUS_ESP32_READY");
}

void loop() {

  // ── 1. Enviar comandos ao Gazebo via ROS ──────────────────
  // Digite no Serial Monitor: T:500  E:0.3  R:0.2
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      inputBuffer.trim();
      if (inputBuffer.length() > 0) {
        Serial.println(inputBuffer);  // nó ROS lê e publica
      }
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }

  // ── 2. Receber dados do Gazebo (enviados pelo nó ROS) ─────
  // O nó Python escreve "IMU:..." e "GPS:..." na serial
  // Nada a fazer aqui — o Serial Monitor já imprime automaticamente
  // Caso queira tratar os dados no ESP32, adicione lógica aqui:
  //
   if (Serial.available()) {
     String dados = Serial.readStringUntil('\n');
     if (dados.startsWith("IMU:")) { /* parsear */ }
     if (dados.startsWith("GPS:")) { /* parsear */ }
   }
}
