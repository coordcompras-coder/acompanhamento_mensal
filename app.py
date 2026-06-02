import streamlit as st
import pandas as pd
import os
import plotly.express as px
import requests
from io import BytesIO
from PIL import Image

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit)
# ==============================================================================
st.set_page_config(
    page_title="Dashboard Corporativo de Gastos 2026",
    layout="wide",
    page_icon="📊"
)

# ==============================================================================
# DADOS DE USUÁRIOS E SEGURANÇA
# ==============================================================================
USUARIOS = {
    "admin": {"senha": "admin2026", "acesso": ["PR", "DG", "DE", "DC", "DO"]},
    "pr": {"senha": "pr2026", "acesso": ["PR", "DG", "DE", "DC", "DO"]},
    "dg": {"senha": "dg2026*", "acesso": ["DG"]},
    "dc": {"senha": "dc*2026", "acesso": ["DC"]},
    "de": {"senha": "*de2026", "acesso": ["DE"]},
    "do": {"senha": "do2026#", "acesso": ["DO"]}
}

# Inicialização do estado da sessão
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
if 'diretorias' not in st.session_state:
    st.session_state.diretorias = []

# ==============================================================================
# ESTILIZAÇÃO PROFISSIONAL (CSS)
# ==============================================================================
st.markdown("""
<style>

/* =========================================================
   IMPORTAÇÃO DE FONTE
========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

/* =========================================================
   FONTE GLOBAL
========================================================= */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* =========================================================
   FUNDO PRINCIPAL
========================================================= */
.stApp {
    background-color: #FFFFFF;
}

/* =========================================================
   TEXTOS GERAIS
========================================================= */
p, span, label, div {
    color: #000000;
}

/* =========================================================
   TÍTULOS
========================================================= */
h1, h2, h3, h4, h5, h6 {
    color: #0F172A !important;
    font-weight: 700 !important;
}

.main-title {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    border-left: 8px solid #89CFF0;
    padding-left: 1rem;
}

/* =========================================================
   SIDEBAR
========================================================= */
[data-testid="stSidebar"] {
    background-color: #F1F5F9;
    border-right: 1px solid #E2E8F0;
}

/* textos sidebar */
[data-testid="stSidebar"] * {
    color: #000000 !important;
}

/* seta recolher sidebar */
button[kind="header"] svg {
    fill: #000000 !important;
}

/* =========================================================
   TABS
========================================================= */

/* container tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background-color: #F1F5F9;
    padding: 10px;
    border-radius: 10px;
}

/* tabs normais */
.stTabs [data-baseweb="tab"] {
    background-color: #D9EEF7;
    color: #000000 !important;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    border: none;
}

/* hover */
.stTabs [data-baseweb="tab"]:hover {
    background-color: #89CFF0;
    color: #000000 !important;
}

/* tab ativa */
.stTabs [aria-selected="true"] {
    background-color: #1CACEF !important;
    color: #FFFFFF !important;
}

/* =========================================================
   BOTÕES
========================================================= */
.stButton>button {
    background-color: #89CFF0;
    color: #000000 !important;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    padding: 0.5rem 2rem;
    transition: all 0.3s;
}

.stButton>button:hover {
    background-color: #5fbce9;
    box-shadow: 0 4px 12px rgba(137, 207, 240, 0.4);
}

/* =========================================================
   INPUTS LOGIN
========================================================= */

/* labels */
.stTextInput label {
    color: #000000 !important;
    font-weight: 600;
}

/* input */
.stTextInput input {
    color: #000000 !important;
    background-color: #FFFFFF !important;
}

/* placeholder */
.stTextInput input::placeholder {
    color: #6B7280 !important;
}

/* borda */
.stTextInput div[data-baseweb="input"] {
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    background-color: #FFFFFF !important;
}

/* senha */
input[type="password"] {
    color: #000000 !important;
    background-color: #FFFFFF !important;
}

/* =========================================================
   MÉTRICAS
========================================================= */
[data-testid="stMetric"] {
    background: #E2E8F0;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 20px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

[data-testid="stMetricValue"] {
    color: #000000 !important;
    font-weight: 700 !important;
    font-size: 15px !important;   /* VALOR PRINCIPAL VALOR DOS CARDS*/
}

/* =========================================================
   DATAFRAMES / TABELAS
========================================================= */

/* tabela geral */
[data-testid="stDataFrame"] {
    background-color: #F0F8FF !important;
    border-radius: 10px;
    padding: 5px;
}

/* cabeçalho */
[data-testid="stDataFrame"] thead tr th {
    background-color: #F4FBFE !important;
    color: #1F2937 !important;
    font-weight: bold !important;
    text-align: center !important;
}

/* corpo */
[data-testid="stDataFrame"] tbody tr td {
    background-color: #EAF6FB !important;
    color: #1F2937 !important;
    text-align: center !important;
}

/* grid interno */
div[data-testid="stDataFrame"] div[role="grid"] div[role="columnheader"] {
    background-color: #E1F5FE !important;
    color: #000000 !important;
    font-weight: bold !important;
}

div[data-testid="stDataFrame"] div[role="grid"] div[role="gridcell"] {
    color: #000000 !important;
}

/* =========================================================
   TEXTOS STREAMLIT
========================================================= */

/* st.write */
.stMarkdown p {
    color: #000000 !important;
}

/* caption */
[data-testid="stCaptionContainer"] {
    color: #000000 !important;
}

/* info */
[data-testid="stAlert"] {
    color: #000000 !important;
}

/* =========================================================
   EXPANDERS
========================================================= */
.streamlit-expanderHeader {
    color: #000000 !important;
    font-weight: 600;
}

/* =========================================================
   SELECTBOX
========================================================= */
.stSelectbox label {
    color: #000000 !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* =========================================================
   MULTISELECT
========================================================= */
.stMultiSelect label {
    color: #000000 !important;
}

/* =========================================================
   RADIO
========================================================= */
.stRadio label {
    color: #000000 !important;
}

/* =========================================================
   CHECKBOX
========================================================= */
.stCheckbox label {
    color: #000000 !important;
}

/* =========================================================
   SCROLLBAR
========================================================= */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #F1F5F9;
}

::-webkit-scrollbar-thumb {
    background: #89CFF0;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #1CACEF;
}

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNÇÕES UTILITÁRIAS
# ==============================================================================
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==============================================================================
# TELA DE LOGIN
# ==============================================================================
if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Tentar carregar logo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "icon", "imagem_caema.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=300)
        
        st.markdown("### Acesso ao Sistema")
        with st.form("login_form"):
            user_input = st.text_input("Usuário")
            pass_input = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                if user_input in USUARIOS and pass_input == USUARIOS[user_input]["senha"]:
                    st.session_state.autenticado = True
                    st.session_state.usuario = user_input
                    st.session_state.diretorias = USUARIOS[user_input]["acesso"]
                    st.rerun()
                else:
                    st.error("Credenciais inválidas. Por favor, tente novamente.")
    st.stop()

# ==============================================================================
# DASHBOARD PRINCIPAL (Só acessível após login)
# ==============================================================================

# Barra lateral com informações do usuário e Logout
with st.sidebar:
    st.markdown(f"### Bem-vindo, **{st.session_state.usuario.upper()}**")
    st.markdown("---")
    if st.button("Sair do Sistema"):
        st.session_state.autenticado = False
        st.session_state.usuario = None
        st.rerun()

# Cabeçalho do Dashboard
# Logo acima do cabeçalho
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "icon", "imagem_caema.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=250)   # ajusta o tamanho conforme preferir

st.markdown('<h1 class="main-title">ACOMPANHAMENTO DE GASTOS PREVISTOS E NÃO PREVISTOS 2026</h1>', unsafe_allow_html=True)

# ================== CARREGAR EXCEL ==================
# caminho_excel = "https://docs.google.com/spreadsheets/d/1seIaYVZ1D06jPZm9O7yzXbW8hi8tgV2OzBHguyNrfMY/export?format=xlsx"


# df_previsto = pd.read_excel(caminho_excel, sheet_name="previsto")
# df_realizado = pd.read_excel(caminho_excel, sheet_name="realizado")
# df_orcamento = pd.read_excel(caminho_excel, sheet_name="orcamento")

#OBS: EU VOU DEIXAR ESSE CÓDIGO COMENTADO POIS É O ORIGINAL. POREM VOU MUDAR PORQUE DEU UM PEQUENO PROBLEMA COM CACHÊ. SE FICAR IGUAL EU VOU VOLTAR PARA ESSE. HOJE É 19/05/2026 AS 08:53


# ================== CARREGAR EXCEL ================== ADICIONEI OS 2 ULTIMOS IMPORTS LÁ EM CIMA POR ESSE TRECHO

URL_EXCEL = "https://docs.google.com/spreadsheets/d/1seIaYVZ1D06jPZm9O7yzXbW8hi8tgV2OzBHguyNrfMY/export?format=xlsx"

@st.cache_data(ttl=300)
def carregar_dados():

    response = requests.get(URL_EXCEL)

    if response.status_code != 200:
        st.error("Erro ao carregar a planilha.")
        st.stop()

    arquivo_excel = BytesIO(response.content)

    df_previsto = pd.read_excel(arquivo_excel, sheet_name="previsto")

    # precisa reposicionar o ponteiro
    arquivo_excel.seek(0)
    df_realizado = pd.read_excel(arquivo_excel, sheet_name="realizado")

    arquivo_excel.seek(0)
    df_orcamento = pd.read_excel(arquivo_excel, sheet_name="orcamento")

    return df_previsto, df_realizado, df_orcamento

df_previsto, df_realizado, df_orcamento = carregar_dados()


#ESSE TRECHO ESTÁ EM TESTE PARA VER SE É MELHOR 19/05/2026


# ================== PADRONIZAÇÃO ==================
df_previsto.columns = df_previsto.columns.str.upper().str.strip()
df_realizado.columns = df_realizado.columns.str.upper().str.strip()
df_orcamento.columns = df_orcamento.columns.str.upper().str.strip()

# ================== TRATAMENTO DE DATA ==================
df_realizado["DATA"] = pd.to_datetime(df_realizado["DATA"], errors="coerce")

# Número do mês (ordem)
df_realizado["MES_NUM"] = df_realizado["DATA"].dt.month

# Nome do mês
df_realizado["MES_NOME"] = df_realizado["DATA"].dt.strftime("%b")

# Traduzir para PT-BR
mapa_meses = {
    "Jan": "Jan", "Feb": "Fev", "Mar": "Mar", "Apr": "Abr",
    "May": "Mai", "Jun": "Jun", "Jul": "Jul", "Aug": "Ago",
    "Sep": "Set", "Oct": "Out", "Nov": "Nov", "Dec": "Dez"
}

df_realizado["MES_NOME"] = df_realizado["MES_NOME"].map(mapa_meses)

# ================== PALETA AZUL BEBÊ ==================
# Cor de fundo dos gráficos: azul bebê suave
GRAPH_BG = "rgba(209,223,230,0.30)"
# Cor das barras/linhas padrão: azul bebê médio
BABY_BLUE = "#1CACEF"
# Cor do texto dos gráficos: preto
FONT_COLOR = "#000000"

# ================== ABAS ==================
abas = ["Visão Geral"] + st.session_state.diretorias
tabs = st.tabs(abas)

# ================== DASHBOARD ==================
with tabs[0]:
    st.header("Dashboard Geral")

    # total = df_realizado["VALOR_OC"].sum()

    # servicos = df_realizado[df_realizado["TIPO"] == "SERVICO"]["VALOR_OC"].sum()
    # aquisicoes = df_realizado[df_realizado["TIPO"] == "AQUISICAO"]["VALOR_OC"].sum()

    # col1, col2, col3 = st.columns(3)

    # col1.metric("Total Geral", formatar_moeda(total))
    # col2.metric("Serviços", formatar_moeda(servicos))
    # col3.metric("Aquisições", formatar_moeda(aquisicoes))


        # NF Serviços
    nf_servicos = (
        df_realizado[df_realizado["TIPO"] == "SERVICO"]["VALOR_NF"]
        .sum()
    )

    # NF Aquisições
    nf_aquisicoes = (
        df_realizado[df_realizado["TIPO"] == "AQUISICAO"]["VALOR_NF"]
        .sum()
    )

    # Base apenas de AQUISIÇÃO
    df_aquisicao = df_realizado[
        df_realizado["TIPO"] == "AQUISICAO"
    ]

    # Quantidade de Ordens de Compra
    qtd_oc = df_aquisicao["OC"].nunique()

    # Quantidade de Fornecedores
    qtd_fornecedores = df_aquisicao["FORNECEDOR"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "NF Serviços",
        formatar_moeda(nf_servicos)
    )

    col2.metric(
        "NF Aquisições",
        formatar_moeda(nf_aquisicoes)
    )

    col3.metric(
        "Qtd. Ordens de Compra",
        f"{qtd_oc:,}".replace(",", ".")
    )

    col4.metric(
        "Qtd. Fornecedores",
        f"{qtd_fornecedores:,}".replace(",", ".")
    )



#========graficos de linha por diretoria========
    st.markdown("---")
#AQUISIÇÃO LINHA POR DIRETORIA
    st.subheader("Evolução Mensal - Aquisições por Diretoria")

    df_aq = df_realizado[df_realizado["TIPO"] == "AQUISICAO"]

    df_aq_mensal = (
        df_aq.groupby(["MES_NUM", "MES_NOME", "DIRETORIA"])["VALOR_OC"]
        .sum()
        .reset_index()
        .sort_values("MES_NUM")
    )

    fig_aq = px.line(
        df_aq_mensal,
        x="MES_NOME",
        y="VALOR_OC",
        color="DIRETORIA",
        markers=True,
        color_discrete_map={
            "PR": "#103749",
            "DG": "#15DDDA",
            "DE": "#E6AF15",
            "DC": "#7D1AB7",
            "DO": "#0D562E"
        }
    )

    fig_aq.update_traces(
        line_shape="spline", # suaviza as linhas,  line=dict(width=4) deixa as linhas mais grossas, dash="dash" deixa tracejada, 
        hovertemplate="R$ %{y:,.2s}"
    )

    fig_aq.update_layout(
        yaxis=dict(
            tickprefix="R$ ",
            tickformat=",.2s", # .2f  mostra valores completos com 2 casas decimais, || .0f mostra valores arredondados sem casas decimais  || ",.2s"    # reduzido (k, M, B) || ",.2%"    # porcentagem || ",.2e"    # notação científica  
            separatethousands=True,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        xaxis=dict(
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        separators=",.",
        plot_bgcolor=GRAPH_BG,
        paper_bgcolor=GRAPH_BG,
        font=dict(color=FONT_COLOR),
        legend=dict(font=dict(color=FONT_COLOR))
    )

    st.plotly_chart(fig_aq, use_container_width=True, key="linha_aquisicao_dir")


    st.markdown("---")
#SERVIÇOS LINHA POR DIRETORIA
    st.subheader("Evolução Mensal - Serviços Pagos por Diretoria")

    df_sv = df_realizado[df_realizado["TIPO"] == "SERVICO"]

    df_sv_mensal = (
        df_sv.groupby(["MES_NUM", "MES_NOME", "DIRETORIA"])["VALOR_NF"]
        .sum()
        .reset_index()
        .sort_values("MES_NUM")
    )

    fig_sv = px.line(
        df_sv_mensal,
        x="MES_NOME",
        y="VALOR_NF",
        color="DIRETORIA",
        markers=True,
        color_discrete_map={
            "PR": "#103749",
            "DG": "#15DDDA",
            "DE": "#E6AF15",
            "DC": "#7D1AB7",
            "DO": "#0D562E"
        }
    )

    fig_sv.update_traces(
        line_shape="spline",
        hovertemplate="R$ %{y:,.2s}"
    )

    fig_sv.update_layout(
        yaxis=dict(
            tickprefix="R$ ",
            tickformat=",.2s", # .2f  mostra valores completos com 2 casas decimais, || .0f mostra valores arredondados sem casas decimais  || ",.2s"    # reduzido (k, M, B) || ",.2%"    # porcentagem || ",.2e"    # notação científica
            separatethousands=True,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        xaxis=dict(
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        separators=",.",
        plot_bgcolor=GRAPH_BG,
        paper_bgcolor=GRAPH_BG,
        font=dict(color=FONT_COLOR),
        legend=dict(font=dict(color=FONT_COLOR))
    )

    st.plotly_chart(fig_sv, use_container_width=True, key="linha_servico_dir")


    st.markdown("---")
#DISTRIBUIÇÃO POR CLASSIFICAÇÃO
    st.subheader(" Distribuição por Classificação %")
    df_class = (
        df_realizado[df_realizado["TIPO"] == "AQUISICAO"]
        .groupby("CLASSIFICACAO")["VALOR_OC"]
        .sum()
        .reset_index()
        .sort_values("VALOR_OC", ascending=False)
    )

    # ================== PIZZA (TOP 6) ==================
    df_pizza = df_class.head(6)

    fig = px.pie(
        df_pizza,
        names="CLASSIFICACAO",
        values="VALOR_OC",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        insidetextfont=dict(
            color='white',
            size=14
        )
    )

    fig.update_layout(
        plot_bgcolor=GRAPH_BG,
        paper_bgcolor=GRAPH_BG,
        font=dict(color=FONT_COLOR),
        legend=dict(font=dict(color=FONT_COLOR))
    )

    st.plotly_chart(fig, use_container_width=True)
 

    st.markdown("---")


    # ================== BARRAS (TOP 10) ==================
    st.subheader("Top 10 Classificações")

    df_bar = df_class.head(10)

    fig_bar = px.bar(
        df_bar,
        x="VALOR_OC",
        y="CLASSIFICACAO",
        orientation="h",
        text="VALOR_OC",
        color_discrete_sequence=[BABY_BLUE]
    )

    fig_bar.update_traces(
        texttemplate="R$ %{text:,.2s}",
        textposition="auto",
        textfont=dict(color=FONT_COLOR)
    )

    fig_bar.update_layout(
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        xaxis=dict(
            tickprefix="R$ ",
            tickformat=",.2s",
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        separators=".,",
        plot_bgcolor=GRAPH_BG,
        paper_bgcolor=GRAPH_BG,
        font=dict(color=FONT_COLOR)
    )

    st.plotly_chart(fig_bar, use_container_width=True)




#TOP GERÊNCIAS QUE MAIS GASTAM
    st.subheader("TOP 10 GERÊNCIAS QUE MAIS GASTAM")
    df_ger = (
        df_realizado[df_realizado["TIPO"] == "AQUISICAO"]
        .groupby("GERENCIA")["VALOR_OC"]
        .sum()
        .reset_index()
        .sort_values("VALOR_OC", ascending=False)
        .head(10)
    )

    fig = px.bar(
        df_ger,
        x="VALOR_OC",
        y="GERENCIA",
        orientation="h",
        text="VALOR_OC",
        color_discrete_sequence=[BABY_BLUE]
    )

    fig.update_traces(
        texttemplate="R$ %{text:,.2s}",
        textposition="auto",
        textfont=dict(color=FONT_COLOR)
    )

    fig.update_layout(
        yaxis=dict(
            autorange="reversed",
            separatethousands=True,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        xaxis=dict(
            tickprefix="R$ ",
            tickformat=",.2s",
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        separators=",.",
        plot_bgcolor=GRAPH_BG,
        paper_bgcolor=GRAPH_BG,
        font=dict(color=FONT_COLOR),
        legend=dict(font=dict(color=FONT_COLOR))
    )

    st.plotly_chart(fig, use_container_width=True)


    st.markdown("---")


    #TOP 10 FORNECEDORES
    st.subheader("TOP 10 FORNECEDORES")
    df_ger = (
        df_realizado[df_realizado["TIPO"] == "AQUISICAO"]
        .groupby("FORNECEDOR")["VALOR_OC"]
        .sum()
        .reset_index()
        .sort_values("VALOR_OC", ascending=False)
        .head(10)
    )

    fig = px.bar(
        df_ger,
        x="VALOR_OC",
        y="FORNECEDOR",
        orientation="h",
        text="VALOR_OC",
        color_discrete_sequence=[BABY_BLUE]
    )

    fig.update_traces(
        texttemplate="R$ %{text:,.2s}",
        textposition="auto",
        textfont=dict(color=FONT_COLOR)
    )

    fig.update_layout(
        yaxis=dict(
            autorange="reversed",
            separatethousands=True,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        xaxis=dict(
            tickprefix="R$ ",
            tickformat=",.2s",
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        separators=",.",
            plot_bgcolor=GRAPH_BG,
            paper_bgcolor=GRAPH_BG,
            font=dict(color=FONT_COLOR),
            legend=dict(font=dict(color=FONT_COLOR))
        )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")






#REALIZADO vs NÃO PREVISTO (impacto)
    st.subheader("REALIZADO vs NÃO PREVISTO (Aquisição)")
    df_prev = (
    df_realizado.groupby("PREVISTO")["VALOR_OC"]
    .sum()
    .reset_index()
)
    fig = px.bar(
        df_prev,
        x="PREVISTO",
        y="VALOR_OC",
        color="PREVISTO",
        text="VALOR_OC",
        color_discrete_map={
        "SIM": "#62afe3",   # 
        "NAO": "#1090e6"    # 
    }
    )

    fig.update_traces(
        texttemplate="R$ %{text:,.2f}",
        textposition="inside", #outside
        textfont=dict(color=FONT_COLOR)
    )

    fig.update_layout(
        yaxis=dict(
            tickprefix="R$ ",
            tickformat=",.2f",
            separatethousands=True,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        xaxis=dict(
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        separators=",.",
        plot_bgcolor=GRAPH_BG,
        paper_bgcolor=GRAPH_BG,
        font=dict(color=FONT_COLOR),
        legend=dict(font=dict(color=FONT_COLOR))
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

#AQUISIÇÃO vs SERVIÇO AO LONGO DO TEMPO
    st.subheader("AQUISIÇÃO vs SERVIÇO AO LONGO DO TEMPO")
    df_tipo = (
    df_realizado.groupby(["MES_NUM", "MES_NOME", "TIPO"])["VALOR_NF"]
    .sum()
    .reset_index()
    .sort_values("MES_NUM")
)

    fig = px.line(
        df_tipo,
        x="MES_NOME",
        y="VALOR_NF",
        color="TIPO",
        markers=True,
        color_discrete_map={
            "AQUISICAO": "#031521",  # azul petróleo#0B3C5D
            "SERVICO": "#1CACEF"     # azul bebê
        }
    )

    fig.update_traces(line_shape="spline")
    fig.update_layout(
        plot_bgcolor=GRAPH_BG,
        paper_bgcolor=GRAPH_BG,
        font=dict(color=FONT_COLOR),
        legend=dict(font=dict(color=FONT_COLOR)),
        yaxis=dict(
            tickprefix="R$ ",
            tickformat=",.2s",
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        xaxis=dict(
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        separators=",."
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

#OC vs NF (controle financeiro)

    st.subheader("OC vs NF (Aquisição) por Diretoria vs Orçamento")

    # FILTRAR APENAS AQUISIÇÃO
    df_aq = df_realizado[df_realizado["TIPO"] == "AQUISICAO"]

    # AGRUPAR OC e NF
    df_oc_nf = (
        df_aq.groupby("DIRETORIA")[["VALOR_OC", "VALOR_NF"]]
        .sum()
        .reset_index()
    )

    # ORÇAMENTO (já é aquisição)
    df_orc = (
        df_orcamento.groupby("DIRETORIA")["ORCAMENTO_AQUISICAO"]
        .sum()
        .reset_index()
    )

    # MERGE
    df_final = df_oc_nf.merge(df_orc, on="DIRETORIA", how="left")

    # GRÁFICO DE BARRAS
    fig = px.bar(
        df_final,
        x="DIRETORIA",
        y=["VALOR_OC", "VALOR_NF"],
        barmode="group",
        text_auto=True,
        #color_discrete_sequence=px.colors.sequential.Blues_r
    )

    # CORES DAS BARRAS
    fig.for_each_trace(
        lambda t: t.update(
            marker_color=
            "#0B3C5D" if t.name == "VALOR_OC"
            else "#1CACEF"
        )
    )

    # TEXTO FORA DA BARRA
    fig.update_traces(
        texttemplate="R$ %{y:,.2s}",
        textposition="outside",
        textfont=dict(color=FONT_COLOR)
    )

    # LINHA DE ORÇAMENTO (SUAVE)
    fig.add_scatter(
        x=df_final["DIRETORIA"],
        y=df_final["ORCAMENTO_AQUISICAO"],
        mode="lines+markers",
        name="Orçamento Aquisição",
        line=dict(
            shape="spline",
            dash="solid",
            color="red",
            width=3
        )
    )

    # FORMATAÇÃO
    fig.update_layout(
        yaxis=dict(
            tickprefix="R$ ",
            tickformat=",.2s",
            separatethousands=True,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        xaxis=dict(
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR)
        ),
        separators=",.",
        plot_bgcolor=GRAPH_BG,
        paper_bgcolor=GRAPH_BG,
        font=dict(color=FONT_COLOR),
        legend=dict(font=dict(color=FONT_COLOR))
    )

    st.plotly_chart(fig, use_container_width=True)

    #tabela de conferencia entre OC e NF
    # ================== TABELA CONFERÊNCIA ==================
    st.subheader("Conferência: Orçado vs Realizado por Diretoria")

    df_conf = (
        df_realizado[df_realizado["TIPO"] == "AQUISICAO"]
        .groupby("DIRETORIA")["VALOR_OC"]
        .sum()
        .reset_index()
    )

    df_conf = df_conf.merge(
        df_orcamento[["DIRETORIA", "ORCAMENTO_AQUISICAO"]],
        on="DIRETORIA",
        how="left"
    )

    # ================== SALDO ==================
    df_conf["SALDO_RESTANTE"] = (
        df_conf["ORCAMENTO_AQUISICAO"] - df_conf["VALOR_OC"]
    )

    # ================== FUNÇÃO DE COR ==================
    def cor_saldo(row):

        saldo = row["SALDO_RESTANTE"]
        orcamento = row["ORCAMENTO_AQUISICAO"]

        estilos = [''] * len(row)

        col_idx = row.index.get_loc("SALDO_RESTANTE")

        # 🔴 passou orçamento
        if saldo < 0:
            estilos[col_idx] = (
                'background-color: #FECACA; '
                'color: #991B1B; '
                'font-weight: bold'
            )

        # 🟡 próximo do limite
        elif saldo <= (orcamento * 0.30):
            estilos[col_idx] = (
                'background-color: #FEF3C7; '
                'color: #92400E; '
                'font-weight: bold'
            )

        # 🟢 saudável
        else:
            estilos[col_idx] = (
                'background-color: #DCFCE7; '
                'color: #166534; '
                'font-weight: bold'
            )

        return estilos


    # ================== STYLE DATAFRAME ==================
    styled_df = (
        df_conf[[
            "DIRETORIA",
            "VALOR_OC",
            "ORCAMENTO_AQUISICAO",
            "SALDO_RESTANTE"
        ]]
        .style
        .format({
            "VALOR_OC": "R$ {:,.2f}",
            "ORCAMENTO_AQUISICAO": "R$ {:,.2f}",
            "SALDO_RESTANTE": "R$ {:,.2f}"
        })
        .set_properties(**{
            "background-color": "#EAF6FB",
            "color": "#062D3C",
            "border-color": "#D6EAF2",
            "text-align": "center"
        })
        .apply(cor_saldo, axis=1)
    )

    # ================== EXIBIÇÃO ==================
    st.dataframe(
        styled_df,
        use_container_width=True
    )

    st.write("🔎 Se o saldo restante for negativo, significa que a diretoria já estourou o orçamento.")
    st.caption("📌 Este relatório considera apenas dados de AQUISIÇÃO")
    st.markdown("---")

  
    # ================== INSIGHTS MENSAIS ==================
    st.subheader("Insights Mensais")

    # Agrupa por mês
    df_mensal = (
        df_realizado
        .groupby(["MES_NUM", "MES_NOME"])["VALOR_OC"]
        .sum()
        .reset_index()
        .sort_values("MES_NUM")
    )

    insights = []

    for _, row in df_mensal.iterrows():

        mes = row["MES_NOME"]

        # Filtra dados do mês
        df_mes = df_realizado[df_realizado["MES_NOME"] == mes]

        # Total gasto no mês
        total_mes = df_mes["VALOR_OC"].sum()

        # ==============================
        # DIRETORIA QUE MAIS GASTOU
        # ==============================
        top_dir = (
            df_mes.groupby("DIRETORIA")["VALOR_OC"]
            .sum()
            .sort_values(ascending=False)
        )

        diretoria_top = top_dir.index[0]

        # ==============================
        # CLASSIFICAÇÃO QUE MAIS GASTOU
        # ==============================
        top_class = (
            df_mes.groupby("CLASSIFICACAO")["VALOR_OC"]
            .sum()
            .sort_values(ascending=False)
        )

        class_top = top_class.index[0]

        # ==============================
        # LISTA FINAL
        # ==============================
        insights.append({
            "MÊS": mes,
            "DIRETORIA QUE MAIS GASTOU": diretoria_top,
            "VALOR TOTAL GASTO": formatar_moeda(total_mes),
            "CLASSIFICAÇÃO QUE MAIS GASTOU": class_top
        })

    # DataFrame final
    df_insights = pd.DataFrame(insights)

    # Exibição
    st.dataframe(
        df_insights.style
        .set_properties(**{
            "background-color": "#EAF6FB",
            "color": "#1F2937",
            "border-color": "#D6EAF2",
            "text-align": "center"
        }),
        use_container_width=True
    )


# ================== LOOP ==================
for i, diretoria in enumerate(st.session_state.diretorias):


    with tabs[i + 1]:  # +1 porque a primeira aba é o dashboard geral
        st.header(f" Diretoria {diretoria}")

        # FILTROS
        prev = df_previsto[df_previsto["DIRETORIA"] == diretoria]
        real = df_realizado[
            (df_realizado["DIRETORIA"] == diretoria) &
            (df_realizado["TIPO"] == "AQUISICAO")
        ]
        orc = df_orcamento[df_orcamento["DIRETORIA"] == diretoria]

        # ================== CÁLCULOS ==================
        # Quantidade de OCs da diretoria
        qtd_oc = real["OC"].dropna().nunique()
        orc_aquisicao = orc["ORCAMENTO_AQUISICAO"].sum()

        realizado_total = real["VALOR_OC"].sum()
        realizado_previsto = real[real["PREVISTO"] == "SIM"]["VALOR_OC"].sum()
        nao_previsto = real[real["PREVISTO"] == "NAO"]["VALOR_OC"].sum()

        # ================== KPIs ==================
        st.subheader("Indicadores")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Orçamento Aquisição", formatar_moeda(orc_aquisicao))
        col2.metric("Realizado", formatar_moeda(realizado_total))
        col3.metric("Não Previsto", formatar_moeda(nao_previsto))
        col4.metric("Qtd. Ordens de Compra", f"{qtd_oc:,}".replace(",", "."))

        st.markdown("---")

        # ================== GRÁFICO BARRAS ==================
        st.subheader("Comparativo")

        df_grafico = pd.DataFrame({
            "Categoria": ["Orçamento", "Realizado Previsto", "Não Previsto"],
            "Valor": [orc_aquisicao, realizado_previsto, nao_previsto]
        })

        fig_bar = px.bar(
            df_grafico,
            x="Categoria",
            y="Valor",
            text="Valor",
            color="Categoria",
            color_discrete_map={
                "Orçamento": "#5DADE2",          # Azul claro 
                "Realizado Previsto": "#063432", # azul escuro
                "Não Previsto": "#d94557"       # vermelho
            }
        )

        fig_bar.update_traces(
            texttemplate="R$ %{y:,.2f}",
            textposition="outside",
            textfont=dict(color=FONT_COLOR)
        )

        fig_bar.update_layout(
            yaxis=dict(
                tickprefix="R$ ",
                tickformat=",.2f",
                separatethousands=True,
                tickfont=dict(color=FONT_COLOR),
                title_font=dict(color=FONT_COLOR)
            ),
            xaxis=dict(
                tickfont=dict(color=FONT_COLOR),
                title_font=dict(color=FONT_COLOR)
            ),
            separators=",.",
            plot_bgcolor=GRAPH_BG,
            paper_bgcolor=GRAPH_BG,
            font=dict(color=FONT_COLOR),
            legend=dict(font=dict(color=FONT_COLOR))
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        # ================== GRÁFICO LINHA ==================
        st.subheader("Evolução Mensal")

        df_linha = (
            real.groupby(["MES_NUM", "MES_NOME", "PREVISTO"])["VALOR_OC"]
            .sum()
            .reset_index()
            .sort_values("MES_NUM")
        )

        fig_linha = px.line(
            df_linha,
            x="MES_NOME",
            y="VALOR_OC",
            color="PREVISTO",
            markers=True,
             category_orders={
                "MES_NOME": [
                    "Jan", "Fev", "Mar", "Abr",
                    "Mai", "Jun", "Jul", "Ago",
                    "Set", "Out", "Nov", "Dez"
                ]
            },                                                               
            color_discrete_map={
                "SIM": "#0F4A07",   # verde
                "NAO": "#C61313"    # vermelho
            }
        )

        fig_linha.update_traces(
            line_shape="spline",
            texttemplate="R$ %{y:,.0f}",
            hovertemplate="R$ %{y:,.2f}"
        )

        fig_linha.update_layout(
            yaxis=dict(
                tickprefix="R$ ",
                tickformat=",.2s",
                separatethousands=True,
                tickfont=dict(color=FONT_COLOR),
                title_font=dict(color=FONT_COLOR)
            ),
            xaxis=dict(
                tickfont=dict(color=FONT_COLOR),
                title_font=dict(color=FONT_COLOR)
            ),
            separators=",.",
            plot_bgcolor=GRAPH_BG,
            paper_bgcolor=GRAPH_BG,
            font=dict(color=FONT_COLOR),
            legend=dict(font=dict(color=FONT_COLOR))
        )

        fig_linha.update_yaxes(
            tickprefix="R$ ",
            separatethousands=True
        )

        st.plotly_chart(fig_linha, use_container_width=True)

        st.markdown("---")

        # ================== TABELA MENSAL ==================
        st.subheader("Realizado por Mês")

        tabela_mensal = (
            real[real["PREVISTO"] == "SIM"]
            .groupby(["MES_NUM", "MES_NOME"])["VALOR_OC"]
            .sum()
            .reset_index()
            .sort_values("MES_NUM")
        )
        
        
        st.dataframe(
            tabela_mensal[["MES_NOME", "VALOR_OC"]]
            .style
            .format({
                "VALOR_OC": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            })
            .set_properties(**{
                "background-color": "#EAF6FB",
                "color": "#1F2937",
                "border-color": "#D6EAF2",
                "text-align": "center"
            }),
            use_container_width=True
        )
        

        st.markdown("---")

        # ================== TABELA NÃO PREVISTO ==================
        st.subheader("Não Previsto")

        tabela_nao_previsto = real[real["PREVISTO"] == "NAO"]

        st.dataframe(
        tabela_nao_previsto[["GERENCIA", "DESCRICAO", "TIPO", "VALOR_OC"]]
        .style
        .format({ "VALOR_OC": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")})
        .set_properties(**{
            "background-color": "#FDEDEC",
            "color": "#C53030",
            "border-color": "#F5C6CB",
            "text-align": "center"
        }),
        use_container_width=True
    )
        

        # ================== TABELA DETALHAMENTO POR MÊS ==================

        st.markdown("---")

        st.subheader("Compras por Mês (Detalhado)")

        tabela_total = (
            real[["MES_NUM", "MES_NOME", "DESCRICAO", "VALOR_OC"]]
            .sort_values(["MES_NUM", "DESCRICAO"])
        )

        st.dataframe(
            tabela_total[["MES_NOME", "DESCRICAO", "VALOR_OC"]]
            .style
            .format({ "VALOR_OC": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")})
            .set_properties(**{
                "background-color": "#EAF6FB",
                "color": "#09242B",
                "border-color": "#D6EAF2",
                "text-align": "center"
            }),
            use_container_width=True
        )


st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #000000;'>"
    "Sistema conectado ao Excel | Atualização automática de dados"
    "</div>",
    unsafe_allow_html=True
)