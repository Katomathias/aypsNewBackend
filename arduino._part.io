[11:51 am, 13/06/2024] Bwire Olaka Software: #include <SoftwareSerial.h>
#include <Wire.h>

#define DE 5
#define RE 4

byte n, p, k;

const byte nitro[] = { 0x01, 0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c };
const byte phos[] = { 0x01, 0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc };
const byte pota[] = { 0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0 };

byte values[11];
SoftwareSerial mod(3, 6);
const int moisturePin = A0;
const int relayPin = 8;
byte nitrogen() {

  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);

  delay(150);

  if (mod.write(nitro, sizeof(nitro)) == 8) {
    digitalWrite(DE, LOW);
    digitalWrite(RE, LOW);
    for (byte i = 0; i < 7; i++) {
      values[i] = mod.read();
    }
  }

  return values[4];
}

byte phosphorous() {

  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);

  delay(150);

  if (mod.write(phos, sizeof(phos)) == 8) {
    digitalWrite(DE, LOW);
    digitalWrite(RE, LOW);
    for (byte i = 0; i < 7; i++) {
      values[i] = mod.read();
    }
  }

  return values[4];
}

byte potassium() {

  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);

  delay(150);

  if (mod.write(pota, sizeof(pota)) == 8) {

    digitalWrite(DE, LOW);
    digitalWrite(RE, LOW);

    for (byte i = 0; i < 7; i++) {
      values[i] = mod.read();
    }
   // Serial.println();
  }

  return values[4];
}

void showResult() {
byte nLast,pLast,kLast;
  if (!((n == 0 && p == 0 && k == 0) || (n > 0 && p > 0 && k > 0) || (n < 255 && p < 255 && k < 255))) {
    nLast = n;
    pLast = p;
    kLast = k;
    
    if ((n == 255 && p == 255 && k == 255)){
      n = nLast;
      p = pLast;
      k = kLast;
      return;
    }
    
  }

  
  Serial.println(n);
  Serial.println(p);
  Serial.println(k);
  delay(1000);
}
void moistureReading(){

  String irrigation;
  int moistureRead = analogRead(moisturePin);
  int moisture = map(moistureRead, 0, 1023, 0, 100);
  Serial.println(moisture);
  delay(1000);
  if(moisture < 45){
    irrigation = "on";
    digitalWrite(relayPin,HIGH);
    Serial.println(irrigation);
  }
  else{
    irrigation = "off";
    digitalWrite(relayPin,LOW);
    Serial.println(irrigation);
  }
}

void setup() {

  Serial.begin(9600);

  mod.begin(4800);
  pinMode(relayPin, OUTPUT);
  pinMode(RE, OUTPUT);
  pinMode(DE, OUTPUT);

  n = nitrogen();
  delay(1050);
  p = phosphorous();
  delay(1050);
  k = potassium();
  delay(1050);
}
unsigned long currentTime;
unsigned long previousCheckTime = 0;

const unsigned long sensorReadInterval = 1350UL;

void loop() {

  currentTime = millis();

  if (currentTime - previousCheckTime >= sensorReadInterval) {

    delay(1350);
    n = nitrogen();
    delay(1350);
    p = phosphorous();
    delay(1350);
    k = potassium();

    showResult();
    moistureReading();
    previousCheckTime = currentTime;
  }
}
[11:51 am, 13/06/2024] Bwire Olaka Software: #include <WiFi.h>

// Define the WiFi network credentials
const char* WIFI_SSID = "INSERT_YOUR_SSID_HERE";
const char* WIFI_PASSWORD = "INSERT_YOUR_WIFI_PASSWORD_HERE";

void setup() {
  // Initialize the Serial port for debugging
  Serial.begin(115200);
 
  // Initialize the ESP32 WiFi module
  WiFi.mode(WIFI_STA);

  // Connect to the WiFi network
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  Serial.println("...");

  // Wait for the WiFi connection to be established
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  // Print the IP address assigned to the Raspberry Pi by the WiFi network
  Serial.println("");
  Serial.println("WiFi connection established.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // do nothing
}
