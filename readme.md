# 🌡️ KyberMint Labs - Simulador de Temperatura 3D Pro

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Dash](https://img.shields.io/badge/Framework-Dash/Plotly-orange.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)

Este projeto é um **Simulador de Telemetria Industrial** que monitora a temperatura de uma sala em tempo real. Ele utiliza uma stack moderna em Python para criar um gêmeo digital (Digital Twin) de um circuito de hardware, integrando visualização 3D, análise de dados e armazenamento persistente.

## 🚀 Metas do Projeto
- **Visualização 3D:** Renderização de hardware estilizado (ESP32 + DHT22) em ambiente CAD.
- **Monitoramento em Tempo Real:** Medidor circular (Gauge) dinâmico com alertas visuais.
- **Persistência de Dados:** Armazenamento automático de todas as leituras em banco de dados SQL.
- **Histórico:** Gráfico de linha interativo para análise de tendências.

---

## 🛠️ Componentes do Sistema

### Hardware Simulado (Camada de Dados)
- **MCU:** ESP32 DevKit V1 (Simulação de processamento e conectividade).
- **Sensor:** DHT22 (Sensor digital de alta precisão para temperatura/umidade).
- **Comunicação:** Gerenciamento via Porta Serial Interna (Thread Synchronization).

### Software (Camada de Aplicação)
- **Dash & Plotly:** Engine gráfica para o Dashboard e o modelo 3D.
- **Pandas:** Manipulação e tratamento de séries temporais.
- **SQLite3:** Engine de banco de dados serverless para logs de telemetria.
- **Threading:** Processamento paralelo para garantir que a interface não trave durante a leitura do sensor.

---

## 📋 Pré-requisitos

Certifique-se de ter o Python 3.10 ou superior instalado. Recomenda-se o uso de um ambiente virtual.

```bash
# Instalação das dependências necessárias
pip install dash pandas dash-bootstrap-components plotly
```
## 💻 Como Executar
1. Clone o repositório:
```Bash
git clone [https://github.com/seu-usuario/kybermint-temperatura.git](https://github.com/seu-usuario/kybermint-temperatura.git)
```
2. Navegue até a pasta:
```Bash
cd kybermint-temperatura
Execute a aplicação:
```
3. Execute a aplicação:
```Bash
python kybermint_dashboard_pro.py
```
4. Acesse no seu navegador: http://127.0.0.1:8050

## 📊 Estrutura de Dados (Banco de Dados)

O sistema utiliza o SQLite para garantir que nenhuma leitura seja perdida. A tabela leituras possui a seguinte estrutura:

| Coluna | Tipo | Descrição |
| :--- | :---: | ---: |
| ida | INTEGER | Chave primária autoincrementada. |
| timestamp | TEXT | Data e hora exata da captura (YYYY-MM-DD HH:MM:SS). |
| temperatura | REAL | Valor flutuante da temperatura em graus Celsius.  |

## ⚙️ Arquitetura Técnica

O sistema opera em um modelo de Multithreading:

1. Thread A (Sensor): Gera dados randômicos realistas e injeta no banco de dados a cada 2 segundos.

2. Thread B (UI): O Dash monitora o banco de dados e atualiza os componentes visuais (3D e Gráficos) via Callbacks assíncronos.

##  ✒️ Autor

Marcio Bezerra Cavalcanti Junior