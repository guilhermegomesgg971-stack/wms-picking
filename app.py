import streamlit as st
import pandas as pd

# Mantivemos tudo, apenas adicionamos o estilo visual
st.set_page_config(page_title="WMS Picking", page_icon="📦")
st.markdown("""
    <style>
    .stButton>button { background-color: #004a99; color: white; border-radius: 10px; width: 100%; }
    .card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Lógica original de leitura
@st.cache_data
def carregar_dados():
    return pd.read_csv('produtos.csv')

df = carregar_dados()

st.title("📦 WMS Picking")

# Adicionamos apenas o botão para disparar a busca
pesquisa = st.text_input("Digite o código ou descrição do produto:")
botao_pesquisar = st.button("🔍 PESQUISAR")

# A lógica de busca continua a mesma, só colocamos ela dentro do clique do botão
if botao_pesquisar:
    if pesquisa:
        resultado = df[
            df['código'].astype(str).str.contains(pesquisa, case=False, na=False) | 
            df['descrição'].astype(str).str.contains(pesquisa, case=False, na=False)
        ]
        
        if not resultado.empty:
            for _, item in resultado.iterrows():
                st.markdown(f"""
                <div class="card">
                    <b>{item['descrição']}</b><br>
                    Cód: {item['código']} | Local: {item['Rack']} - {item['linha']} - {item['coluna']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum produto encontrado.")
    else:
        st.error("Digite um termo para pesquisar.")
