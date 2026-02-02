import streamlit as st
import pandas as pd
from github import Github
import io

# Configurações de Segurança (Pegas dos Secrets)
TOKEN = st.secrets["github_token"]
REPO_NAME = st.secrets["repo_name"]
FILE_NAME = "estoque.xlsx"

st.set_page_config(page_title="Sistema de Estoque", page_icon="🚗")

# Estilização
st.markdown("""<style>.stApp { background-color: #2b59b4; color: white; } .stButton>button { background-color: #f1d064; color: #1e3d7d; font-weight: bold; }</style>""", unsafe_allow_html=True)

st.title("🚗 Consulta de Estoque")

# Função para conectar ao GitHub
g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

# --- PARTE 1: UPLOAD E SALVAMENTO ---
with st.expander("⬆️ ATUALIZAR PLANILHA (SÓ QUANDO MUDAR O ESTOQUE)"):
    new_file = st.file_uploader("Suba o novo Excel para salvar no sistema", type=["xlsx"])
    if st.button("SALVAR NO SISTEMA"):
        if new_file:
            content = new_file.getvalue()
            try:
                # Tenta atualizar o arquivo existente
                contents = repo.get_contents(FILE_NAME)
                repo.update_file(contents.path, "Atualizando estoque", content, contents.sha)
                st.success("Salvo com sucesso! Agora todos os celulares verão este arquivo.")
                st.cache_data.clear() # Limpa o cache para ler o novo
            except:
                # Se o arquivo não existir, cria um novo
                repo.create_file(FILE_NAME, "Criando estoque inicial", content)
                st.success("Arquivo criado com sucesso!")

# --- PARTE 2: LEITURA E PESQUISA ---
@st.cache_data(ttl=300)
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
            st.write(f"**Placa:** {row['Placa']}")
            st.write(f"**Modelo:** {row['Modelo']}")
            st.write(f"**Cor:** {row['Cor']}")
            st.write(f"**Ano:** {row['Ano']}")
            st.write(f"**KM:** {row['KM']}")
            st.write(f"**Valor FIPE:** {row['Valor FIPE']}")
            st.write(f"**Valor:** {row['VALOR']}")
            st.write(f"**Margem:** {row['MARGEM']}")
        else:
            st.error("Placa não encontrada.")
    else:
        st.warning("Nenhum dado salvo. Por favor, faça o primeiro upload acima.")
