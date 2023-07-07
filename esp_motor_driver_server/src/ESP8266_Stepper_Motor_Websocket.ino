/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/stepper-motor-esp8266-websocket/

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESPAsyncWebServer.h>
#include "LittleFS.h"
#include <AccelStepper.h>

#define IN1 D0
#define IN2 D5
#define IN3 D6
#define IN4 D7

// #define IN1 D1
// #define IN2 D2
// #define IN3 D3
// #define IN4 D4

AccelStepper stepper(AccelStepper::HALF4WIRE, IN1, IN3, IN2, IN4);

String message = "";

// Replace with your network credentials
const char *ssid = "Ik heb geen wifi";
const char *password = "ikhebG1idee";

// 184, 185, 186
IPAddress local_IP(192, 168, 178, 186);
IPAddress gateway(192, 168, 178, 1);

IPAddress subnet(255, 255, 255, 0);

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// Create a WebSocket object
AsyncWebSocket ws("/ws");

// Variables to save values from HTML form
String value;
String cmd;
int speed = 10;

bool notifyStop = false;

// Initialize LittleFS
void initFS()
{
  if (!LittleFS.begin())
  {
    Serial.println("An error has occurred while mounting LittleFS");
  }
  else
  {
    Serial.println("LittleFS mounted successfully");
  }
}

// Initialize WiFi
void initWiFi()
{
  if (!WiFi.config(local_IP, gateway, subnet))
  {
    Serial.println("STA Failed to configure");
  }
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

void notifyClients(String state)
{
  ws.textAll(state);
}

void handleWebSocketMessage(void *arg, uint8_t *data, size_t len)
{
  AwsFrameInfo *info = (AwsFrameInfo *)arg;
  if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT)
  {
    data[len] = 0;
    message = (char *)data;
    cmd = message.substring(0, message.indexOf("&"));
    value = message.substring(message.indexOf("&") + 1, message.length());
    Serial.print("cmd: ");
    Serial.print(cmd);
    Serial.print(" | value: ");
    Serial.println(value);
    notifyClients(message);
    notifyStop = true;
    if (cmd == "STEP")
    {
      stepper.move(value.toInt());
    }
    else if (cmd == "CON")
    {
      speed = value.toInt();
      stepper.setSpeed(speed);
    }
    else if (cmd == "STOP")
    {
      stepper.stop();
      speed = 0;
      stepper.setSpeed(0);
    }
    else if (cmd == "ACCEL")
    {
      stepper.setAcceleration(value.toInt());
    }
    else if (cmd == "MAX_SPEED")
    {
      stepper.setMaxSpeed(value.toInt());
    }
  }
}

void onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len)
{
  switch (type)
  {
  case WS_EVT_CONNECT:
    Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
    break;
  case WS_EVT_DISCONNECT:
    Serial.printf("WebSocket client #%u disconnected\n", client->id());
    break;
  case WS_EVT_DATA:
    handleWebSocketMessage(arg, data, len);
    break;
  case WS_EVT_PONG:
  case WS_EVT_ERROR:
    break;
  }
}

void initWebSocket()
{
  ws.onEvent(onEvent);
  server.addHandler(&ws);
}

void setup()
{
  // Serial port for debugging purposes

  Serial.begin(115200);
  initWiFi();
  initWebSocket();
  initFS();
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);

  // Web Server Root URL
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request)
            { request->send(LittleFS, "/index.html", "text/html"); });

  server.serveStatic("/", LittleFS, "/");

  server.begin();
}

void loop()
{
  ws.cleanupClients();
  if (stepper.speed() == 0)
  {
    stepper.run();
  }
  else
  {
    stepper.runSpeed();
  }
}
