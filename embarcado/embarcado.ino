#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#define DHTTYPE      DHT22
#define DHTPIN 3

DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;

void setup() {
  Serial.begin(9600);
  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  dht.humidity().getSensor(&sensor);
  delayMS = sensor.min_delay / 1000;

  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
}

void loop() {
  delay(delayMS);
  sensors_event_t event;

  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)){
    Serial.println("ERRO Erro na leitura da Temperatura!");
  } else {
    Serial.print("TEMP ");
    Serial.println(event.temperature);
  }

  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)){
    Serial.println("ERRO Erro na leitura da Umidade!");
  }
  else {
    Serial.print("UMID ");
    Serial.println(event.relative_humidity);
  }

  Serial.print("META ");
  Serial.println(analogRead(A0));

  Serial.print("MONO ");
  Serial.println(analogRead(A1));

  Serial.print("HIDR ");
  Serial.println(analogRead(A2));
}
