import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Consulta de Estoque", page_icon="🚗")

# Estilização Visual
st.markdown("""
    <style>
    .stApp { background-color: #2b59b4; color: white; }
    .stButton>button { 
        background-color: #f1d064; 
        color: #1e3d7d; 
        font-weight: bold; 
        border-radius: 5px; 
        width: 100%; 
    }
    h1, h3 { color: white; }
    label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 Consulta de Estoque")

# 1. Área de Upload (Fica discreta)
uploaded_file = st.file_uploader("Selecione a planilha", type=["xlsx"], label_visibility="collapsed")

# 2. Campo de Pesquisa
st.subheader("DIGITE A PLACA")
placa_input = st.text_input("Ex: ABC1D23", "").upper().strip()

# Botão de Pesquisa
if st.button("PESQUISAR"):
    if uploaded_file is not None:
        try:
            # Carrega a planilha
            df = pd.read_excel(uploaded_file)
            
            # Limpa nomes de colunas (tira espaços extras)
            df.columns = df.columns.str.strip()
            
            # Converte a coluna Placa para texto e busca
            df['Placa'] = df['Placa'].astype(str).str.strip().str.upper()
            resultado = df[df['Placa'] == placa_input]

            if not resultado.empty:
                row = resultado.iloc[0]
                
                st.markdown("---")
                # Exibição dos dados um embaixo do outro
                st.write(f"**Placa:** {row['Placa']}")
                st.write(f"**Modelo:** {row['Modelo']}")
                st.write(f"**Cor:** {row['Cor']}")
                st.write(f"**Ano:** {row['Ano']}")
                st.write(f"**KM:** {row['KM']}")
                
                # Formatação de valores (se for número, coloca R$. Se for texto, exibe direto)
                fipe = row['Valor FIPE']
                st.write(f"**Valor FIPE:** R$ {fipe:,.2f}" if isinstance(fipe, (int, float)) else f"**Valor FIPE:** {fipe}")
                
                valor = row['VALOR']
                st.write(f"**Valor:** R$ {valor:,.2f}" if isinstance(valor, (int, float)) else f"**Valor:** {valor}")
                
                st.write(f"**Margem:** {row['MARGEM']}")
            else:
                st.error("Placa não encontrada.")
        except Exception as e:
            st.error(f"Erro ao ler planilha: Verifique se as colunas estão corretas.")
    else:
        st.warning("Por favor, faça o upload do arquivo Excel primeiro.")
