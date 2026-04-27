import streamlit as st
import pandas as pd
import os
import plotly.express as px


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")



# CONFIGURAÇÃO
st.set_page_config(
    page_title="Dashboard de Compras e Serviços",
    layout="wide",
    page_icon="icon/tendencia.png"
)

# LOGO
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "icon", "imagem_caema.png")
st.image(logo_path, width=300)

st.title("📊 ACOMPANHAMENTO DE GASTOS PREVISTOS E NÃO PREVISTOS 2026")

# ================== CARREGAR EXCEL ==================
caminho_excel = "https://docs.google.com/spreadsheets/d/1TiTr8mzVnE0baK3vsctaYWdBVZ6A1FHi/export?format=xlsx"

df_previsto = pd.read_excel(caminho_excel, sheet_name="previsto")
df_realizado = pd.read_excel(caminho_excel, sheet_name="realizado")
df_orcamento = pd.read_excel(caminho_excel, sheet_name="orcamento")

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

# ================== ABAS ==================
diretorias = ["PR", "DG", "DE", "DC", "DO"]
tabs = st.tabs(diretorias)

# ================== LOOP ==================
for i, diretoria in enumerate(diretorias):

    with tabs[i]:
        st.header(f"📊 Diretoria {diretoria}")

        # FILTROS
        prev = df_previsto[df_previsto["DIRETORIA"] == diretoria]
        real = df_realizado[df_realizado["DIRETORIA"] == diretoria]
        orc = df_orcamento[df_orcamento["DIRETORIA"] == diretoria]

        # ================== CÁLCULOS ==================
        orc_aquisicao = orc["ORCAMENTO_AQUISICAO"].sum()

        realizado_total = real["VALOR_REAL"].sum()
        realizado_previsto = real[real["PREVISTO"] == "SIM"]["VALOR_REAL"].sum()
        nao_previsto = real[real["PREVISTO"] == "NAO"]["VALOR_REAL"].sum()

        # ================== KPIs ==================
        st.subheader("📊 Indicadores")

        col1, col2, col3 = st.columns(3)


        col1.metric("Orçamento Aquisição", formatar_moeda(orc_aquisicao))
        col2.metric("Realizado", formatar_moeda(realizado_total))
        col3.metric("Não Previsto", formatar_moeda(nao_previsto))

        st.markdown("---")

        # ================== GRÁFICO BARRAS ==================
        st.subheader("📈 Comparativo")

        df_grafico = pd.DataFrame({
            "Categoria": ["Orçamento", "Realizado Previsto", "Não Previsto"],
            "Valor": [orc_aquisicao, realizado_previsto, nao_previsto]
        })

        fig_bar = px.bar(
            df_grafico,
            x="Categoria",
            y="Valor",
            text="Valor",
            color="Categoria"
        )

        fig_bar.update_traces(
            texttemplate="R$ %{y:,.2f}",
            textposition="outside"
        )

        fig_bar.update_layout(
            yaxis_tickprefix="R$ ",
            yaxis_tickformat=",.2f"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        # ================== GRÁFICO LINHA ==================
        st.subheader("📈 Evolução Mensal")

        df_linha = (
            real.groupby(["MES_NUM", "MES_NOME", "PREVISTO"])["VALOR_REAL"]
            .sum()
            .reset_index()
            .sort_values("MES_NUM")
        )

        fig_linha = px.line(
            df_linha,
            x="MES_NOME",
            y="VALOR_REAL",
            color="PREVISTO",
            markers=True,
            color_discrete_map={
                "SIM": "#00FFAA",   # verde
                "NAO": "#FF4B4B"    # vermelho
            }
        )

        fig_linha.update_traces(
            line_shape="spline",
            texttemplate="R$ %{y:,.0f}",
            hovertemplate="R$ %{y:,.2f}"
        )

        fig_linha.update_layout(
            yaxis_tickprefix="R$ ",
            yaxis_tickformat=",.2f"
        )

        fig_linha.update_yaxes(
            tickprefix="R$ ",
            separatethousands=True
        )        

        st.plotly_chart(fig_linha, use_container_width=True)

        st.markdown("---")

        # ================== TABELA MENSAL ==================
        st.subheader("📋 Realizado Previsto por Mês")

        tabela_mensal = (
            real[real["PREVISTO"] == "SIM"]
            .groupby(["MES_NUM", "MES_NOME"])["VALOR_REAL"]
            .sum()
            .reset_index()
            .sort_values("MES_NUM")
        )

        st.dataframe(
        tabela_mensal[["MES_NOME", "VALOR_REAL"]]
        .style.format({"VALOR_REAL": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}),
        use_container_width=True
        )

        st.markdown("---")

        # ================== TABELA NÃO PREVISTO ==================
        st.subheader("⚠️ Não Previsto")

        tabela_nao_previsto = real[real["PREVISTO"] == "NAO"]

        st.dataframe(
        tabela_nao_previsto[["GERENCIA", "DESCRICAO", "TIPO", "VALOR_REAL"]]
        .style.format({"VALOR_REAL": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}),
        use_container_width=True
    )
        

        # ================== TABELA DETALHAMENTO POR MÊS ==================

        st.markdown("---")

        st.subheader("📊 Compras por Mês (Detalhado)")

        tabela_total = (
            real[["MES_NUM", "MES_NOME", "DESCRICAO", "VALOR_REAL"]]
            .sort_values(["MES_NUM", "DESCRICAO"])
        )

        st.dataframe(
            tabela_total[["MES_NOME", "DESCRICAO", "VALOR_REAL"]]
            .style.format({"VALOR_REAL": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")"}),
            use_container_width=True
        )



st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Sistema conectado ao Excel | Atualização automática de dados"
    "</div>",
    unsafe_allow_html=True
)