// Define the pins for the 5 fingers
int ledPins[] = {2, 3, 4, 5, 6}; 

void setup() {
  // Start serial communication at 9600 baud rate
  Serial.begin(9600);
  
  // Set all LED pins as OUTPUT
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming string until a newline character
    String fingerData = Serial.readStringUntil('\n');
    
    // Ensure we received exactly 5 characters (one for each finger)
    if (fingerData.length() >= 5) {
      for (int i = 0; i < 5; i++) {
        if (fingerData[i] == '1') {
          digitalWrite(ledPins[i], HIGH);
        } else if (fingerData[i] == '0') {
          digitalWrite(ledPins[i], LOW);
        }
      }
    }
  }
}