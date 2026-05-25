#include <Arduino.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "Perceptron.h" // Importando nossa IA modular!

// --- Definições de Hardware ---
#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

#define RELAY_PIN 8
#define LED_PIN 13
#define GAS_PIN 26 // Pino analógico do MQ-135

// --- Display OLED ---
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// --- Instanciando a Inteligência Artificial ---
// Pesos: Temp(0.6), Umid(0.1), Gas(0.4), Bias(-40.0)
Perceptron ia_ecoNode(0.6, 0.1, 0.4, -40.0); 

void setup() {
    Serial.begin(115200);
    dht.begin();
    
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(LED_PIN, OUTPUT);
    analogReadResolution(12); // Resolução de 12 bits para o Pico (0 a 4095)

    // Configurando I2C para o OLED
    Wire.setSDA(4);
    Wire.setSCL(5);
    Wire.begin();
    
    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 10);
    display.println("KyberMint EcoNode");
    display.println("Inicializando...");
    display.display();
    delay(2000);
}

void loop() {
    // 1. Coleta (Sensores)
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    
    // Simulação do MQ-135 (Mapeando a leitura analógica para uma % de poluição 0-100)
    int gas_raw = analogRead(GAS_PIN);
    float gas_percent = map(gas_raw, 0, 4095, 0, 100);

    if (isnan(temp)) return;

    // 2. Inferência (IA)
    int decision = ia_ecoNode.infer(temp, hum, gas_percent);

    // 3. Interface e Atuadores
    display.clearDisplay();
    display.setTextSize(1);
    
    // Linha 1 (Y = 0)
    display.setCursor(0, 0);
    display.printf("Temp: %.1f C\n", temp);
    
    // Linha 2 (Y = 12)
    display.setCursor(0, 12);
    display.printf("Umid: %.1f %%\n", hum);
    
    // Linha 3 (Y = 24)
    display.setCursor(0, 24);
    display.printf("Gas : %.1f %%\n", gas_percent);
    
    // Status da IA (Y = 45)
    display.setCursor(0, 45);
    if (decision == 1) {
        display.setTextSize(2);
        display.println("CRITICO!");
        digitalWrite(RELAY_PIN, HIGH);
        digitalWrite(LED_PIN, HIGH);
    } else {
        display.setTextSize(2);
        display.println("NORMAL");
        digitalWrite(RELAY_PIN, LOW);
        digitalWrite(LED_PIN, LOW);
    }
    
    display.display();
    delay(1000); }// Aguarda antes de atualizar