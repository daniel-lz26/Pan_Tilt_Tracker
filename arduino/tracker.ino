#include <Servo.h>
#include <Arduino_LED_Matrix.h>

Servo pan;
Servo tilt;
ArduinoLEDMatrix matrix;

int panAngle = 90;
int tiltAngle = 90;

byte frame[8][12];

void clearFrame() {
  for (int r = 0; r < 8; r++)
    for (int c = 0; c < 12; c++)
      frame[r][c] = 0;
}

// Display a two-digit number (0–99) on the 8x12 LED matrix.
// Each digit occupies a 3-wide column block separated by a gap.
void showNumber(int n) {
  clearFrame();
  n = constrain(n, 0, 99);

  int tens = n / 10;
  int ones = n % 10;

  // Draw one digit (0–9) starting at column offset `col`.
  // Uses a compact 3x5 pixel font (rows 1–5, cols col..col+2).
  auto drawDigit = [&](int d, int col) {
    switch (d) {
      case 0:
        frame[1][col]=1; frame[1][col+1]=1; frame[1][col+2]=1;
        frame[2][col]=1;                    frame[2][col+2]=1;
        frame[3][col]=1;                    frame[3][col+2]=1;
        frame[4][col]=1;                    frame[4][col+2]=1;
        frame[5][col]=1; frame[5][col+1]=1; frame[5][col+2]=1;
        break;
      case 1:
                         frame[1][col+1]=1;
                         frame[2][col+1]=1;
                         frame[3][col+1]=1;
                         frame[4][col+1]=1;
                         frame[5][col+1]=1;
        break;
      case 2:
        frame[1][col]=1; frame[1][col+1]=1; frame[1][col+2]=1;
                                            frame[2][col+2]=1;
        frame[3][col]=1; frame[3][col+1]=1; frame[3][col+2]=1;
        frame[4][col]=1;
        frame[5][col]=1; frame[5][col+1]=1; frame[5][col+2]=1;
        break;
      case 3:
        frame[1][col]=1; frame[1][col+1]=1; frame[1][col+2]=1;
                                            frame[2][col+2]=1;
        frame[3][col]=1; frame[3][col+1]=1; frame[3][col+2]=1;
                                            frame[4][col+2]=1;
        frame[5][col]=1; frame[5][col+1]=1; frame[5][col+2]=1;
        break;
      case 4:
        frame[1][col]=1;                    frame[1][col+2]=1;
        frame[2][col]=1;                    frame[2][col+2]=1;
        frame[3][col]=1; frame[3][col+1]=1; frame[3][col+2]=1;
                                            frame[4][col+2]=1;
                                            frame[5][col+2]=1;
        break;
      case 5:
        frame[1][col]=1; frame[1][col+1]=1; frame[1][col+2]=1;
        frame[2][col]=1;
        frame[3][col]=1; frame[3][col+1]=1; frame[3][col+2]=1;
                                            frame[4][col+2]=1;
        frame[5][col]=1; frame[5][col+1]=1; frame[5][col+2]=1;
        break;
      case 6:
        frame[1][col]=1; frame[1][col+1]=1; frame[1][col+2]=1;
        frame[2][col]=1;
        frame[3][col]=1; frame[3][col+1]=1; frame[3][col+2]=1;
        frame[4][col]=1;                    frame[4][col+2]=1;
        frame[5][col]=1; frame[5][col+1]=1; frame[5][col+2]=1;
        break;
      case 7:
        frame[1][col]=1; frame[1][col+1]=1; frame[1][col+2]=1;
                                            frame[2][col+2]=1;
                                            frame[3][col+2]=1;
                                            frame[4][col+2]=1;
                                            frame[5][col+2]=1;
        break;
      case 8:
        frame[1][col]=1; frame[1][col+1]=1; frame[1][col+2]=1;
        frame[2][col]=1;                    frame[2][col+2]=1;
        frame[3][col]=1; frame[3][col+1]=1; frame[3][col+2]=1;
        frame[4][col]=1;                    frame[4][col+2]=1;
        frame[5][col]=1; frame[5][col+1]=1; frame[5][col+2]=1;
        break;
      case 9:
        frame[1][col]=1; frame[1][col+1]=1; frame[1][col+2]=1;
        frame[2][col]=1;                    frame[2][col+2]=1;
        frame[3][col]=1; frame[3][col+1]=1; frame[3][col+2]=1;
                                            frame[4][col+2]=1;
        frame[5][col]=1; frame[5][col+1]=1; frame[5][col+2]=1;
        break;
    }
  };

  drawDigit(tens, 0);   // columns 0–2
  drawDigit(ones, 4);   // columns 4–6  (gap at column 3)

  matrix.renderBitmap(frame, 8, 12);
}

void setup() {
  Serial.begin(9600);
  pan.attach(9);
  tilt.attach(10);
  pan.write(panAngle);
  tilt.write(tiltAngle);
  matrix.begin();
  showNumber(panAngle);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // Expected format: "P<pan>,T<tilt>"  e.g. "P87,T93"
    int commaIdx = cmd.indexOf(',');
    if (cmd.length() > 2 && cmd.charAt(0) == 'P' && commaIdx > 1) {
      int p = cmd.substring(1, commaIdx).toInt();
      int tIdx = cmd.indexOf('T', commaIdx);
      if (tIdx != -1) {
        int t = cmd.substring(tIdx + 1).toInt();

        panAngle  = constrain(p, 0, 180);
        tiltAngle = constrain(t, 0, 180);

        pan.write(panAngle);
        tilt.write(tiltAngle);

        // Show pan angle on LED matrix (0–99 range displayed)
        showNumber(min(panAngle, 99));

        Serial.print("P:");
        Serial.print(panAngle);
        Serial.print(" T:");
        Serial.println(tiltAngle);
      }
    }
  }
}
