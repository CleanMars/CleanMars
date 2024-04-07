#include <Servo.h>

// Define the servo pin
const int servoPin = A5; // Change this to the pin you're using
Servo servo;

void setup() {
  // Initialize the servo object
  servo.attach(servoPin);
  
  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Check if data is available on serial port
  if (Serial.available() > 0) {
    // Read the integer value representing servo position
    int position = Serial.parseInt();
    
    // Input validation
    if (position >= 0 && position <= 180) {
      // Move the servo to the specified position
      servo.write(position);
    } else {
      // Invalid input, print an error message
      Serial.println("Error: Invalid position value. Please enter a value between 0 and 180.");
    }
  }
}
