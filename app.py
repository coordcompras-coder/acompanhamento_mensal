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

#CSS PERSONALIZADO
st.markdown("""
<style>
/* 🎨 FUNDO GRADIENTE */
.stApp {
    background: linear-gradient(135deg, #1F4E5F, #2F6F89);
}

/* 📦 CARDS (containers) */
[data-testid="stMetric"], 
[data-testid="stDataFrame"], 
[data-testid="stTable"] {
    background-color: #FFFFFF;
    border-radius: 10px;
    padding: 10px;
}

/* 🔢 TEXTO DOS INDICADORES */
[data-testid="stMetric"] * {
    color: #000000 !important;
}

/* 📝 TEXTO PRINCIPAL */
h1, h2, h3, h4, h5, h6, p, label {
    color: #FFFFFF !important;
}

/* 📝 TEXTO SECUNDÁRIO */
span, div {
    color: #D9E6EC;
}

/* 🔝 HEADER TRANSPARENTE */
[data-testid="stHeader"] {
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

# LOGO
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "icon", "imagem_caema.png")
st.image(logo_path, width=300)

st.title("ACOMPANHAMENTO DE GASTOS PREVISTOS E NÃO PREVISTOS 2026")

# 🔐 SENHA DE ACESSO
SENHA_CORRETA = "CAEMA2026"  # 👉 você define aqui

senha = st.text_input("🔐 Digite a senha para acessar o sistema", type="password")

if senha != SENHA_CORRETA:
    if senha != "":
        st.error("Senha incorreta")
    st.stop()



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
diretorias = ["Dashboard", "PR", "DG", "DE", "DC", "DO"]
tabs = st.tabs(["Dashboard", "PR", "DG", "DE", "DC", "DO"])

# ================== DASHBOARD ==================
with tabs[0]:
    st.header("Dashboard Geral")

    total = df_realizado["VALOR_OC"].sum()

    servicos = df_realizado[df_realizado["TIPO"] == "SERVICO"]["VALOR_OC"].sum()
    aquisicoes = df_realizado[df_realizado["TIPO"] == "AQUISICAO"]["VALOR_OC"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Geral", formatar_moeda(total))
    col2.metric("Serviços", formatar_moeda(servicos))
    col3.metric("Aquisições", formatar_moeda(aquisicoes))



#========graficos de linha por diretoria========
    st.markdown("---")
#AQUISIÇÃO LINHA POR DIRETORIA
    st.subheader("📈 Evolução Mensal - Aquisições por Diretoria")

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
        markers=True
    )

    fig_aq.update_traces(
        line_shape="spline",  # 👈 linha suave
        hovertemplate="R$ %{y:,.2f}"
    )

    fig_aq.update_layout(
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.2f"
    )

    st.plotly_chart(fig_aq, use_container_width=True, key="linha_aquisicao_dir")


    st.markdown("---")
#SERVIÇOS LINHA POR DIRETORIA
    st.subheader("📈 Evolução Mensal - Serviços por Diretoria")

    df_sv = df_realizado[df_realizado["TIPO"] == "SERVICO"]

    df_sv_mensal = (
        df_sv.groupby(["MES_NUM", "MES_NOME", "DIRETORIA"])["VALOR_OC"]
        .sum()
        .reset_index()
        .sort_values("MES_NUM")
    )

    fig_sv = px.line(
        df_sv_mensal,
        x="MES_NOME",
        y="VALOR_OC",
        color="DIRETORIA",
        markers=True
    )

    fig_sv.update_traces(
        line_shape="spline",
        hovertemplate="R$ %{y:,.2f}"
    )

    fig_sv.update_layout(
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.2f"
    )

    st.plotly_chart(fig_sv, use_container_width=True, key="linha_servico_dir")

    st.markdown("---")
#DISTRIBUIÇÃO POR CLASSIFICAÇÃO
    df_class = (
        df_realizado[df_realizado["TIPO"] == "AQUISICAO"]  # 👈 FILTRO AQUI
        .groupby("CLASSIFICACAO")["VALOR_OC"]
        .sum()
        .reset_index()
        .sort_values("VALOR_OC", ascending=False)
    )

    # Top 10
    df_top10 = df_class.head(10)

    fig = px.pie(
        df_top10,
        names="CLASSIFICACAO",
        values="VALOR_OC",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
#TOP GERÊNCIAS QUE MAIS GASTAM
    st.subheader("TOP 10 GERÊNCIAS QUE MAIS GASTAM")
    df_ger = (
        df_realizado[df_realizado["TIPO"] == "AQUISICAO"]  # 👈 FILTRO AQUI
        .groupby("GERENCIA")["VALOR_OC"]
        .sum()
        .reset_index()
        .sort_values("VALOR_OC", ascending=False)
        .head(10)
    )

    fig = px.bar(
        df_ger,  # ou df_top10 (depende do seu nome)
        x="VALOR_OC",
        y="GERENCIA",
        orientation="h",
        text="VALOR_OC"  # 👈 MOSTRA O VALOR
    )

    fig.update_traces(
        texttemplate="R$ %{text:,.2f}",  # 👈 FORMATA EM REAL
        textposition="inside" #outside para mostrar fora da barra, inside para mostrar dentro da barra e automatic ou auto para deixar o Plotly decidir o melhor lugar para mostrar o valor 
    )

    fig.update_layout(
        xaxis_tickprefix="R$ ",
        xaxis_tickformat=",.2f"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
#REALIZADO vs NÃO PREVISTO (impacto)
    st.subheader("REALIZADO vs NÃO PREVISTO (impacto)")
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
        text="VALOR_OC"  # 👈 MOSTRA O VALOR
    )

    fig.update_traces(
        texttemplate="R$ %{text:,.2f}",  # 👈 FORMATA
        textposition="outside"
    )

    fig.update_layout(
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.2f"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
#AQUISIÇÃO vs SERVIÇO AO LONGO DO TEMPO
    st.subheader("AQUISIÇÃO vs SERVIÇO AO LONGO DO TEMPO")
    df_tipo = (
    df_realizado.groupby(["MES_NUM", "MES_NOME", "TIPO"])["VALOR_OC"]
    .sum()
    .reset_index()
    .sort_values("MES_NUM")
)

    fig = px.line(
        df_tipo,
        x="MES_NOME",
        y="VALOR_OC",
        color="TIPO",
        markers=True
    )

    fig.update_traces(line_shape="spline")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
#OC vs NF (controle financeiro)
    st.subheader("📊 OC vs NF (Aquisição) por Diretoria vs Orçamento")

    # 🔹 FILTRAR APENAS AQUISIÇÃO
    df_aq = df_realizado[df_realizado["TIPO"] == "AQUISICAO"]

    # 🔹 AGRUPAR OC e NF
    df_oc_nf = (
        df_aq.groupby("DIRETORIA")[["VALOR_OC", "VALOR_NF"]]
        .sum()
        .reset_index()
    )

    # 🔹 ORÇAMENTO (já é aquisição)
    df_orc = (
        df_orcamento.groupby("DIRETORIA")["ORCAMENTO_AQUISICAO"]
        .sum()
        .reset_index()
    )

    # 🔹 MERGE
    df_final = df_oc_nf.merge(df_orc, on="DIRETORIA", how="left")

    # 🔹 GRÁFICO DE BARRAS
    fig = px.bar(
        df_final,
        x="DIRETORIA",
        y=["VALOR_OC", "VALOR_NF"],
        barmode="group",
        text_auto=True
    )

    # 🔹 TEXTO FORA DA BARRA
    fig.update_traces(
        texttemplate="R$ %{y:,.2f}",
        textposition="outside"
    )

    # 🔹 LINHA DE ORÇAMENTO (SUAVE)
    fig.add_scatter(
        x=df_final["DIRETORIA"],
        y=df_final["ORCAMENTO_AQUISICAO"],
        mode="lines+markers",
        name="Orçamento Aquisição",
        line=dict(
            shape="spline",   # mantém a linha suave
            dash="solid",     # 👈 linha contínua
            color="red",      # 👈 cor vermelha
            width=3
        )
    )

    # 🔹 FORMATAÇÃO
    fig.update_layout(
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.2f"
    )

    st.plotly_chart(fig, use_container_width=True)

#tabela de conferencia entre OC e NF
    st.subheader("📊 Conferência: Orçado vs Realizado por Diretoria")

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

    df_conf["DIFERENCA"] = df_conf["VALOR_OC"] - df_conf["ORCAMENTO_AQUISICAO"]

    st.dataframe(
        df_conf.style.format({
            "VALOR_OC": "R$ {:,.2f}",
            "ORCAMENTO_AQUISICAO": "R$ {:,.2f}",
            "DIFERENCA": "R$ {:,.2f}"
        }),
        use_container_width=True
    )
    
    st.write("Se a diferença for positiva, estourou. Se for negativa, ainda tem saldo ")
    st.caption("📌 Este gráfico considera apenas dados de AQUISIÇÃO")

    st.markdown("---")
#INSIGHTS AUTOMÁTICOS
    st.subheader("🧠 Insights Automáticos")

    # 🔹 Diretoria que mais gastou (AQUISIÇÃO)
    df_aq = df_realizado[df_realizado["TIPO"] == "AQUISICAO"]

    top_dir = (
        df_aq.groupby("DIRETORIA")["VALOR_OC"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    if not top_dir.empty:
        dir_top = top_dir.iloc[0]

        st.info(f"🏆 Diretoria com maior gasto em aquisições: **{dir_top['DIRETORIA']}** "
                f"com {formatar_moeda(dir_top['VALOR_OC'])}")

    # 🔹 Mês com maior gasto
    top_mes = (
        df_realizado.groupby(["MES_NUM", "MES_NOME"])["VALOR_OC"]
        .sum()
        .reset_index()
        .sort_values("VALOR_OC", ascending=False)
    )

    if not top_mes.empty:
        mes_top = top_mes.iloc[0]

        st.info(f"📅 Mês com maior gasto: **{mes_top['MES_NOME']}** "
                f"com {formatar_moeda(mes_top['VALOR_OC'])}")

    # 🔹 % de não previsto
    total = df_realizado["VALOR_OC"].sum()
    nao_prev = df_realizado[df_realizado["PREVISTO"] == "NAO"]["VALOR_OC"].sum()

    if total > 0:
        perc_nao_prev = (nao_prev / total) * 100

        st.warning(f"⚠️ {perc_nao_prev:.1f}% dos gastos são NÃO PREVISTOS")

    # 🔹 Diretoria que estourou orçamento
    df_conf = (
        df_aq.groupby("DIRETORIA")["VALOR_OC"]
        .sum()
        .reset_index()
    )

    df_conf = df_conf.merge(
        df_orcamento[["DIRETORIA", "ORCAMENTO_AQUISICAO"]],
        on="DIRETORIA",
        how="left"
    )

    df_conf["DIFERENCA"] = df_conf["VALOR_OC"] - df_conf["ORCAMENTO_AQUISICAO"]

    estouro = df_conf[df_conf["DIFERENCA"] > 0]

    if not estouro.empty:
        for _, row in estouro.iterrows():
            st.error(f"🚨 {row['DIRETORIA']} ultrapassou o orçamento em "
                    f"{formatar_moeda(row['DIFERENCA'])}")
    else:
        st.success("✅ Nenhuma diretoria ultrapassou o orçamento")

    # 🔹 Classificação que mais consome (AQUISIÇÃO)
    top_class = (
        df_aq.groupby("CLASSIFICACAO")["VALOR_OC"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    if not top_class.empty:
        class_top = top_class.iloc[0]

        st.info(f"📦 Maior tipo de gasto: **{class_top['CLASSIFICACAO']}** "
                f"com {formatar_moeda(class_top['VALOR_OC'])}")








# ================== LOOP ==================
diretorias = ["PR", "DG", "DE", "DC", "DO"]
for i, diretoria in enumerate(diretorias):

    with tabs[i + 1]:
        st.header(f"Diretoria {diretoria}")

        # FILTROS
        prev = df_previsto[df_previsto["DIRETORIA"] == diretoria]
        real = df_realizado[
            (df_realizado["DIRETORIA"] == diretoria) &
            (df_realizado["TIPO"] == "AQUISICAO")
        ]
        orc = df_orcamento[df_orcamento["DIRETORIA"] == diretoria]

        # ================== CÁLCULOS ==================
        orc_aquisicao = orc["ORCAMENTO_AQUISICAO"].sum()

        realizado_total = real["VALOR_OC"].sum()
        realizado_previsto = real[real["PREVISTO"] == "SIM"]["VALOR_OC"].sum()
        nao_previsto = real[real["PREVISTO"] == "NAO"]["VALOR_OC"].sum()

        # ================== KPIs ==================
        st.subheader("Indicadores")

        col1, col2, col3 = st.columns(3)


        col1.metric("Orçamento Aquisição", formatar_moeda(orc_aquisicao))
        col2.metric("Realizado", formatar_moeda(realizado_total))
        col3.metric("Não Previsto", formatar_moeda(nao_previsto))

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
        st.subheader("📋 Realizado por Mês")

        tabela_mensal = (
            real[real["PREVISTO"] == "SIM"]
            .groupby(["MES_NUM", "MES_NOME"])["VALOR_OC"]
            .sum()
            .reset_index()
            .sort_values("MES_NUM")
        )

        st.dataframe(
        tabela_mensal[["MES_NOME", "VALOR_OC"]]
        .style.format({
            "VALOR_OC": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        }),
        use_container_width=True
        )

        st.markdown("---")

        # ================== TABELA NÃO PREVISTO ==================
        st.subheader("⚠️ Não Previsto")

        tabela_nao_previsto = real[real["PREVISTO"] == "NAO"]

        st.dataframe(
        tabela_nao_previsto[["GERENCIA", "DESCRICAO", "TIPO", "VALOR_OC"]]
        .style.format({
            "VALOR_OC": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
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
        .style.format({
            "VALOR_OC": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        }),
            use_container_width=True
        )



st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Sistema conectado ao Excel | Atualização automática de dados"
    "</div>",
    unsafe_allow_html=True
)