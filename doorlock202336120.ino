#include <cvzone.h> // Library to connect OpenCV with Arduino
#include <Servo.h> // Library to control the servo motor
SerialData serialData(1, 1); // Initialize cvzone serial communication for data transmission
Servo myservo; // Create a servo motor object
int trig = 11; // Trigger pin for the ultrasonic sensor
int echo = 12; // Echo pin for the ultrasonic sensor
int ledPin = 10; // LED pin number
int ServoPin = 13; // Servo motor pin number
int distance = 100; // Initial distance value measured by the ultrasonic sensor
int valsRec[1]; // Array to store data received from cvzone

void setup() {
    serialData.begin(); // Initialize serial communication with cvzone
    pinMode(trig, OUTPUT); // Set the trigger pin as output
    pinMode(echo, INPUT); // Set the echo pin as input
    pinMode(ledPin, OUTPUT); // Set the LED pin as output
    myservo.attach(ServoPin); // Attach the servo motor to the specified pin
}

void loop() {
    serialData.Get(valsRec); // Receive data from cvzone (e.g., face recognition value)

    // Condition: Face recognition success (valsRec[0] == 1) or detected distance <= 20cm
    if (valsRec[0] == 1 || distance <= 20) {
        digitalWrite(ledPin, 1); // Turn on the LED (indicates door is open)
        myservo.write(90); // Rotate the servo motor to 90 degrees (open the door)
        delay(3000); // Wait for 3 seconds
    } else {
        digitalWrite(ledPin, 0); // Turn off the LED (indicates door is closed)
        myservo.write(0); // Rotate the servo motor to 0 degrees (close the door)
    }
}
