// defines pins numbers for the first sensor
const int trigPin1 = A1;
const int echoPin1 = A3;

// defines pins numbers for the second sensor
const int trigPin2 = A4;
const int echoPin2 = A2;

// defines variables for the first sensor
long duration1;
int distance1;

// defines variables for the second sensor
long duration2;
int distance2;

void setup() {
  pinMode(trigPin1, OUTPUT); // Sets the trigPin1 as an Output
  pinMode(echoPin1, INPUT);  // Sets the echoPin1 as an Input

  pinMode(trigPin2, OUTPUT); // Sets the trigPin2 as an Output
  pinMode(echoPin2, INPUT);  // Sets the echoPin2 as an Input
  
  Serial.begin(9600); // Starts the serial communication
}

void loop() {
  // ------- Readings from the first sensor ----------
  digitalWrite(trigPin1, LOW);          // Clears the trigPin1
  delayMicroseconds(2);
  
  digitalWrite(trigPin1, HIGH);         // Sets the trigPin1 on HIGH state for 10 microseconds
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  
  duration1 = pulseIn(echoPin1, HIGH);  // Reads the echoPin1, returns the sound wave travel time in microseconds
  
  distance1 = duration1 * 0.034 / 2;     // Calculating the distance for the first sensor
  
  Serial.print("Distance 1: ");         // Prints the distance from the first sensor on the Serial Monitor
  Serial.println(distance1);


  //delay to avoid interference
  delayMicroseconds(100);
  //
  
  // ------- Readings from the second sensor ----------
  digitalWrite(trigPin2, LOW);          // Clears the trigPin2
  delayMicroseconds(2);
  
  digitalWrite(trigPin2, HIGH);         // Sets the trigPin2 on HIGH state for 10 microseconds
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);
  
  duration2 = pulseIn(echoPin2, HIGH);  // Reads the echoPin2, returns the sound wave travel time in microseconds
  
  distance2 = duration2 * 0.034 / 2;     // Calculating the distance for the second sensor
  
  Serial.print("Distance 2: ");         // Prints the distance from the second sensor on the Serial Monitor
  Serial.println(distance2);

  delay(100); // Delay between readings
}
