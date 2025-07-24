const int analogPin = A0;
float sensitivity = 0.1; // For ACS712-20A, use 0.066 for 30A, 0.185 for 5A
int offset = 512; // Midpoint for 5V

void setup() {
  Serial.begin(9600);
}

void loop() {
  long sum = 0;
  for (int i = 0; i < 1000; i++) {
    int val = analogRead(analogPin);
    sum += (val - offset) * (val - offset);
    delayMicroseconds(100);
  }

  float rms = sqrt(sum / 1000.0);
  float voltage = (rms * 5.0) / 1024.0;
  float current = voltage / sensitivity;

  Serial.print("Current (A): ");
  Serial.println(current);
  
  // Estimate Power (Apparent Power)
  float assumedVoltage = 230.0; // You can measure with a sensor for real values
  float power = assumedVoltage * current;

  Serial.print("Apparent Power (VA): ");
  Serial.println(power);

  delay(1000);
}

/*
⚠️ SAFETY WARNING
Never touch bare wires or terminals connected to AC mains.

Always use proper insulation.

Preferably use a clamp meter or a current transformer for AC appliances. Direct connection should only be attempted by experienced users.

🧰 Components Required:
Arduino Uno

ACS712 module (e.g., 20A version)

Burden resistor (if not built-in)

Relay module or plug board with separated wires (for inserting ACS712)

LCD or Serial monitor

Voltage sensor module (optional, for real power)

Jumper wires

🔌 Step 1: Wiring ACS712 to Arduino
📦 ACS712 Pinout:
Vcc → Arduino 5V

GND → Arduino GND

OUT → Arduino A0 (analog input)

🧪 Step 2: Connect ACS712 to Refrigerator Power Line
You need to connect one line (Live or Neutral) of the refrigerator’s AC power cord in series through the ACS712.

⚡ Safe Method:
Cut an extension cable or use a plug with split wires.

Connect only the Live wire through the ACS712 input terminals.

Leave Neutral and Earth wires as-is.

DO NOT connect both Live and Neutral wires through ACS712, or it will cancel the current sensing.

*/
