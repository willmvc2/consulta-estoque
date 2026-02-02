import streamlit as st
import pandas as pd
from github import Github
import io

# Tenta pegar as chaves de segurança
try:
    TOKEN = st.secrets["github_token"]
    REPO_NAME = st.secrets["repo_name"]
    FILE_NAME = "estoque.xlsx"
    g = Github(TOKEN)
    repo = g.get_repo(REPO_NAME)
except Exception as e:
    st.error(f"Erro de Configuração: Verifique os 'Secrets' no Streamlit. {e}")
    st.stop()

st.set_page_config(page_title="Sistema de Estoque", page_icon="🚗")

# Estilização
st.markdown("""<style>.stApp { background-color: #2b59b4; color: white; } .stButton>button { background-color: #f1d064; color: #1e3d7d; font-weight: bold; }</style>""", unsafe_allow_html=True)

st.title("🚗 Consulta de Estoque")

# --- AREA DE UPLOAD ---
with st.expander("⬆️ CLIQUE AQUI PARA ATUALIZAR A PLANILHA"):
    new_file = st.file_uploader("Selecione o novo Excel", type=["xlsx"])
    if st.button("SALVAR NO SISTEMA"):
        if new_file:
            try:
                content = new_file.getvalue()
                try:
                    contents = repo.get_contents(FILE_NAME)
                    repo.update_file(contents.path, "Update", content, contents.sha)
                except:
                    repo.create_file(FILE_NAME, "Initial", content)
                st.success("✅ Salvo! Agora todos os aparelhos podem consultar.")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Erro ao salvar no GitHub: {e}")

# --- AREA DE PESQUISA ---
@st.cache_data(ttl=60)
def load_data():
    try:
        file_content = repo.get_contents(FILE_NAME)
        return pd.read_excel(io.BytesIO(file_content.decoded_content))
    except:
        return None

df = load_data()

st.subheader("DIGITE A PLACA")
placa_input = st.text_input("", "").upper().strip()

if st.button("PESQUISAR"):
    if df is not None:
        df.columns = df.columns.str.strip()
        df['Placa'] = df['Placa'].astype(str).str.strip().str.upper()
        res = df[df['Placa'] == placa_input]
        
        if not res.empty:
            row = res.iloc[0]
            st.markdown("---")
            for col in ['Placa', 'Modelo', 'Cor', 'Ano', 'KM', 'Valor FIPE', 'VALOR', 'MARGEM']:
                if col in df.columns:
                    st.write(f"**{col}:** {row[col]}")
        else:
            st.error("Placa não encontrada.")
    else:
        st.warning("O sistema ainda está vazio. Faça o primeiro upload no botão acima.")
