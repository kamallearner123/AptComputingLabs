// Define the pins
const int SOUND_SENSOR_PIN = A0; // Analog input pin for sound sensor
const int LED_PIN = 13;           // Digital output pin for LED
int claps = 0;

// Define the sound threshold (adjust this value as needed)
const int SOUND_THRESHOLD = 50;  // Set threshold based on your requirements

void setup() {
  // Initialize serial communication for debugging
  Serial.begin(9600);
  Serial.println("Sound Detection with LED Program Initialized");

  // Set the LED pin as output
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // Read the analog value from the sound sensor
  int soundValue = analogRead(SOUND_SENSOR_PIN);

  // Check if the sound value exceeds the threshold
  if (soundValue > SOUND_THRESHOLD) {
    claps +=1;
    // Turn on the LED if the sound level is above the threshold
    digitalWrite(LED_PIN, HIGH);

    // Print the analog value to the Serial Monitor for debugging
    Serial.print("Sound Sensor Value: ");
    Serial.println(claps);
    delay(1000);

  } else {
    // Turn off the LED if the sound level is below the threshold
    digitalWrite(LED_PIN, LOW);
  }

  // Short delay for stability
  delay(10);  // Adjust delay as needed
}
