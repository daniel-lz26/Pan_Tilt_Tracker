#include <Servo.h>
#include <Arduino_LED_Matrix.h>

Servo servo1;
Servo servo2;
ArduinoLEDMatrix matrix;

// 8x12 LED matrix frames for 45, 90, 180
// Each number hand-drawn as pixel art for the 8x12 grid

byte frame[8][12];

void clearFrame() {
  for (int r = 0; r < 8; r++)
    for (int c = 0; c < 12; c++)
      frame[r][c] = 0;
}

void showNumber(int degrees) {
  clearFrame();

  if (degrees == 45) {
    // "45" on 8x12 grid
    // 4
    frame[1][0] = 1; frame[1][2] = 1;
    frame[2][0] = 1; frame[2][2] = 1;
    frame[3][0] = 1; frame[3][1] = 1; frame[3][2] = 1;
    frame[4][2] = 1;
    frame[5][2] = 1;
    // 5
    frame[1][4] = 1; frame[1][5] = 1;
    frame[2][4] = 1;
    frame[3][4] = 1; frame[3][5] = 1;
    frame[4][5] = 1;
    frame[5][4] = 1; frame[5][5] = 1;

  } else if (degrees == 90) {
    // "90" on 8x12 grid
    // 9
    frame[1][0] = 1; frame[1][1] = 1;
    frame[2][0] = 1; frame[2][2] = 1;
    frame[3][1] = 1; frame[3][2] = 1;
    frame[4][2] = 1;
    frame[5][1] = 1;
    // 0
    frame[1][4] = 1; frame[1][5] = 1;
    frame[2][4] = 1; frame[2][5] = 1;
    frame[3][4] = 1; frame[3][5] = 1;
    frame[4][4] = 1; frame[4][5] = 1;
    frame[5][4] = 1; frame[5][5] = 1;

  } else if (degrees == 180) {
    // "180" squeezed into 8x12
    // 1
    frame[1][0] = 1;
    frame[2][0] = 1;
    frame[3][0] = 1;
    frame[4][0] = 1;
    frame[5][0] = 1;
    // 8
    frame[1][2] = 1; frame[1][3] = 1;
    frame[2][2] = 1; frame[2][3] = 1;
    frame[3][2] = 1; frame[3][3] = 1;
    frame[4][2] = 1; frame[4][3] = 1;
    frame[5][2] = 1; frame[5][3] = 1;
    // 0
    frame[1][5] = 1; frame[1][6] = 1;
    frame[2][5] = 1; frame[2][6] = 1;
    frame[3][5] = 1; frame[3][6] = 1;
    frame[4][5] = 1; frame[4][6] = 1;
    frame[5][5] = 1; frame[5][6] = 1;
  }

  matrix.renderBitmap(frame, 8, 12);
}

int angles[] = {45, 90, 180};
int angleIndex = 0;

void setup() {
  servo1.attach(9);
  servo2.attach(10);
  matrix.begin();
  Serial.begin(9600);

  servo1.write(angles[0]);
  servo2.write(angles[0]);
  showNumber(angles[0]);
}

void loop() {
  angleIndex = (angleIndex + 1) % 3;
  int angle = angles[angleIndex];

  servo1.write(angle);
  servo2.write(angle);
  showNumber(angle);

  Serial.print("Angle: ");
  Serial.println(angle);

  delay(3000);
}