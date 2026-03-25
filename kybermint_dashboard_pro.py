import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import random
import time
from datetime import datetime
import threading

# ==========================================
# CONFIGURAÇÕES E BANCO DE DADOS (N2 Storage)
# ==========================================
NOME_BANCO = 'temp_monitor_data_pro.db'

# Simulação de temperatura da sala (para não precisar de hardware real)
sim_temperatura_base = 24.5

def inicializar_banco():
    """Cria o banco de dados e a tabela se não existirem."""
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS leituras 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       timestamp TEXT, 
                       temperatura REAL)''')
    conn.commit()
    conn.close()

def salvar_leitura(temp):
    """Armazena a leitura de temperatura no banco de dados."""
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leituras (timestamp, temperatura) VALUES (?, ?)",
                   (datetime.now().strftime('%H:%M:%S'), temp))
    conn.commit()
    conn.close()

def obter_historico():
    """Retorna o histórico para o gráfico."""
    conn = sqlite3.connect(NOME_BANCO)
    df = pd.read_sql_query("SELECT timestamp, temperatura FROM leituras ORDER BY id DESC LIMIT 50", conn)
    conn.close()
    return df

# ==========================================
# SIMULAÇÃO DO HARDWARE (Interna e Concurrency)
# ==========================================
def sensor_thread_loop():
    """Thread dedicada que simula o sensor e o banco de dados."""
    global sim_temperatura_base
    inicializar_banco()
    while True:
        # Simula flutuação de temperatura real de uma sala
        sim_temperatura_base += random.uniform(-0.4, 0.4)
        
        # Limita a temperatura entre 18°C e 28°C
        sim_temperatura_base = max(18.0, min(28.0, sim_temperatura_base))
        
        # Salva no banco de dados (armazena a informação)
        salvar_leitura(sim_temperatura_base)
        
        time.sleep(2) # Próxima leitura em 2 segundos

# Inicia a simulação em segundo plano
threading.Thread(target=sensor_thread_loop, daemon=True).start()

# ==========================================
# COMPONENTES GRÁFICOS E MODELAGEM 3D CAD
# ==========================================
# Estilo "Dark Pro" (N2 UI/UX)
ESTILO_DARK_BG = {"backgroundColor": "#121212", "color": "white", "height": "100vh", "padding": "20px"}
ESTILO_CARD = {"backgroundColor": "#1e1e1e", "color": "white", "borderRadius": "10px", "border": "1px solid #333"}

# Função auxiliar para criar formas geométricas (N2 CAD Drawing)
def criar_cubo(x, y, z, dx, dy, dz, color, name):
    """Cria geometrias 3D em estilo CAD profissional."""
    return go.Mesh3d(
        # Vértices do cubo
        x=[x, x+dx, x+dx, x, x, x+dx, x+dx, x],
        y=[y, y, y+dy, y+dy, y, y, y+dy, y+dy],
        z=[z, z, z, z, z+dz, z+dz, z+dz, z+dz],
        # Faces do cubo
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color=color, name=name, opacity=1.0, flatshading=True, hoverinfo="name"
    )

# Função para criar o HARDWARE 3D MANEIRO (Clonando Image 7/8)
def criar_hardware_3d(temp):
    """Cria a cena 3D nativa integrada no painel."""
    fig = go.Figure()
    
    # Adiciona os componentes (Modelagem CAD simplificada mas detalhada)
    fig.add_trace(criar_cubo(0, 0, 0, 10, 6, 0.1, '#0f380f', 'PCB (KyberMint Node)')) # Placa Verde Escura
    fig.add_trace(criar_cubo(1, 1, 0.1, 3, 4, 0.3, '#1a1a1a', 'ESP32 MCU')) # Chip ESP32
    fig.add_trace(criar_cubo(6, 2, 0.1, 2, 2, 1.2, '#e0e0e0', 'Sensor DHT22')) # Sensor Branco
    
    # Simulação de Fiação (Jumpers coloridos style Image 7)
    fig.add_trace(go.Scatter3d(x=[4, 6], y=[2, 2.5], z=[0.2, 0.6], mode='lines', line=dict(color='red', width=5), name="VCC"))
    fig.add_trace(go.Scatter3d(x=[4, 6], y=[3, 3], z=[0.2, 0.6], mode='lines', line=dict(color='yellow', width=5), name="DATA"))
    fig.add_trace(go.Scatter3d(x=[4, 6], y=[4, 3.5], z=[0.2, 0.6], mode='lines', line=dict(color='black', width=5), name="GND"))

    # Adiciona Texto flutuante no 3D (para telemetria HUD style)
    fig.add_trace(go.Scatter3d(x=[5], y=[3], z=[3], mode='text', text=[f"Temp: {temp:.1f}°C"], textfont=dict(color='#00aaff', size=25), name="Leitura"))

    # Configurações da Cena 3D
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            camera=dict(eye=dict(x=-1.5, y=-1.5, z=1.5)) # Ângulo isométrico de CAD
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=500
    )
    return fig

# Função para criar o medidor circular profissional (Gauge) style Image 4
def criar_gauge_profissional(value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        number = {'suffix': "°C", 'font': {'color': 'white', 'size': 50}},
        title = {'text': "TEMPERATURA ATUAL", 'font': {'color': 'gray', 'size': 18}},
        gauge = {
            'axis': {'range': [18, 28], 'tickcolor': 'gray', 'tickwidth': 1},
            'bar': {'color': "#00aaff"}, # Cor do medidor circular azul
            'bgcolor': "#333",
            'borderwidth': 0,
            'steps': [
                {'range': [18, 21], 'color': 'rgba(0, 170, 255, 0.1)'},
                {'range': [21, 26], 'color': 'rgba(0, 170, 255, 0.2)'},
                {'range': [26, 28], 'color': 'rgba(255, 0, 0, 0.3)'}
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', # Fundo transparente do card
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        height=250
    )
    return fig

# Função para criar o gráfico histórico style Image 4
def criar_grafico_historico(df):
    if df.empty:
        return go.Figure().update_layout(template="plotly_dark")
    
    # Inverte para o tempo correr da esquerda para a direita
    df = df.iloc[::-1]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['temperatura'], mode='lines', 
                             line=dict(color='#00aaff', width=3), 
                             fill='tozeroy', fillcolor='rgba(0, 170, 255, 0.1)')) # Sombra style Image 4
    
    fig.update_layout(
        title = {'text': "LOG DE HISTÓRICO (BD SQLite3)", 'font': {'color': 'white', 'size': 16}},
        xaxis = {'title': "Tempo", 'tickcolor': 'gray', 'gridcolor': '#333'},
        yaxis = {'title': "Temperatura (°C)", 'range': [18, 28], 'tickcolor': 'gray', 'gridcolor': '#333'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
        height=250
    )
    return fig

# ==========================================
# LAYOUT DO DASHBOARD (Dash UI)
# ==========================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(style=ESTILO_DARK_BG, children=[
    dbc.Container(fluid=True, children=[
        # Título Principal Pro style Image 4
        dbc.Row(className="mb-4", children=[
            dbc.Col(html.H1("SYSTEM TELEMETRY - KYBERMINT", className="text-white text-left"), width=12)
        ]),
        
        # Grid Principal de 2 Colunas style Image 4
        dbc.Row(className="mb-4", children=[
            # COLUNA ESQUERDA: VISUALIZAÇÃO 3D (O 3D MANEIRO e Detalhado)
            dbc.Col(width=7, children=[
                dbc.Card(style=ESTILO_CARD, children=[
                    dbc.CardHeader(html.H4("HARDWARE NODE (Modelo CAD)", className="text-white")),
                    dbc.CardBody(children=[
                        # ATENÇÃO N2: Aqui está a integração!
                        # Estamos usando dcc.Graph nativo para renderizar o modelo 3D
                        # fotorrealista/estilizado de CAD.
                        dcc.Graph(id='hardware-3d')
                    ])
                ])
            ]),
            
            # COLUNA DIREITA: TELEMETRIA (Medidor circular e Gráfico style Image 4)
            dbc.Col(width=5, children=[
                dbc.Card(style=ESTILO_CARD, className="mb-4", children=[
                    dbc.CardBody(dcc.Graph(id='gauge-temperatura'))
                ]),
                dbc.Card(style=ESTILO_CARD, children=[
                    dbc.CardBody(dcc.Graph(id='grafico-historico'))
                ])
            ])
        ]),
        
        # Intervalo de Atualização (N2 Performance)
        dcc.Interval(id='interval-update', interval=2000, n_intervals=0) # Atualiza a UI a cada 2 seg
    ])
])

# ==========================================
# CALLBACKS (UI/UX Real-time Sync)
# ==========================================
# Atualiza a UI completa (3D, Medidor e Gráfico) em tempo real (N2 Sync)
@app.callback(
    [Output('hardware-3d', 'figure'),
     Output('gauge-temperatura', 'figure'),
     Output('grafico-historico', 'figure')],
    [Input('interval-update', 'n_intervals')]
)
def update_dashboard_ui(n):
    # Obtém a temperatura simulada mais recente da thread de hardware
    temp_atual = sim_temperatura_base
    
    # Busca o histórico do banco de dados
    df_hist = obter_historico()
    
    # Atualiza a cena 3D, o Medidor e o Gráfico (METAs Atendidas)
    fig_3d = criar_hardware_3d(temp_atual)
    fig_gauge = criar_gauge_profissional(temp_atual)
    fig_hist = criar_grafico_historico(df_hist)
    
    return fig_3d, fig_gauge, fig_hist

# ==========================================
# PASSO FINAL: EXECUÇÃO
# ==========================================
# Agora nós podemos rodar o Dash na thread principal sem travar o signal.
# O Dash 3D integrado elimina a necessidade de VPython em background.
if __name__ == '__main__':
    print("--- Inicializando Dashboard Telemetria Pro KyberMint (Abra o Navegador) ---")
    print("Abra o navegador em: http://127.0.0.1:8050")
    app.run(debug=True, port=8050, use_reloader=False) # Lança na porta 8050