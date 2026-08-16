/*
  Attendance Bridge Firmware
  Board: ESP32 DevKit
  Sensor: R307S (fingerprint)
  Display: 0.96" SSD1306 OLED (I2C)

  This is the firmware that runs DURING attendance taking.
  It talks to your Python script over USB serial (COM8):
    - When a finger is scanned and matched to a stored ID,
      it sends "FP:<id>" over serial (e.g. "FP:1")
    - It listens for "DISPLAY:line1|line2" commands from Python
      and shows them on the OLED

  Libraries needed (Arduino Library Manager):
    - Adafruit Fingerprint Sensor Library
    - Adafruit SSD1306
    - Adafruit GFX Library

  Wiring: same as before
    R307S  TX  -> ESP32 GPIO16 (RX2)
    R307S  RX  -> ESP32 GPIO17 (TX2)
    R307S  VCC -> ESP32 5V (VIN)
    R307S  GND -> GND

    OLED   SDA -> ESP32 GPIO21
    OLED   SCL -> ESP32 GPIO22
    OLED   VCC -> ESP32 3.3V
    OLED   GND -> GND

  IMPORTANT: fingerprints must already be registered on the sensor
  (using the separate registration sketch) before this will work -
  this firmware only reads/matches, it doesn't enroll new prints.
*/

#include <Adafruit_Fingerprint.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

HardwareSerial mySerial(2); // UART2 -> GPIO16 (RX), GPIO17 (TX)
Adafruit_Fingerprint finger(&mySerial);

String serialBuffer = "";

void showMessage(const String &line1, const String &line2 = "") {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 20);
  display.println(line1);
  if (line2.length() > 0) {
    display.setCursor(0, 35);
    display.println(line2);
  }
  display.display();
}

void setup() {
  Serial.begin(9600); // must match Python's serial.Serial('COM8', 9600, ...)
  delay(500);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    // Keep going even if OLED fails - fingerprint matching can still work
    Serial.println("OLED not found");
  } else {
    showMessage("Booting...");
  }

  mySerial.begin(57600, SERIAL_8N1, 16, 17);
  finger.begin(57600);

  if (finger.verifyPassword()) {
    showMessage("Smart Attendance", "Show your face");
  } else {
    showMessage("Sensor NOT found", "Check wiring");
    while (true) delay(10);
  }
}

void loop() {
  // 1. Listen for DISPLAY: commands coming from Python
  readSerialCommands();

  // 2. Continuously check for a fingerprint scan
  int id = getFingerprintID();
  if (id >= 0) {
    Serial.print("FP:");
    Serial.println(id);
  }

  delay(50);
}

void readSerialCommands() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      processCommand(serialBuffer);
      serialBuffer = "";
    } else {
      serialBuffer += c;
    }
  }
}

void processCommand(String cmd) {
  cmd.trim();
  if (cmd.startsWith("DISPLAY:")) {
    String payload = cmd.substring(8); // strip "DISPLAY:"
    int sep = payload.indexOf('|');
    if (sep >= 0) {
      String line1 = payload.substring(0, sep);
      String line2 = payload.substring(sep + 1);
      showMessage(line1, line2);
    } else {
      showMessage(payload);
    }
  }
}

int getFingerprintID() {
  int p = finger.getImage();
  if (p != FINGERPRINT_OK) return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK) return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK) return -1; // no match found

  return finger.fingerID; // matched ID
}