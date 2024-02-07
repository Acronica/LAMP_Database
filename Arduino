#include <DHT.h>

#define DHTPIN 8  // DHT11 센서의 데이터 핀
#define DHTTYPE DHT11  // DHT 센서 유형
#define AnalogPort A0

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  int analog_port = analogRead(A0);
  double ground_humi = 100 - (analog_port / 1023.0 * 100.0);
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // JSON 형식으로 데이터 전송
  Serial.print("{\"ground_humi\":");
  Serial.print(ground_humi);
  Serial.print(",\"humi\":");
  Serial.print(humidity);
  Serial.print(",\"temp\":");
  Serial.print(temperature);
  Serial.println("}");

  // 2초 대기
  delay(10000);
}
