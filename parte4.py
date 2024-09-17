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

@st.cache_data
def carregar_ticker_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers

acoes = carregar_ticker_acoes()
dados = carregar_dados(acoes)

# criar a interface do streamlit
st.write("""
# App Preço de Ações
O Gráfico abaixo representa a evolução do preço das ações ao longo dos anos
""") # markdown

# preparar as visualizações
st.sidebar.header("Filtros")


#filtro de ações
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    # Tratando incompatibilidade com apenas uma ação
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})
    else:
        dados = dados[lista_acoes]

# filtro de datas
data_inicial =  dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()

intervalo_data = st.sidebar.slider("Selecione o período", 
                                   min_value=data_inicial, 
                                   max_value=data_final, 
                                   value=(data_inicial, data_final))

dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

# Criar gráfico
st.line_chart(dados)

# Performance
texto_performance_ativos = ""

if len(lista_acoes)==0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes)==1:
    dados = dados.rename(columns={"Close": acao_unica})

for acao in lista_acoes:
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)
    
    if performance_ativo > 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :green[{performance_ativo:.1%}]"
    elif performance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :red[{performance_ativo:.1%}]"
    else:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: {performance_ativo:.1%}"
        
st.write(f"""
### Performance dos Ativos
Esta foi a performance dos ativos no periodo selecionado:

{texto_performance_ativos}
""") # markdown