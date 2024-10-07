#================================
#
# IOT - Dispositivo de Votacion
#
# DEV: Maximiliano Mansilla 
# Año: 2024
#
#==============================

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <base64.h>  // Para codificar en Base64

const char* ssid = "SSIDWifi";     // Reemplazar con el nombre de tu red WiFi
const char* password = "ClaveWIFI"; // Reemplazar con la contraseña de tu WiFi
const char* endpoint = "http://localhost:5006/api/votos/add" // Endpoint para votacion

// Pines a los que están conectados los botones
const int button1Pin = D1;
const int button2Pin = D2;
const int button3Pin = D3;

// Credenciales para autenticación básica
const char* user = "app";
const char* pass = "Energia2025";

void setup() {
  Serial.begin(115200);
  
  // Inicializar los pines de los botones
  pinMode(button1Pin, INPUT_PULLUP);
  pinMode(button2Pin, INPUT_PULLUP);
  pinMode(button3Pin, INPUT_PULLUP);

  // Conectar a la red WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a WiFi");
}

void loop() {
  // Chequear si algún botón fue presionado
  if (digitalRead(button1Pin) == LOW) {
    sendVote(1);  // Enviar voto con valor 1
    delay(500);   // Pequeño retraso para evitar múltiples envíos
  }
  if (digitalRead(button2Pin) == LOW) {
    sendVote(2);  // Enviar voto con valor 2
    delay(500);
  }
  if (digitalRead(button3Pin) == LOW) {
    sendVote(3);  // Enviar voto con valor 3
    delay(500);
  }
}

// Función para enviar el voto al endpoint
void sendVote(int voteValue) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(String(endpoint));  // URL del endpoint

    // Codificar las credenciales en Base64
    String credentials = String(user) + ":" + String(pass);
    String encodedAuth = base64::encode(credentials);
    
    // Configurar los headers y autenticación básica
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Basic " + encodedAuth);

    // Crear el cuerpo de la solicitud en formato JSON
    String postData = "{\"idLista\": " + String(voteValue) + "}";

    // Realizar la solicitud POST
    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();  // Leer la respuesta del servidor
      Serial.println("Respuesta del servidor: " + response);
    } else {
      Serial.println("Error en la solicitud POST");
    }
    http.end();  // Terminar la conexión
  } else {
    Serial.println("WiFi desconectado");
  }
}
