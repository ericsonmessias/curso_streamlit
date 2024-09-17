# Importar as bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf

# Criar as funções de carregamento de dados
    # cotações do Itau ITUB4 2010 a 2024
@st.cache_data #decorator atribui uma funcionalidade ao código subsequente 
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-07-01")
    cotacoes_acao = cotacoes_acao["Close"] #Retorna valor de fechamento em forma de tabela
    return cotacoes_acao

acoes = ["ITUB4.SA","CPLE6.SA","BBAS3.SA","BBSE3.SA"]
dados = carregar_dados(acoes)

# criar a interface do streamlit
st.write("""
# App Preço de Ações
O Gráfico abaixo representa a evolução do preço das ações ao longo dos anos
""") # markdown

# preparar as visualizações
lista_acoes = st.multiselect("Escolha as ações para visualizar", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    # Tratando incompatibilidade com apenas uma ação
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})
    else:
        dados = dados[lista_acoes]

print(dados)
# Criar gráfico
st.line_chart(dados)