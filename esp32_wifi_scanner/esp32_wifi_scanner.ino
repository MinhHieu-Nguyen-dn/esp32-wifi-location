#include "WiFi.h"

// Number of times to scan
const int scanTimes = 10;

void setup() {
  Serial.begin(9600);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  for (int i = 0; i < scanTimes; ++i) {
    Serial.println("Start Scan");
    int networkCount = WiFi.scanNetworks();
    Serial.print("Number of Networks Found: ");
    Serial.println(networkCount);
    for (int j = 0; j < networkCount; ++j) {
      int rssi = (int(WiFi.RSSI(j)) + 100) * 2;
      // Get BSSID as an array of bytes
      uint8_t* bssid = WiFi.BSSID(j);
      // Convert BSSID to a string of hexadecimal numbers
      char bssidStr[18];
      sprintf(bssidStr, "%02X:%02X:%02X:%02X:%02X:%02X", bssid[0], bssid[1], bssid[2], bssid[3], bssid[4], bssid[5]);
      // Print SSID, BSSID, and RSSI to Serial Monitor
      char buffer[60];
      sprintf(buffer, "%s %s: %d", WiFi.SSID(j).c_str(), bssidStr, rssi);
      Serial.println(buffer);
    }
    Serial.println("---");
    delay(15000);
  }
}

void loop() {
  // Nothing to do here
}
