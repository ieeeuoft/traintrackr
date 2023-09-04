void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(9600);
  Serial.flush();

}

void loop() {
  if (Serial.available() > 0) {
      digitalWrite(13, HIGH);
      String received = Serial.readStringUntil('\n');
      Serial.println("Received string: " + received);
      delay(2000);
      
      Serial.flush();
  }
  else {
    digitalWrite(13, LOW);
  }
}
