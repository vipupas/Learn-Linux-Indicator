#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "Vipin";
const char* password = "Vipin@123";

// Create BMP180 object
Adafruit_BMP085 bmp;

// Create web server on port 80
WebServer server(80);

void setup() {
  Serial.begin(115200);
  
  // Initialize BMP180
  if (!bmp.begin()) {
    Serial.println("Could not find BMP180 sensor!");
    while (1) {}
  }
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("WiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  // Define routes
  server.on("/", handleRoot);
  server.on("/data", handleData);
  server.enableCORS(true);
  
  // Start server
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}

void handleRoot() {
  String html = "<html><body>";
  html += "<h1>ESP32 BMP180 Sensor</h1>";
  html += "<p>Temperature: " + String(bmp.readTemperature()) + " °C</p>";
  html += "<p>Pressure: " + String(bmp.readPressure() / 100.0F) + " hPa</p>";
  html += "<p>Altitude: " + String(bmp.readAltitude()) + " m</p>";
  html += "<p><a href='/data'>JSON Data</a></p>";
  html += "</body></html>";
  
  server.send(200, "text/html", html);
}

void handleData() {
  // Create JSON response
  StaticJsonDocument<200> doc;
  
  float temperature = bmp.readTemperature();
  float pressure = bmp.readPressure() / 100.0F; // Convert Pa to hPa
  float altitude = bmp.readAltitude();
  
  doc["temperature"] = temperature;
  doc["pressure"] = pressure;
  doc["altitude"] = altitude;
  doc["timestamp"] = millis();
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  server.send(200, "application/json", jsonString);
}