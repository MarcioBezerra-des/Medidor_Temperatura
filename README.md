# 🌍 KyberMint Labs - Monitoramento Ambiental

Este repositório documenta a evolução do projeto de Monitoramento Ambiental, desenvolvido no âmbito do 5º semestre de Ciência da Computação (UNIC), aplicando conceitos de Sistemas Digitais, Banco de Dados, Microprocessadores e Inteligência Artificial.

## 📂 Arquitetura do Repositório (Monorepo)

O projeto foi construído em duas grandes fases tecnológicas, demonstrando a evolução de um modelo simulado para um nó computacional de borda real:

* 🐍 **[Versão 1: Protótipo Digital Twin (Python & Dash)](./01_Prototipo_Python)**
  * Dashboard de telemetria interativo construído com Python, Dash/Plotly e banco de dados persistente em SQLite3. Serviu como a camada inicial de visualização e simulação de dados.

* ⚙️ **[Versão 2: EcoNode Edge AI (C++ & ARM)](./02_EcoNode_EdgeAI_Cpp)**
  * Sistema embarcado de borda rodando nativamente na arquitetura ARM (Raspberry Pi Pico W). Integra leitura de sensores (Temperatura, Umidade, Qualidade do Ar) com tomada de decisão autônoma via Inteligência Artificial (**Perceptron**) desenvolvida em C/C++.

---