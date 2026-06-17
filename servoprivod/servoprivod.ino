#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_MIN 150
#define SERVO_MAX 600

int servo1 = 8;
int servo2 = 15;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);

  pwm.begin();
  pwm.setPWMFreq(50);

  delay(10);

  setServoAngle(servo1, 0);
  setServoAngle(servo2, 0);

  Serial.println("READY");
}

void loop() {

  if (Serial.available() > 0) {

    int cmd = Serial.parseInt();

    Serial.print("Получено: ");
    Serial.println(cmd);

    if (cmd == 1) {
      setServoAngle(servo1, 90);
      delay(500);
      setServoAngle(servo1, 0);

      Serial.println("DONE 1");
    }

    else if (cmd == 2) {
      setServoAngle(servo2, 90);
      delay(500);
      setServoAngle(servo2, 0);

      Serial.println("DONE 2");
    }

    else if (cmd == 3) {
      Serial.println("PASS 3");
    }

    else if (cmd == 4) {
      Serial.println("PASS 4");
    },

    else {
      Serial.println("UNKNOWN");
    }

    delay(100);
  }
}

void setServoAngle(int channel, int angle) {
  int pulse = map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
  pwm.setPWM(channel, 0, pulse);
}