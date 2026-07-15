import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="WMS Picking", page_icon="📦", layout="centered")

# 2. Estilo Visual (CSS)
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
    # Carrega o arquivo dados.csv
    df = pd.read_csv('dados.csv')
    return df

try:
    df = carregar_dados()

    # 5. Formulário de pesquisa
    with st.form(key='search_form'):
        pesquisa = st.text_input("Digite o código ou descrição:")
        submit_button = st.form_submit_button(label='🔍 PESQUISAR')

    # 6. Lógica de pesquisa
    if submit_button and pesquisa:
        # Filtro nas colunas 'codigo' e 'descricao'
        resultado = df[
            df['codigo'].astype(str).str.contains(pesquisa, case=False, na=False) | 
            df['descricao'].astype(str).str.contains(pesquisa, case=False, na=False)
        ]

        if not resultado.empty:
            st.success(f"Encontrei {len(resultado)} item(ns):")
            for _, item in resultado.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <b>Produto:</b> {item['descricao']}<br>
                    <b>Código:</b> {item['codigo']}<br>
                    <b>Estação:</b> {item['estacao']}<br>
                    <b>Local:</b> Rack {item['Rack']} | Linha {item['linha']} | Coluna {item['coluna']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum produto encontrado. Verifique o que digitou!")
    elif submit_button and not pesquisa:
        st.error("Por favor, digite algo para pesquisar.")

except Exception as e:
    st.error("Erro ao carregar o arquivo 'dados.csv'. Verifique se ele está no GitHub e se os nomes das colunas estão corretos.")
