import streamlit as st
import pandas as pd

# Carregar os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv('produtos.csv')

df = carregar_dados()

# Interface simples
st.title("WMS Picking")

pesquisa = st.text_input("Digite o código ou descrição do produto:")

if pesquisa:
    resultado = df[
        df['código'].astype(str).str.contains(pesquisa, case=False, na=False) | 
        df['descrição'].astype(str).str.contains(pesquisa, case=False, na=False)
    ]
    
    if not resultado.empty:
        st.write(resultado)
    else:
        st.warning("Nenhum produto encontrado.")
