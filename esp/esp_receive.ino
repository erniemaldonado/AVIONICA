#include <Wire.h>
#include <math.h>

String lora_band = "915000000"; // Banda de frecuencia (Hz)
String lora_networkid = "18";   // Identificación de la red LoRa
String lora_address = "2";      // Dirección del módulo
String lora_txpower = "22";     // Potencia de transmisión (dBm)
String lora_SF = "11" ;
String lora_BW = "9" ;
String textoEntrada;

void setup() {
  Serial2.begin(115200, SERIAL_8N1, 16, 17);
  delay(500);
  Serial.begin(115200);
  delay(500);

  Serial2.println("AT+BAND=" + lora_band);
  delay(1500);
  Serial2.println("AT+NETWORKID=" + lora_networkid);
  delay(1500);
  Serial2.println("AT+PARAMETER="+ lora_SF + "," + lora_BW + ",2,24");
  delay(1500);
  Serial2.println("AT+ADDRESS=" + lora_address);
  delay(1500);
 

}

void loop() {
  if(Serial2.available()){
    textoEntrada = Serial2.readString();
    Serial.println(textoEntrada);  
                      }
}