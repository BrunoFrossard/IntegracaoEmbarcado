#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h> 
#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

Adafruit_BME280 bme; 

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  if (!bme.begin(0x76)) {
    Serial.println("{\"erro\": \"BME280 nao encontrado no 0x76\"}");
  }
}

void loop() {
  float t = bme.readTemperature();
  float p = bme.readPressure() / 100.0F;
  float h = bme.readHumidity();

  if (isnan(h) || h == 0) {
    h = dht.readHumidity();
  }

  Serial.print("{");
  Serial.print("\"temperatura\":"); Serial.print(t);
  Serial.print(",");
  Serial.print("\"umidade\":"); Serial.print(h);
  Serial.print(",");
  Serial.print("\"pressao\":"); Serial.print(p);
  Serial.println("}");

  delay(5000); 
}
