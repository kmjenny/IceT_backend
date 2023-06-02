#include <DHT.h>
#define DHTPIN A1
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
}

void loop() {
  int h = dht.readHumidity();
  int t = dht.readTemperature();

  delay(3000);
  
  Serial.print("DATA,");
  Serial.print(h);
  Serial.print(",");
  Serial.println(t);
}
