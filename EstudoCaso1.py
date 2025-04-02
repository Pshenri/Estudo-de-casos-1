import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

def analisar_logs_acesso(caminho_arquivo='portaria_log.json', database_file='acessos.db'):
    try:
        # 1. Leitura do arquivo CSV para um DataFrame do pandas
        df = pd.read_csv(caminho_arquivo)
        
        # 2. Limpeza e preparação dos dados
        df.columns = df.columns.str.strip()  # Remove espaços extras dos nomes das colunas
        df['Data e Hora'] = pd.to_datetime(df['Data e Hora'])  # Converte a coluna 'Data e Hora' para datetime
        df['Hora'] = df['Data e Hora'].dt.hour  # Extrai a hora e cria uma nova coluna 'Hora'
        df['Minuto'] = df['Data e Hora'].dt.minute # Extrai o minuto e cria nova coluna 'Minuto'
        df['Tipo de Usuário'] = df['Observações'].apply(lambda x: x.split()[0] if isinstance(x, str) else 'Desconhecido') # Extrai o primeiro nome da coluna observações para classificar o tipo de usuário.
        df = df[pd.to_numeric(df['Tempo de Resposta (segundos)'], errors='coerce').notna()] # Garante que a coluna 'Tempo de Resposta (segundos)' contenha apenas valores numéricos válidos.
        df['Tempo de Resposta (segundos)'] = df['Tempo de Resposta (segundos)'].astype(int) # Converte a coluna 'Tempo de Resposta (segundos)' para inteiro

        # 3. Detecção de anomalias usando Isolation Forest
        modelo_if = IsolationForest(contamination=0.05)  # Cria um modelo Isolation Forest
        df['Anomalia'] = modelo_if.fit_predict(df[['Tempo de Resposta (segundos)']])  # Treina o modelo e detecta anomalias

        # 4. Classificação de acessos com base em anomalias e outros critérios
        def classificar_acesso(row):
            if row['Anomalia'] == -1:
                return 'Suspeito'
            elif row['Status'] == 'Negado' or 'Alarme' in row['Tipo de Evento']:
                return 'Crítico'
            else:
                return 'Normal'
        df['Classificação'] = df.apply(classificar_acesso, axis=1)  # Aplica a função para classificar os acessos

        # 5. Alerta para acessos críticos
        acessos_criticos = df[df['Classificação'] == 'Crítico']
        if not acessos_criticos.empty:
            print("\nALERTA: Acessos Críticos Detectados!")
            for index, row in acessos_criticos.iterrows():
                print(f"- Data/Hora: {row['Data e Hora']}")
                print(f"- Tipo de Evento: {row['Tipo de Evento']}")
                print(f"- Usuário/Veículo: {row['Usuário/Veículo']}")
                print(f"- Observações: {row['Observações']}\n")

        # 6. Visualizações dos dados
        visualizar_distribuicao_acessos(df)  # Distribuição de acessos por hora
        visualizar_anomalias(df)  # Anomalias no tempo de resposta
        visualizar_tipos_eventos(df)  # Contagem de tipos de eventos

        # 7. Armazenamento dos dados em um banco de dados SQLite
        armazenar_dados_sqlite(df, database_file)  # Salva os dados em um banco de dados SQLite

    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def visualizar_distribuicao_acessos(df):
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x='Hora', data=df)  # Cria um gráfico de contagem de acessos por hora
    plt.title('Distribuição de Acessos por Hora do Dia')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Número de Acessos')
    
    # Adiciona a contagem de acessos em cada barra
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black', weight='bold')
    
    plt.show()

def visualizar_anomalias(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Data e Hora', y='Tempo de Resposta (segundos)', hue='Anomalia', data=df)  # Cria um gráfico de dispersão para visualizar anomalias
    plt.title('Anomalias no Tempo de Resposta')
    plt.xlabel('Data e Hora')
    plt.ylabel('Tempo de Resposta (segundos)')
    plt.show()

def visualizar_tipos_eventos(df):
    plt.figure(figsize=(12, 6))
    ax = sns.countplot(x='Tipo de Evento', data=df)  # Cria um gráfico de contagem de tipos de eventos
    plt.title('Contagem de Tipos de Eventos')
    plt.xlabel('Tipo de Evento')
    plt.ylabel('Contagem')
    plt.xticks(rotation=45, ha='right')  # Rotaciona os rótulos do eixo x para melhor visualização
    
    # Adiciona a contagem de cada tipo de evento em cada barra
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black', weight='bold')
    
    plt.tight_layout()
    plt.show()

def armazenar_dados_sqlite(df, database_file):
    try:
        conn = sqlite3.connect(database_file)  # Conecta ao banco de dados SQLite
        df.to_sql('acessos', conn, if_exists='replace', index=False)  # Salva o DataFrame na tabela 'acessos'
        conn.close()  # Fecha a conexão com o banco de dados
        print(f"\nDados armazenados com sucesso em '{database_file}'.")
    except Exception as e:
        print(f"Erro ao armazenar dados em SQLite: {e}")

# Exemplo de uso
analisar_logs_acesso()