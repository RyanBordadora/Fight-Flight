const int button1Pin = 2;  // Pin for button 1
const int button2Pin = 3;  // Pin for button 2
const int button3Pin = 4;  // Pin for button 3

void setup() {
  Serial.begin(9600);
  pinMode(button1Pin, INPUT_PULLUP);
  pinMode(button2Pin, INPUT_PULLUP);
  pinMode(button3Pin, INPUT_PULLUP);
}

void loop() {
  // Read the states of the buttons
  int button1State = digitalRead(button1Pin);
  int button2State = digitalRead(button2Pin);
  int button3State = digitalRead(button3Pin);

  // Invert button states
  button1State = !button1State;
  button2State = !button2State;
  button3State = !button3State;

  // Send the inverted button states over serial
  Serial.print(button1State);
  Serial.print(",");
  Serial.print(button2State);
  Serial.print(",");
  Serial.println(button3State);

  delay(100);  // Add a small delay to avoid flooding the serial port
}
