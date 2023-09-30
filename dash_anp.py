import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout='wide')

@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io = "base_anp_new.xlsx",
        engine = "openpyxl",
        sheet_name = "base",
        usecols = "A:Q",
        nrows = 20323
    )
    return df
df = gerar_df()
colunasUteis = ['MÊS', 'PRODUTO', 'REGIÃO', 'ESTADO', 'PREÇO MÉDIO REVENDA']
df = df[colunasUteis]

with st.sidebar:
    st.subheader('BASE ANP 2013-AGO/2023')
    st.subheader('BY CRISTIAN CASSOLI')
    logo = Image.open('logo_fuel.png')
    st.image(logo, use_column_width=True)
    st.subheader('SELEÇÃO DE FILTROS')
    fProduto = st.selectbox(
        "Selecione o combustível:",
        options=df['PRODUTO'].unique()
    )
    
    fEstado = st.selectbox(
        "Selecione o estado:",
        options=df['ESTADO'].unique()
    )

    dadosUsuario = df.loc[(
        df['PRODUTO'] == fProduto) &
        (df['ESTADO'] == fEstado)
    ]

updateDatas = dadosUsuario['MÊS'].dt.strftime('%Y/%b')
dadosUsuario['MÊS'] = updateDatas[0:]

st.header('PREÇO DOS COMBUSTÍVEIS NO BRASIL: 2013 À AGO/2023')
st.markdown('**Combustível selecionado:** ' + fProduto)
st.markdown('**Estado selecionado** ' + fEstado)

grafCombEstado = alt.Chart(dadosUsuario).mark_line(
    point=alt.OverlayMarkDef(color='red', size=20)
).encode(
    x = 'MÊS:T',
    y = 'PREÇO MÉDIO REVENDA',
    strokeWidth = alt.value(3)
).properties(
    height = 600,
    width = 1100
)

st.altair_chart(grafCombEstado)