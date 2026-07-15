import streamlit as st
import pandas as pd

# 1. Configuração da página para ficar com cara de App
st.set_page_config(page_title="WMS Picking", page_icon="📦", layout="centered")

# 2. Adicionando Cores e Estilo (CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3em; 
        background-color: #004a99; 
        color: white; 
        font-weight: bold;
    }
    .result-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #004a99;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    h1 { color: #004a99; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 3. Cabeçalho
st.title("📦 WMS - Localizador")
st.write("---")

# 4. Carregamento dos dados
@st.cache_data
def carregar_dados():
    # Certifique-se de que o arquivo está na mesma pasta do app.py
    df = pd.read_csv('produtos.csv')
    return df

try:
    df = carregar_dados()

    # 5. Criando o formulário com o botão de pesquisa
    with st.form(key='search_form'):
        pesquisa = st.text_input("Digite o código ou descrição do produto:")
        submit_button = st.form_submit_button(label='🔍 PESQUISAR')

    # 6. Lógica de pesquisa (só acontece quando aperta o botão)
    if submit_button and pesquisa:
        # Filtro simples
        resultado = df[
            df['código'].astype(str).str.contains(pesquisa, case=False, na=False) | 
            df['descrição'].astype(str).str.contains(pesquisa, case=False, na=False)
        ]

        if not resultado.empty:
            st.success(f"Encontrei {len(resultado)} item(ns):")
            for _, item in resultado.iterrows():
                # Exibindo os resultados em "cards" bonitos
                st.markdown(f"""
                <div class="result-card">
                    <b>Produto:</b> {item['descrição']}<br>
                    <b>Código:</b> {item['código']}<br>
                    <b>Estação:</b> {item['estação']}<br>
                    <b>Local:</b> Rack {item['Rack']} | Linha {item['linha']} | Coluna {item['coluna']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum produto encontrado. Verifique o código!")
    elif submit_button and not pesquisa:
        st.error("Por favor, digite algo para pesquisar.")

except Exception as e:
    st.error("Erro ao carregar os dados. Verifique se o arquivo produtos.csv está no GitHub.")
