"""
Dashboard de Análise de Sentimentos E-commerce
Página principal
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.append(str(Path(__file__).parent))

from src.preprocessing.text_cleaner import TextCleaner
from src.preprocessing.category_extractor import CategoryExtractor
from src.analysis.churn_detector import ChurnDetector
from src.analysis.opportunity_finder import OpportunityFinder
from src.visualization.charts import DashboardCharts

# Configuração da página
st.set_page_config(
    page_title="Análise de Sentimentos - E-commerce",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Carrega e processa o dataset."""
    df = pd.read_csv('data/dataset_avaliacoes.csv')
    return df


@st.cache_data
def process_data(df):
    """Processa dados: categorias, churn, oportunidades."""
    # Inicializa processadores
    text_cleaner = TextCleaner()
    category_extractor = CategoryExtractor()

    # Limpa textos
    df['avaliacao_limpa'] = df['avaliacao'].apply(text_cleaner.clean_text)

    # Extrai categorias
    df[['categoria', 'categoria_confianca']] = df['avaliacao_limpa'].apply(
        lambda x: pd.Series(category_extractor.extract_category(x))
    )

    return df


# Header
st.markdown('<h1 class="main-header">📊 Dashboard de Análise de Sentimentos</h1>',
            unsafe_allow_html=True)
st.markdown("**Análise de 15.500+ avaliações de e-commerce brasileiro**")

# Disclaimer sobre privacidade e uso dos dados
with st.expander("ℹ️ Sobre os Dados e Privacidade", expanded=False):
    st.info("""
    **📊 Dados Educacionais e Demonstrativos**

    Este dashboard foi desenvolvido com **finalidade educacional e demonstrativa**, como parte de um projeto de portfólio em Ciência de Dados.

    **🔒 Privacidade e Conformidade:**
    - ✅ **Dados 100% anônimos**: Não contêm informações pessoais identificáveis
    - ✅ **Sem dados sensíveis**: Não há CPF, e-mail, telefone, endereço ou qualquer dado pessoal
    - ✅ **Avaliações públicas**: Textos são avaliações genéricas de produtos de e-commerce
    - ✅ **Conformidade LGPD/GDPR**: Todos os dados foram anonimizados e não comprometem a privacidade

    **🎓 Finalidade:**
    - Demonstração de técnicas de **Processamento de Linguagem Natural (NLP)**
    - Análise de sentimentos e detecção de padrões textuais
    - Visualização de dados e criação de dashboards interativos
    - Aplicação prática de Machine Learning em contexto de negócios

    **📌 Importante:** Este é um projeto acadêmico/educacional. Os insights e análises apresentados são para fins demonstrativos.
    """)

st.divider()

# Carregamento de dados
with st.spinner('Carregando dados...'):
    df = load_data()
    df = process_data(df)

# Sidebar com filtros
with st.sidebar:
    st.header("🔍 Filtros")

    sentimento_filter = st.multiselect(
        "Sentimento",
        options=df['sentimento'].unique().tolist(),
        default=df['sentimento'].unique().tolist()
    )

    nota_filter = st.slider(
        "Faixa de Notas",
        min_value=int(df['nota'].min()),
        max_value=int(df['nota'].max()),
        value=(int(df['nota'].min()), int(df['nota'].max()))
    )

    categorias_disponiveis = df['categoria'].unique().tolist()
    categoria_filter = st.multiselect(
        "Categoria",
        options=categorias_disponiveis,
        default=categorias_disponiveis
    )

    st.divider()
    st.markdown("### 📄 Sobre")
    st.markdown("""
    Este dashboard analisa avaliações de clientes usando:
    - 🤖 **NLP** para categorização
    - 😊 **Análise de sentimentos**
    - ⚠️ **Detecção de churn**
    - 💡 **Oportunidades de crescimento**
    """)

# Aplicar filtros
df_filtered = df[
    (df['sentimento'].isin(sentimento_filter)) &
    (df['nota'].between(nota_filter[0], nota_filter[1])) &
    (df['categoria'].isin(categoria_filter))
]

# Métricas principais
st.header("📈 Métricas Principais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total = len(df_filtered)
    st.metric(
        "Total de Avaliações",
        f"{total:,}",
        delta=f"{(total/len(df)*100):.0f}% do total"
    )

with col2:
    nota_media = df_filtered['nota'].mean()
    delta_nota = nota_media - df['nota'].mean()
    st.metric(
        "Nota Média",
        f"{nota_media:.2f}",
        delta=f"{delta_nota:+.2f}"
    )

with col3:
    pct_positivo = (df_filtered['sentimento'] == 'positivo').mean() * 100
    st.metric(
        "% Sentimento Positivo",
        f"{pct_positivo:.1f}%"
    )

with col4:
    cinco_estrelas = (df_filtered['nota'] == 5).sum()
    st.metric(
        "Avaliações 5 ⭐",
        f"{cinco_estrelas:,}"
    )

st.divider()

# Gráficos principais
st.header("📊 Visualizações")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Distribuição de Notas")
    fig_rating = DashboardCharts.rating_distribution(df_filtered)
    st.plotly_chart(fig_rating, use_container_width=True)

with col_right:
    st.subheader("Distribuição de Sentimentos")
    fig_sentiment = DashboardCharts.sentiment_donut(df_filtered)
    st.plotly_chart(fig_sentiment, use_container_width=True)

st.divider()

# Análise por categoria
st.header("🏷️ Análise por Categoria")

col_cat1, col_cat2 = st.columns([2, 1])

with col_cat1:
    st.subheader("Comparação por Categoria")
    if 'categoria' in df_filtered.columns:
        fig_category = DashboardCharts.category_comparison(df_filtered, 'categoria')
        st.plotly_chart(fig_category, use_container_width=True)

with col_cat2:
    st.subheader("Distribuição de Categorias")
    if 'categoria' in df_filtered.columns:
        fig_cat_pie = DashboardCharts.category_pie(df_filtered, 'categoria')
        st.plotly_chart(fig_cat_pie, use_container_width=True)

st.divider()

# Análise de Churn e Oportunidades
st.header("🎯 Insights de Negócio")

# Calcula métricas de churn e oportunidades
churn_detector = ChurnDetector()
opportunity_finder = OpportunityFinder()

churn_stats = churn_detector.get_churn_statistics(df_filtered)
opportunity_stats = opportunity_finder.get_opportunity_statistics(df_filtered)

col_business1, col_business2 = st.columns(2)

with col_business1:
    st.subheader("⚠️ Risco de Churn")
    pct_alto_risco = churn_stats['percentual_alto_risco']
    fig_churn = DashboardCharts.churn_gauge(pct_alto_risco)
    st.plotly_chart(fig_churn, use_container_width=True)

    st.metric("Clientes em Alto Risco", churn_stats['alto_risco'])
    st.metric("Clientes em Médio Risco", churn_stats['medio_risco'])

with col_business2:
    st.subheader("💡 Oportunidades")
    pct_alta_oportunidade = opportunity_stats['percentual_alta_oportunidade']
    fig_opportunity = DashboardCharts.opportunity_gauge(pct_alta_oportunidade)
    st.plotly_chart(fig_opportunity, use_container_width=True)

    st.metric("Alta Oportunidade", opportunity_stats['alta_oportunidade'])
    st.metric("Advogados da Marca", opportunity_stats['advogados_marca'])

st.divider()

# Navegação para outras páginas
st.header("🧭 Explore Mais")

st.markdown("""
Navegue pelas páginas laterais para análises mais detalhadas:
- **📊 Visão Geral**: Análise completa com filtros avançados
- **😊 Análise de Sentimentos**: Deep dive em sentimentos e aspectos
- **🏷️ Categorias**: Análise detalhada por categoria de produto
- **🎯 Churn & Oportunidades**: Identificação de riscos e oportunidades
- **🔤 Insights NLP**: Tópicos, palavras-chave e análise textual
""")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Dashboard desenvolvido com Streamlit | Dados: E-commerce Brasil</p>
    <p>📧 Análise de 15.500+ avaliações reais de clientes</p>
</div>
""", unsafe_allow_html=True)
