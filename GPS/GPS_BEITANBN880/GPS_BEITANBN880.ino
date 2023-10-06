
#include "TinyGPS++.h";
#include "HardwareSerial.h";

TinyGPSPlus gps;
HardwareSerial SerialGPS(1);
void loop() {
    while (SerialGPS.available() >0) {
       gps.encode(SerialGPS.read());
    }

    Serial.print("LAT,");  Serial.print(gps.location.lat(), 6); Serial.print(",");
    Serial.print("LONG,"); Serial.print(gps.location.lng(), 6); Serial.print(",");
    Serial.print("ALT,");  Serial.println(gps.altitude.meters());
    delay(500);
}

void setup() {
        Serial.begin(38400); //Serial port of USB
        SerialGPS.begin(9600, SERIAL_8N1, 16, 17); //Establish which pins to use (rx2,tx2)
       
}