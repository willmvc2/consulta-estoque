import streamlit as st
import pandas as pd
import os

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Estoque Unidas",
    page_icon="🚗",
    layout="centered"
)

# ==============================
# ESTILO
# ==============================
st.markdown("""
<style>
.stApp { background-color: #1f3c88; color: white; }
h1, h2, h3 { color: white; }
label { color: white !important; }
.stButton>button {
    background-color: #f1d064;
    color: #1f3c88;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🚗 Estoque Unidas")

# ==============================
# VARIÁVEIS
# ==============================
ARQUIVO_ESTOQUE = "estoque.xlsx"

# ==============================
# FUNÇÕES
# ==============================
def carregar_estoque():
    if os.path.exists(ARQUIVO_ESTOQUE):
        df = pd.read_excel(ARQUIVO_ESTOQUE)
        df.columns = df.columns.str.strip()
        df["Placa"] = df["Placa"].astype(str).str.upper().str.strip()
        return df
    return None

# ==============================
# CONTROLE ADMIN (LINK SECRETO)
# ==============================
query_params = st.experimental_get_query_params()
modo_admin = query_params.get("admin", ["0"])[0] == "1"

if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

# ==============================
# LOGIN ADMIN (SÓ SE URL TIVER ?admin=1)
# ==============================
if modo_admin and not st.session_state.admin_logado:
    st.subheader("🔐 Login Administrador")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if (
            email == st.secrets["ADMIN_EMAIL"]
            and senha == st.secrets["ADMIN_SENHA"]
        ):
            st.session_state.admin_logado = True
            st.success("Login realizado com sucesso")
        else:
            st.error("Email ou senha inválidos")

# ==============================
# ÁREA ADMIN (SÓ SE LOGADO)
# ==============================
if modo_admin and st.session_state.admin_logado:
    st.subheader("📤 Atualizar Estoque")

    arquivo = st.file_uploader(
        "Enviar planilha Excel",
        type=["xlsx"]
    )

    if arquivo:
        df = pd.read_excel(arquivo)
        df.to_excel(ARQUIVO_ESTOQUE, index=False)
        st.success("Estoque atualizado com sucesso")

    if st.button("Sair"):
        st.session_state.admin_logado = False

st.markdown("---")

# ==============================
# CONSULTA PÚBLICA (SEMPRE VISÍVEL)
# ==============================
st.subheader("🔎 Consultar veículo por placa")

placa = st.text_input("Digite a placa (ex: ABC1D23)").upper().strip()

if st.button("PESQUISAR"):
    df = carregar_estoque()

    if df is None:
        st.error("Estoque ainda não cadastrado.")
    else:
        resultado = df[df["Placa"] == placa]

        if resultado.empty:
            st.warning("Placa não encontrada.")
        else:
            r = resultado.iloc[0]
            st.success("Veículo encontrado")
            st.write(f"**Placa:** {r['Placa']}")
            st.write(f"**Modelo:** {r['Modelo']}")
            st.write(f"**Cor:** {r['Cor']}")
            st.write(f"**Ano:** {r['Ano']}")
            st.write(f"**KM:** {r['KM']}")
            st.write(f"**Valor FIPE:** R$ {r['Valor FIPE']:,.2f}")
            st.write(f"**Valor:** R$ {r['VALOR']:,.2f}")
            st.write(f"**Margem:** {r['MARGEM']}")
