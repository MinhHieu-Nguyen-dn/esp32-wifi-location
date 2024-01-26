#include "WiFi.h"
#include <HTTPClient.h>

const char* ssid = "your_WiFi_ssid";
const char* password = "your_WiFi_password";

const uint16_t port = 8090;
const char * host = "your_IPv4_Address";
 
void setup()
{
 
  Serial.begin(9600);
 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.println("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
 
}
 
void loop()
{
  WiFiClient client;

  if (!client.connect(host, port)) {

      Serial.println("Connection to host failed");
      delay(1000);
      return;
  }

  Serial.println("Connected to server successful!");

  Serial.println("Start Scan");
  int networkCount = WiFi.scanNetworks();
  Serial.print("Number of Networks Found: ");
  Serial.println(networkCount);

  String scan_result = "{";
  for (int j = 0; j < networkCount; ++j) {
    int rssi = (int(WiFi.RSSI(j)) + 100) * 2;
    uint8_t* bssid = WiFi.BSSID(j);
    char bssidStr[18];
    sprintf(bssidStr, "%02X:%02X:%02X:%02X:%02X:%02X", bssid[0], bssid[1], bssid[2], bssid[3], bssid[4], bssid[5]);
    char buffer[60];
    sprintf(buffer, "\"%s %s\": %d", WiFi.SSID(j).c_str(), bssidStr, rssi);
    scan_result += buffer;
    scan_result += ", ";
  }
  scan_result += "}";

  client.print(scan_result);
  Serial.println(scan_result);
  Serial.println("---");

  client.stop();
  delay(2000);
}