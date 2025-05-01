int leds[] = {8, 9, 10, 11, 12}; // Pulgar a meñique

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 5; i++) {
    pinMode(leds[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');

    // Apaga todos los LEDs primero
    for (int i = 0; i < 5; i++) {
      digitalWrite(leds[i], LOW);
    }

    // Enciende los LEDs según los caracteres recibidos
    for (int i = 0; i < data.length(); i++) {
      int ledIndex = data[i] - '1';  // convierte '1'..'5' a índice 0..4
      if (ledIndex >= 0 && ledIndex < 5) {
        digitalWrite(leds[ledIndex], HIGH);
      }
    }
  }
}

