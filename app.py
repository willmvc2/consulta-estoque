import streamlit as st
import pandas as pd

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Estoque Unidas",
    page_icon="🚗",
    layout="centered"
)

# ==============================
# ESTILO VISUAL
# ==============================
st.markdown("""
<style>
.stApp {
    background-color: #1f3c88;
}
h1, h2, h3, label {
    color: white;
}
.stButton>button {
    background-color: #f1d064;
    color: #1f3c88;
    font-weight: bold;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# TÍTULO
# ==============================
st.markdown("## 🚗 Estoque Unidas")

# ==============================
# INICIALIZA SESSION STATE
# ==============================
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

if "df" not in st.session_state:
    st.session_state.df = None

# ==============================
# ÁREA DO ADMIN (SÓ SE LOGAR)
# ==============================
with st.expander("🔒 Área do Administrador"):

    if not st.session_state.admin_logado:
        email = st.text_input("Email do administrador")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar como Admin"):
            if (
                email == st.secrets["ADMIN_EMAIL"]
                and senha == st.secrets["ADMIN_SENHA"]
            ):
                st.session_state.admin_logado = True
                st.success("Administrador logado com sucesso!")
                st.rerun()
            else:
                st.error("Email ou senha incorretos")

    else:
        st.success("Você está logado como ADMIN")

        uploaded_file = st.file_uploader(
            "📤 Enviar planilha Excel",
            type=["xlsx"]
        )

        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                df.columns = df.columns.str.strip()
                df["Placa"] = df["Placa"].astype(str).str.upper().str.strip()

                st.session_state.df = df
                st.success("Planilha carregada com sucesso!")

            except Exception:
                st.error("Erro ao ler a planilha. Verifique o formato.")

        if st.button("Sair do Admin"):
            st.session_state.admin_logado = False
            st.rerun()

# ==============================
# ÁREA DO USUÁRIO (SEM LOGIN)
# ==============================
st.markdown("---")
st.markdown("### 🔎 Consultar veículo por placa")

placa = st.text_input(
    "Digite a placa (ex: ABC1D23)",
    "").upper().strip()

if st.button("Pesquisar"):
    if st.session_state.df is None:
        st.warning("Nenhuma planilha carregada pelo administrador.")
    else:
        resultado = st.session_state.df[
            st.session_state.df["Placa"] == placa
        ]

        if resultado.empty:
            st.error("Placa não encontrada.")
        else:
            row = resultado.iloc[0]

            st.markdown("---")
            st.write(f"**Placa:** {row['Placa']}")
            st.write(f"**Modelo:** {row['Modelo']}")
            st.write(f"**Cor:** {row['Cor']}")
            st.write(f"**Ano:** {row['Ano']}")
            st.write(f"**KM:** {row['KM']}")

            st.write(
                f"**Valor FIPE:** R$ {row['Valor FIPE']:,.2f}"
                if isinstance(row["Valor FIPE"], (int, float))
                else f"**Valor FIPE:** {row['Valor FIPE']}"
            )

            st.write(
                f"**Valor:** R$ {row['VALOR']:,.2f}"
                if isinstance(row["VALOR"], (int, float))
                else f"**Valor:** {row['VALOR']}"
            )

            st.write(f"**Margem:** {row['MARGEM']}")
