#include <Stepper.h>

// OBS: Max input is 32767, otherwise overflow error (?, correct wording?) because int(16) max value = 32767.

/*
 * Step motor driver 1  |   Arduino Uno
 *         IN1                  2
 *         IN2                  4
 *         IN3                  3               ~
 *         IN4                  5               ~
 *
 * Step motor driver 2  |   Arduino Uno
 *         IN1                  7
 *         IN2                  8
 *         IN3                  9              ~
 *         IN4                  10             ~
 *         
 * Power
 * Step motor driver 1:
 *  Power supply 1.
 * Step motor driver 2: 
 *  Power supply 2.
*/

#define STEPS 2048

Stepper StepX(STEPS, 2, 3, 4, 5);
Stepper StepY(STEPS, 7, 9, 8, 10);

char rx_byte = 0;
String rx_str = "";

void setup() {
  // put your setup code here, to run once:

  // Rotations per minute => (1 rotation / min) / (2048 steps * 10 rotations) = 0.0029296872 sec / step => ~3 ms / step
  StepX.setSpeed(10);
  StepY.setSpeed(10);

  Serial.begin(9600);
}

void move(int x, int y){

  StepX.step(x);
  StepY.step(y);

}

String split_string(String data, int point){
  // Splits the string the arduino gets from the computer into int, if point is 0 = x value, 1 = y value.

  char separator = ':';

  if (point == 0) {
    return data.substring(0, data.indexOf(separator));
  }
  else{
    return data.substring(data.indexOf(separator) + 1);
  }

}

void loop() {
  // put your main code here, to run repeatedly:

  if (Serial.available() > 0){

    char rx_byte = Serial.read();

    if (rx_byte != '\n'){
      rx_str += rx_byte;
    }
    else{

      int x = split_string(rx_str, 0).toInt();
      int y = split_string(rx_str, 1).toInt();

      rx_str = "";

      String returnText = "x: " + String(x) + " y: " + String(y);

      // Serial.println(returnText);

      move(x, y);
    }

  }

}
