#include <Wire.h>
#include <SPI.h>
#include <SoftwareSerial.h> 
#include <ArduinoJson.h>
#include <math.h>
#include <Adafruit_ADXL375.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"

//Antena Lora
//Cambien estos valores a conveniencia 
String lora_band = "915000000"; //Banda de frecuencia (Hz) Se supone que penetra mejor entre menor sea la frecuencia. Chequen la hoja de datos y la de comandos
String lora_networkid = "18";   //Identificación de la red Lora
String lora_address = "1";      //Dirección del módulo
String lora_RX_address = "2";   //Dirección del módulo receptor
String lora_SF = "11" ;
String lora_BW = "9" ;
String TextoSalida ;
String Longitud;

//IMU
Adafruit_ADXL375 accel = Adafruit_ADXL375(12345);
const int numSamples = 1000;
const int samplingInterval = 10; 
const float g= 9.80665; 
float offsetX = 0.0;
float offsetY = 0.0;
float offsetZ = 0.0;
float vx = 0; //ajusten el (1/1000) como vean conveniente porque pues el tiempo varia dependiendo de que otras operaciones pongan
float vy = 0;
float vz = 0; 
//Barometro
#define BMP_SCK 18 //
#define BMP_MISO 19 //SDO
#define BMP_MOSI 23 //SDI
#define BMP_CS 5
#define SEALEVELPRESSURE_HPA (1013.25)
Adafruit_BMP3XX bmp;

//GPS
#define swsTX 4 // Transmit FROM GPS
#define swsRX 2 // Receive TO GPS
#define GPSBaud 9600 
SoftwareSerial GPSserial(swsRX, swsTX);
String gps;

void setup() {
  
  Serial.begin(115200);
  while (!Serial);
  GPSserial.begin(9600);
  Serial2.begin(115200,SERIAL_8N1,16,17);
  if (!accel.begin()) {
    Serial.println("El sensor ADXL375 no se ha inicializado correctamente. Checa la conexion");
    calibrate();
    while (1);
  }

  if (! bmp.begin_SPI(BMP_CS, BMP_SCK, BMP_MISO, BMP_MOSI)) { 
  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);
                                                              }
  Serial2.println("AT+BAND=" + lora_band);
  delay(1500);
  Serial2.println("AT+NETWORKID=" + lora_networkid);
  delay(1500);
  Serial2.println("AT+PARAMETER="+ lora_SF + "," + lora_BW + ",2,24");
  delay(1500);
  //Serial2.println("AT+RESET");  delay(1500);
  Serial2.println("AT+ADDRESS=" + lora_address);  delay(1500);
 


}

void loop() {
  //IMU
  vx += (accel.getX() - offsetX) / 1000.0 * g; //ajusten el (1/1000) como vean conveniente porque pues el tiempo varia dependiendo de que otras operaciones pongan
  vy += (accel.getY() - offsetY) / 1000.0 * g;
  vz += (accel.getZ() - offsetZ) / 1000.0 * g; 
  float vt = sqrt( pow(vx,2)+ pow(vy,2)+ pow(vz,2));

  //Barometro
  float Altitud = bmp.readAltitude(SEALEVELPRESSURE_HPA);
  float Temperatura = bmp.temperature;

  //GPS
  if (GPSserial.available()){
    gps=GPSserial.read();
  }
  //Envio de datos
  char buffer[100];
  sprintf(buffer, "%.4f,%.4f,%.4f,%s", vt, Altitud, Temperatura, gps.c_str());
  String TextoSalida= String(buffer);
  sendLoraData(TextoSalida, lora_RX_address);
  //Serial2.println("AT+SEND=" + lora_RX_address + "," + String(TextoSalida.length()) + "," + TextoSalida);
  delay(6000); 

}



void sendLoraData(String data, String address) {
  String myString = "AT+SEND=" + address + "," + String(data.length()) + "," + data + "\r\n";
  char* buf = (char*) malloc(sizeof(char) * myString.length() + 1);
  Serial.println(myString);
  myString.toCharArray(buf, myString.length() + 1);
  Serial2.write(buf);
  free(buf);
}




void calibrate() {
  float sumX = 0.0, sumY = 0.0, sumZ = 0.0;

  // Tomar muestras para la calibración
  for (int i = 0; i < numSamples; i++) {
    float x = accel.getX();
    float y = accel.getY();
    float z = accel.getZ();

    sumX += x;
    sumY += y;
    sumZ += z;

    delay(samplingInterval);
  }

  offsetX = sumX / numSamples;
  offsetY = sumY / numSamples;
  offsetZ = sumZ / numSamples;
}