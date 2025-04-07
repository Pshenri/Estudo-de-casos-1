Pipeline de Logs Inteligente para Análise de Acessos em Sistema de Portaria Virtual com Foco em Modelos Preditivos de Comportamento

Este projeto realiza a análise de logs de acesso de um sistema de portaria, identificando padrões de acesso, detectando anomalias no tempo de resposta e classificando os acessos como normais, suspeitos ou críticos. Os resultados são apresentados em visualizações gráficas e armazenados em um banco de dados SQLite para futuras análises.

Funcionalidades Principais
Leitura e Limpeza de Dados: Carrega logs de acesso de um arquivo CSV, limpa e prepara os dados para análise, convertendo colunas para os tipos de dados apropriados e removendo valores inválidos.
Detecção de Anomalias: Utiliza o modelo Isolation Forest para identificar acessos com tempos de resposta atípicos, classificando-os como anomalias.
Classificação de Acessos: Classifica os acessos com base em anomalias detectadas, status de acesso (negado) e tipos de eventos (alarmes), categorizando-os como normais, suspeitos ou críticos.
Visualização de Dados: Apresenta os resultados da análise em gráficos informativos, incluindo a distribuição de acessos por hora do dia, anomalias no tempo de resposta e a contagem de tipos de eventos.
Armazenamento de Dados: Armazena os dados analisados em um banco de dados SQLite para facilitar a consulta e análise futura.
Alertas de Acessos Críticos: Exibe alertas detalhados para acessos classificados como críticos.

NOME: PEDRO HENRI QUE ALVES DE CAMPOS RGM:29548152
NOMD: Henry Kauã de Oliveira Cavalcanti
