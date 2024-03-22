#include <DHT.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>


#define DHTTYPE DHT11
#define DHTPIN D4

const char* ssid = "******";
const char* password = "*****";

String mqtt_user = "temp";
const char* topic = "smart_home/mqtt";
const char* mqtt_server = "192.168.1.9";
const int mqtt_port = 1883;
               
DHT dht(DHTPIN, DHTTYPE);                

float Temperature;
float Humidity;

WiFiClient espClient;
PubSubClient client(espClient);

void send_message(String to_user, String user_id, String cmd, String payload="_") {
  String message = mqtt_user + "|" + to_user + "|" + user_id + "|" + cmd + "|" + payload;
  Serial.println("I sent - " + message);
  client.publish(topic, message.c_str());
}

int MQTTcallback(char* topic, byte* payload, unsigned int length) 
{
  String a[5]; // from_username to_username user_id cmd payload
  int c = 0;
  String temp = "";
  for (int i = 0; i < length; i++) 
  {
    if (i == length - 1) {
      temp += (char)payload[i];
      a[c] = temp; 
    } else if ((char)payload[i] == '|') {
      a[c] = temp;
      temp = "";
      c++;
    } else {
      temp += (char)payload[i];
    }
  }
  if (a[0] == mqtt_user || (a[1] != mqtt_user && a[1] != "all")) {
    Serial.println("It is my message or it was sent not for me so I gonna skip it");
    return 1;
  }
  if (a[3] == "ping") {
    send_message("server", a[2], "pong");
  } else if (a[3] == "get_data") {
    float Temperature = dht.readTemperature();
    float Humidity = dht.readHumidity();
    String payload = "Temperature: " + String(Temperature, 3) + " °C\nHumidity: " + String(Humidity, 3);
    send_message("server", a[2], "send_data", payload);
  }
  return 1;
}

void setup() 
{
  Serial.begin(115200);
  delay(100);
  pinMode(DHTPIN, INPUT);
  dht.begin();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.print("Connected to WiFi :");
  Serial.println(WiFi.SSID());
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(MQTTcallback);
  while (!client.connected()) 
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266"))
    {
      Serial.println("connected");
    }
    else
    {
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }
  client.subscribe(topic);

}

void loop() 
{
  client.loop();
}
