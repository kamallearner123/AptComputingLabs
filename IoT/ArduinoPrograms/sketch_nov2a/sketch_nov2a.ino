#include <MD_MAX72XX.h>
#include <SPI.h>

// Define the number of devices (4 matrices)
#define MAX_DEVICES 4

// Define the data, clock, and CS pins
#define DATA_PIN   4
#define CLK_PIN    5
#define LOAD_PIN   6

// Create an instance of the MD_MAX72XX library
MD_MAX72XX mx = MD_MAX72XX(DATA_PIN, CLK_PIN, LOAD_PIN, MAX_DEVICES);

const String message = "Happy Diwali";  // Message to scroll
int msgLength;  // Length of the message

void setup() {
  // Initialize the LED matrix
  mx.begin();
  msgLength = message.length();
}

void loop() {
  // Scroll the message across the LED matrix
  for (int i = 0; i < msgLength * 6; i++) {
    mx.clear();
    // Print each character of the message
    for (int j = 0; j < MAX_DEVICES; j++) {
      int charIndex = (i - j * 6) / 6;
      if (charIndex >= 0 && charIndex < msgLength) {
        mx.setChar(j * 2, message[charIndex]);  // Print the character
      }
    }
    mx.update();
    delay(100);  // Delay between frames to control scrolling speed
  }
}
