#include <Servo.h>

const int trigPin = 6;
const int echoPin = 4;
const int servoPin = 3;

Servo myServo;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  myServo.attach(servoPin);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2;

  Serial.println(distance);

  while (Serial.available() == 0) {
  }
  String command = Serial.readStringUntil('\n');
  command.trim();

  if (command == "SERVO_0") {
    myServo.write(0);
  } else if (command == "SERVO_90") {
    myServo.write(90);
  } else if (command == "SERVO_180") {
    myServo.write(180);
  }

  delay(200);
}