import streamlit as st
import pandas as pd

st.set_page_config(page_title="WMS Picking", page_icon="📦")

# Estilo visual
st.markdown("""
    <style>
    .result-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #004a99; }
    </style>
""", unsafe_allow_html=True)

st.title("📦 WMS - Localizador")

@st.cache_data
def carregar_dados():
    df = pd.read_csv('produtos.csv')
    # Esta linha abaixo é o segredo: ela padroniza tudo para minúsculo e sem espaço
    df.columns = df.columns.str.lower().str.strip()
    return df

try:
    df = carregar_dados()
    pesquisa = st.text_input("Digite o código ou descrição:")
    btn = st.button("🔍 PESQUISAR")

    if btn and pesquisa:
        # Filtra usando as colunas padronizadas
        resultado = df[
            df['codigo'].astype(str).str.contains(pesquisa, case=False, na=False) | 
            df['descricao'].astype(str).str.contains(pesquisa, case=False, na=False)
        ]

        if not resultado.empty:
            for _, item in resultado.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <b>Produto:</b> {item['descricao']}<br>
                    <b>Código:</b> {item['codigo']}<br>
                    <b>Local:</b> Rack {item['rack']} | Linha {item['linha']} | Coluna {item['coluna']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Produto não encontrado.")

except Exception as e:
    st.error(f"Erro ao ler o arquivo. Detalhe: {e}")
    st.write("Dica: Verifique se o arquivo se chama 'produtos.csv' e se as colunas 'codigo', 'descricao', 'rack', 'linha' e 'coluna' existem.")
