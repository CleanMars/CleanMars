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

template<typename T, typename U>
struct Pair {
    T first;
    U second;
    
    Pair() : first(), second() {}
    Pair(const T& a, const U& b) : first(a), second(b) {}
};


class Wheel {
  private: 
    uint8_t in1, in2;
  public: 
    Wheel(){}
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
      Serial.print("input1: ");
      Serial.println(in1);
      Serial.print("input2: ");
      Serial.println(in2);
      Serial.print("direction: ");
      Serial.println(direction);
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

  public: 
    Robot(){}
    Robot(Pair<uint8_t, uint8_t> *leftW, Pair<uint8_t, uint8_t> *rightW) {
      // Serial.println(leftW[0].first);
      leftWheelNumber = sizeof(leftW) / sizeof(leftW[0]);
      rightWheelNumber = sizeof(rightW) / sizeof(rightW[0]);

      // Serial.println(sizeof(leftW));
      // Serial.println(leftWheelNumber);
      // rightWheelNumber = rsize;
      leftWheels = new Wheel[leftWheelNumber];
      rightWheels = new Wheel[rightWheelNumber];
      // leftWheels = (Wheel*) malloc(leftWheelNumber * sizeof(Wheel));
      // rightWheels = (Wheel*) malloc(rightWheelNumber * sizeof(Wheel));

      for(int i = 0; i < leftWheelNumber; i++) {
        Serial.print(i);
        Serial.print(": ");
        Serial.print(leftW[i].first);
        Serial.print(", ");
        Serial.println(leftW[i].second);
        leftWheels[i] = Wheel(leftW[i].first, leftW[i].second);
      }
      for(int i = 0; i < rightWheelNumber; i++) {
        Serial.print(i);
        Serial.print(": ");
        Serial.print(rightW[i].first);
        Serial.print(", ");
        Serial.println(rightW[i].second);
        rightWheels[i] = Wheel(rightW[i].first, rightW[i].second);
      }

      Serial.println("done setting up");
    }

    void print() {
      Serial.println(leftWheelNumber);
      Serial.println(rightWheelNumber);
      Serial.println("printing...");
    }

    void move(uint8_t power, char direction) {
      analogWrite(PWMA, power);
      analogWrite(PWMB, power);
      if(direction == 'F') {
        // Serial.println(direction);
        for(int i = 0; i < leftWheelNumber; i++) {
            leftWheels[i].move(1);
        }
        for(int i = 0; i < rightWheelNumber; i++) {
            rightWheels[i].move(1);
        }
        return;
      }
      if(direction == 'R') {
        for(int i = 0; i < leftWheelNumber; i++) {
            leftWheels[i].stop();
        }
        for(int i = 0; i < leftWheelNumber; i++) {
            rightWheels[i].move(1);
        }
        return;
      }

      if(direction == 'L') {
        for(int i = 0; i < leftWheelNumber; i++) {
            leftWheels[i].move(1);
        }
        for(int i = 0; i < leftWheelNumber; i++) {
            rightWheels[i].stop();
        }
        return;
      }
      if(direction == 'B') {
        for(int i = 0; i < leftWheelNumber; i++) {
            leftWheels[i].move(0);
        }
        for(int i = 0; i < leftWheelNumber; i++) {
            rightWheels[i].move(0);
        }
        return;
      }
      if(direction == 'A') {
        for(int i = 0; i < leftWheelNumber; i++) {
            leftWheels[i].move(0);
        }
        for(int i = 0; i < leftWheelNumber; i++) {
            rightWheels[i].move(1);
        }
        return;
      }
       if(direction == 'D') {
        for(int i = 0; i < leftWheelNumber; i++) {
            leftWheels[i].move(1);
        }
        for(int i = 0; i < leftWheelNumber; i++) {
            rightWheels[i].move(0);
        }
        return;
      }
    }
};

Pair<uint8_t, uint8_t> left[] = {Pair<uint8_t, uint8_t>(AIN1, AIN2)};
Pair<uint8_t, uint8_t> right[] = {Pair<uint8_t, uint8_t>(BIN1, BIN2)};

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
  digitalWrite(STBY, 1);
}

void loop() {
  // cleanMars.print();
  // String dir = "G";
  cleanMars.move(50, 'F');
  // Serial.println("hello");
  // digitalWrite(AIN1, 0);
  // analogWrite(PWMA, 50);
  // digitalWrite(AIN2, 1);
  // // digitalWrite()
  // analogWrite(PWMA, 50);
  // put your main code here, to run repeatedly:
  // line(false);
}
