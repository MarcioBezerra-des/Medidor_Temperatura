#include "Perceptron.h"

// Inicializando os pesos
Perceptron::Perceptron(float wT, float wH, float wG, float b) {
    weightTemp = wT;
    weightHum = wH;
    weightGas = wG;
    bias = b;
}

// O Motor de Decisão
int Perceptron::infer(float temp, float hum, float gas) {
    // Cálculo do Perceptron com 3 variáveis (Temp, Umidade e Qualidade do Ar)
    float sum = (temp * weightTemp) + (hum * weightHum) + (gas * weightGas) + bias;
    
    // Função de Ativação Step
    return (sum >= 0.0) ? 1 : 0;
}