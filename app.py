import streamlit as st
import pandas as pd
import base64

# Configuração da página
st.set_page_config(page_title="WMS Picking", layout="centered")

# Função para converter a imagem em Base64
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return None

base64_image = get_image_base64("image_de2449.jpg")

# CSS para o visual
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    [data-testid="stAppViewContainer"]::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(30, 42, 56, 0.6); z-index: 0;
    }}
    [data-testid="stAppViewContainer"] > * {{ z-index: 1; position: relative; }}
    .log-card {{ background-color: rgba(255, 255, 255, 0.9); border-left: 10px solid #ff7f0e; padding: 20px; margin-bottom: 20px; color: #333; }}
    .log-titulo {{ color: #d35400; font-size: 1.5em; font-weight: bold; }}
    .grid-container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }}
    .grid-item {{ background: #ecf0f1; padding: 10px; text-align: center; color: #2c3e50; border: 1px solid #bdc3c7; }}
    </style>
""", unsafe_allow_html=True) # AQUI ESTAVA O ERRO, CORRIGIDO PARA unsafe_allow_html

st.title("📦 WMS - CENTRAL DE PICKING")

# Leitura automática
@st.cache_data(ttl=60)
def carregar_dados():
    df = pd.read_csv('produtos.csv', encoding='latin1', sep=';', on_bad_lines='skip', engine='python', dtype=str)
    df.columns = df.columns.str.strip()
    return df

try:
    df = carregar_dados()
    termo = st.text_input("🔍 CONSULTAR ITEM:")

    if termo:
        mask = (df['código'].str.contains(termo, na=False, case=False) | 
                df['descrição'].str.contains(termo, na=False, case=False))
        resultado = df[mask]
        
        if not resultado.empty:
            for _, row in resultado.iterrows():
                st.markdown(f"""
                <div class="log-card">
                    <div class="log-titulo">ITEM: {row['código']}</div>
                    <div style="font-weight: 600;">{row['descrição']}</div>
                    <div class="grid-container">
                        <div class="grid-item"><b>EST:</b> {row['estação']}</div>
                        <div class="grid-item"><b>RACK:</b> {row['Rack']}</div>
                        <div class="grid-item"><b>LINHA:</b> {row['linha']}</div>
                        <div class="grid-item"><b>COL:</b> {row['coluna']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ ITEM NÃO ENCONTRADO.")
except Exception as e:
    st.error(f"Erro: Arquivo 'produtos.csv' não encontrado na pasta ou corrompido.")
