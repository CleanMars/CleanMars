// #include <vector>
// #include <Vector.h>
// #include <vector>


#define PWMB 9
#define BIN2 8
#define BIN1 7
#define STBY 6
#define AIN1 5
#define AIN2 4
#define PWMA 3

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

template<typename T, typename U>
struct Pair {
  T first;
  U second;

  Pair()
    : first(), second() {}
  Pair(const T& a, const U& b)
    : first(a), second(b) {}
};


class Wheel {
private:
  uint8_t in1, in2;
public:
  Wheel() {}
  Wheel(uint8_t num1, uint8_t num2) {
    in1 = num1;
    in2 = num2;
    Serial.print("input1: ");
    Serial.println(in1);
    Serial.print("input2: ");
    Serial.println(in2);
    Serial.println("Wheel done.");
  }

  void move(bool direction) {
    // Serial.print("input1: ");
    // Serial.println(in1);
    // Serial.print("input2: ");
    // Serial.println(in2);
    // Serial.print("direction: ");
    // Serial.println(direction);
    // direction 1 -> forward
    // direction 0 -> backward
    digitalWrite(in1, direction);
    digitalWrite(in2, !direction);
  }

  void stop() {
    digitalWrite(in1, 0);
    digitalWrite(in2, 0);
  }
};

class Robot {
private:
  int leftWheelNumber, rightWheelNumber;
  Wheel* leftWheels;
  Wheel* rightWheels;
  // map

public:
  Robot() {}
  Robot(Pair<uint8_t, uint8_t>* leftW, Pair<uint8_t, uint8_t>* rightW) {
    leftWheelNumber = sizeof(leftW) / sizeof(leftW[0]);
    rightWheelNumber = sizeof(rightW) / sizeof(rightW[0]);

    leftWheels = new Wheel[leftWheelNumber];
    rightWheels = new Wheel[rightWheelNumber];

    for (int i = 0; i < leftWheelNumber; i++) {
      Serial.print(i);
      Serial.print(": ");
      Serial.print(leftW[i].first);
      Serial.print(", ");
      Serial.println(leftW[i].second);
      leftWheels[i] = Wheel(leftW[i].first, leftW[i].second);
    }
    for (int i = 0; i < rightWheelNumber; i++) {
      Serial.print(i);
      Serial.print(": ");
      Serial.print(rightW[i].first);
      Serial.print(", ");
      Serial.println(rightW[i].second);
      rightWheels[i] = Wheel(rightW[i].first, rightW[i].second);
    }

    Serial.println("done setting up");
  }

  void stop() {
    for (int i = 0; i < leftWheelNumber; i++) {
      leftWheels[i].stop();
    }
    for (int i = 0; i < rightWheelNumber; i++) {
      rightWheels[i].stop();
    }
  }

  void move(uint8_t power, char direction) {
    // if(digitalRead(2) == LOW) {
    //   Serial.println("clicked");
    //   digitalWrite(STBY, 1);
    // }
    analogWrite(PWMA, power);
    analogWrite(PWMB, power);
    if (direction == 'F') {
      // Serial.println(direction);
      for (int i = 0; i < leftWheelNumber; i++) {
        leftWheels[i].move(1);
      }
      for (int i = 0; i < rightWheelNumber; i++) {
        rightWheels[i].move(1);
      }
      return;
    }
    if (direction == 'R') {
      for (int i = 0; i < leftWheelNumber; i++) {
        leftWheels[i].stop();
      }
      for (int i = 0; i < leftWheelNumber; i++) {
        rightWheels[i].move(1);
      }
      return;
    }

    if (direction == 'L') {
      for (int i = 0; i < leftWheelNumber; i++) {
        leftWheels[i].move(1);
      }
      for (int i = 0; i < leftWheelNumber; i++) {
        rightWheels[i].stop();
      }
      return;
    }
    if (direction == 'B') {
      for (int i = 0; i < leftWheelNumber; i++) {
        leftWheels[i].move(0);
      }
      for (int i = 0; i < leftWheelNumber; i++) {
        rightWheels[i].move(0);
      }
      return;
    }
    if (direction == 'A') {
      for (int i = 0; i < leftWheelNumber; i++) {
        leftWheels[i].move(0);
      }
      for (int i = 0; i < leftWheelNumber; i++) {
        rightWheels[i].move(1);
      }
      return;
    }
    if (direction == 'D') {
      for (int i = 0; i < leftWheelNumber; i++) {
        leftWheels[i].move(1);
      }
      for (int i = 0; i < leftWheelNumber; i++) {
        rightWheels[i].move(0);
      }
      return;
    }
  }

  Pair<int, int> senseDistance() {
    // Serial.println("scanning...");
    digitalWrite(trigPin1, LOW);  // Clears the trigPin1
    delayMicroseconds(2);

    digitalWrite(trigPin1, HIGH);  // Sets the trigPin1 on HIGH state for 10 microseconds
    delayMicroseconds(10);
    digitalWrite(trigPin1, LOW);

    duration1 = pulseIn(echoPin1, HIGH);  // Reads the echoPin1, returns the sound wave travel time in microseconds

    distance1 = duration1 * 0.034 / 2;  // Calculating the distance for the first sensor

    Serial.print("Distance 1: ");  // Prints the distance from the first sensor on the Serial Monitor
    Serial.println(distance1);


    //delay to avoid interference
    delayMicroseconds(100);
    //

    // ------- Readings from the second sensor ----------
    digitalWrite(trigPin2, LOW);  // Clears the trigPin2
    delayMicroseconds(2);

    digitalWrite(trigPin2, HIGH);  // Sets the trigPin2 on HIGH state for 10 microseconds
    delayMicroseconds(10);
    digitalWrite(trigPin2, LOW);

    duration2 = pulseIn(echoPin2, HIGH);  // Reads the echoPin2, returns the sound wave travel time in microseconds

    distance2 = duration2 * 0.034 / 2;  // Calculating the distance for the second sensor

    Serial.print("Distance 2: ");  // Prints the distance from the second sensor on the Serial Monitor
    Serial.println(distance2);



    delay(100);  // Delay between readings
    return Pair<int, int>(distance1, distance2);
  }

  void run() {
    Pair<int, int> distances = senseDistance();
    if(distances.second < 10) {
      Serial.println("rotating right...");
      move(100, 'D');
      return;
    }
    if(distances.first < 10) {
      Serial.println("rotating left...");
      move(100, 'A');
      return;
    }
    Serial.println("going forward...");
    move(100, 'F');
  }
};

Pair<uint8_t, uint8_t> left[] = { Pair<uint8_t, uint8_t>(AIN1, AIN2) };
Pair<uint8_t, uint8_t> right[] = { Pair<uint8_t, uint8_t>(BIN1, BIN2) };

Robot cleanMars;

void setup() {
  // put your setup code here, to run once:
  // int leftWheelNumber = sizeof(left) / sizeof(left[0]);
  // rightWheelNumber = sizeof(rightW) / sizeof(rightW[0]);
  Serial.begin(9600);
  Serial.println("ON UART");
  cleanMars = Robot(left, right);
  // Serial.println(leftWheelNumber);
  pinMode(PWMB, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(STBY, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(2, INPUT_PULLUP);


  // sensor setup
  pinMode(trigPin1, OUTPUT);  // Sets the trigPin1 as an Output
  pinMode(echoPin1, INPUT);   // Sets the echoPin1 as an Input

  pinMode(trigPin2, OUTPUT);  // Sets the trigPin2 as an Output
  pinMode(echoPin2, INPUT);   // Sets the echoPin2 as an Input

  // digitalWrite(STBY, 0);
  while (digitalRead(2) != LOW);

  digitalWrite(STBY, 1);
  // delay(2000);
  Serial.println("start move");
  // cleanMars.move(255, 'F');
  // delay(2500);
  // cleanMars.stop();
}

void loop() {
  // cleanMars.senseDistance();
  cleanMars.run();
  // cleanMars.print();
  // String dir = "G";
  // cleanMars.move(255, 'F');
  // Serial.println("hello");
  // digitalWrite(AIN1, 0);
  // analogWrite(PWMA, 50);
  // digitalWrite(AIN2, 1);
  // // digitalWrite()
  // analogWrite(PWMA, 50);
  // put your main code here, to run repeatedly:
  // line(false);
}
