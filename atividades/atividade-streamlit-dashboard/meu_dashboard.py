from pathlib import Path

import pandas as pd
import streamlit as st

# Fase 1 - Estrutura básica e otimização de desempenho
st.set_page_config(page_title='Dashboard de Vendas', layout='wide')
st.title('Dashboard de Vendas')

CAMINHO_CSV = Path(__file__).parent / 'vendas.csv'


@st.cache_data
def carregar_dados():
    df = pd.read_csv(CAMINHO_CSV, parse_dates=['data'])
    return df


df = carregar_dados()

# Fase 2 - Layout e filtros laterais
st.sidebar.title('Filtros')

lista_de_categorias = sorted(df['categoria'].unique())
categorias_selecionadas = st.sidebar.multiselect(
    'Selecione as Categorias',
    options=lista_de_categorias,
    default=lista_de_categorias,
)

df_filtrado = df[df['categoria'].isin(categorias_selecionadas)]

if df_filtrado.empty:
    st.warning('Selecione ao menos uma categoria para visualizar os dados.')
    st.stop()

# Fase 3 - Métricas em destaque e visualização de dados
receita_calculada = df_filtrado['receita'].sum()
total_pedidos = len(df_filtrado)

col1, col2 = st.columns([1, 1])

with col1:
    st.metric(
        label='Receita Total',
        value=f'R$ {receita_calculada:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
    )

with col2:
    st.metric(label='Total de Pedidos', value=f'{total_pedidos:,}'.replace(',', '.'))

aba1, aba2 = st.tabs(['Evolução Mensal', 'Tabela de Dados'])

with aba1:
    st.subheader('Receita por mês')
    dados_agrupados = (
        df_filtrado
        .groupby(df_filtrado['data'].dt.to_period('M').dt.to_timestamp())['receita']
        .sum()
        .rename('Receita')
    )
    dados_agrupados.index.name = 'Mês'
    st.area_chart(dados_agrupados)

with aba2:
    st.subheader('Dados filtrados')
    st.dataframe(df_filtrado, width='stretch',hide_index=True)

    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label='Baixar dados em CSV',
        data=csv,
        file_name='vendas_filtradas.csv',
        mime='text/csv',
    )
