# Dashboard Corporativo de Gastos 2026

Sistema desenvolvido em Python utilizando Streamlit para acompanhamento financeiro corporativo, controle orçamentário e análise de gastos previstos e não previstos.

---

# Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL

---

# Objetivo do Projeto

O dashboard foi criado para realizar:

- Controle financeiro corporativo
- Monitoramento de orçamento
- Comparação entre previsto e realizado
- Acompanhamento mensal de gastos
- Visualização executiva por diretoria
- Identificação de gastos não previstos
- Geração de insights automáticos

---

# Sistema de Login

O sistema possui autenticação de usuários com permissões por diretoria.

## Estrutura de Usuários

```python
USUARIOS = {
    "admin": {"senha": "admin2026", "acesso": ["PR", "DG", "DE", "DC", "DO"]},
    "pr": {"senha": "*", "acesso": ["PR", "DG", "DE", "DC", "DO"]},
    "dg": {"senha": "*", "acesso": ["DG"]},
    "dc": {"senha": "*", "acesso": ["DC"]},
    "de": {"senha": "*", "acesso": ["DE"]},
    "do": {"senha": "*", "acesso": ["DO"]}
}
```

---

# Estrutura Esperada do Projeto

```bash
projeto/
│
├── app.py
├── dados.xlsx
│
├── icon/
│   └── imagem_caema.png
```

---

# Estrutura do Excel

O arquivo `dados.xlsx` deve conter as seguintes abas:

## Aba: previsto

Contém os gastos planejados.

---

## Aba: realizado

Contém os gastos executados.

### Colunas principais

| Coluna | Descrição |
|---|---|
| DIRETORIA | Diretoria responsável |
| GERENCIA | Gerência responsável |
| DESCRICAO | Descrição da compra |
| TIPO | AQUISICAO ou SERVICO |
| VALOR_OC | Valor da Ordem de Compra |
| VALOR_NF | Valor da Nota Fiscal |
| PREVISTO | SIM ou NAO |
| DATA | Data da compra |

---

## Aba: orcamento

Contém os valores orçamentários.

### Colunas principais

| Coluna | Descrição |
|---|---|
| DIRETORIA | Diretoria |
| ORCAMENTO_AQUISICAO | Orçamento de aquisição |

---

# Interface do Sistema

O dashboard utiliza:

- Design corporativo
- Paleta azul bebê
- Layout responsivo
- Cards de indicadores
- Gráficos interativos
- Tabelas estilizadas

---

# Funcionalidades

# Dashboard Geral

O dashboard principal apresenta:

## Indicadores (KPIs)

- Total Geral
- Total de Serviços
- Total de Aquisições

---

## Gráficos

### Evolução Mensal de Aquisições por Diretoria

Exibe:
- evolução mensal
- comparação entre diretorias

---

### Evolução Mensal de Serviços

Comparativo mensal de serviços realizados.

---

### Distribuição por Classificação

Gráfico pizza mostrando:
- categorias com maior gasto
- percentual por classificação

---

### Top 10 Classificações

Ranking das classificações com maior custo.

---

### Top 10 Gerências

Mostra as gerências com maiores gastos.

---

### Realizado vs Não Previsto

Compara:
- gastos planejados
- gastos emergenciais

---

### Aquisição vs Serviço

Comparação temporal entre:
- aquisições
- serviços

---

### OC vs NF vs Orçamento

Controle financeiro comparando:
- Ordem de Compra
- Nota Fiscal
- Orçamento disponível

---

# Insights Automáticos

O sistema gera insights mensais automaticamente.

## Informações Geradas

Para cada mês:

- Total gasto
- Diretoria que mais gastou
- Classificação que mais consumiu
- Percentual de gastos não previstos

---

# Dashboard por Diretoria

Cada diretoria possui sua própria aba.

## Funcionalidades

### KPIs

- Orçamento
- Realizado
- Não previsto

---

### Gráficos

- Comparativo financeiro
- Evolução mensal

---

### Tabelas

#### Realizado por mês

Resumo mensal de gastos.

#### Não previsto

Lista:
- gerência
- descrição
- valor

#### Compras detalhadas

Detalhamento completo por mês.

---

# Funções Importantes

## Formatação Monetária

```python
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
```

Converte valores para padrão brasileiro.

---

## Cache de Dados

```python
@st.cache_data
```

Melhora:
- desempenho
- carregamento
- leitura do Excel

---

# Bibliotecas Utilizadas

## Instalação

```bash
pip install streamlit
pip install pandas
pip install plotly
pip install openpyxl
```

---

# Executando o Projeto

## Rodar aplicação

```bash
streamlit run app.py
```

---

# Personalização Visual

O sistema utiliza CSS customizado para:

- cards modernos
- tabelas estilizadas
- sidebar personalizada
- botões interativos
- layout corporativo

---

# Regras de Negócio

## Saldo Restante

```python
SALDO_RESTANTE = ORCAMENTO_AQUISICAO - VALOR_OC
```

### Interpretação

| Resultado | Significado |
|---|---|
| Positivo | Ainda possui orçamento |
| Negativo | Orçamento excedido |

---

# Performance

O sistema utiliza:

- cache de dados
- carregamento otimizado
- filtros dinâmicos
- gráficos responsivos

---

# Controle de Acesso

Cada usuário visualiza apenas:
- diretorias autorizadas
- dados permitidos

---

# Melhorias Futuras

## Sugestões

- Banco de dados SQL
- Exportação PDF
- Exportação Excel
- Integração ERP
- Alertas automáticos
- Inteligência Artificial
- Previsão financeira

---

# Resultado Final

O projeto entrega:

✅ Controle financeiro corporativo  
✅ Gestão orçamentária  
✅ Transparência financeira  
✅ Visual executivo moderno  
✅ Monitoramento em tempo real  
✅ Insights automáticos  
✅ Segurança por usuário  

---

# Desenvolvido com

- Python
- Streamlit
- Pandas
- Plotly

---

# Licença

Projeto desenvolvido para uso corporativo interno.
