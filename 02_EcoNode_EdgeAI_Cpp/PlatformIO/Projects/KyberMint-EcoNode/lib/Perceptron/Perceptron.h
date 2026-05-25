#ifndef PERCEPTRON_H
#define PERCEPTRON_H

class Perceptron {
  private:
    float weightTemp;
    float weightHum;
    float weightGas;
    float bias;

  public:
    // Construtor para inicializar os pesos da rede neural
    Perceptron(float wT, float wH, float wG, float b);
    
    // Função de inferência
    int infer(float temp, float hum, float gas);
};

#endif