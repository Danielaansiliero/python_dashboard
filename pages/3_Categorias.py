"""
Página de Análise por Categoria de Produtos
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.preprocessing.text_cleaner import TextCleaner
from src.preprocessing.category_extractor import CategoryExtractor
from src.visualization.charts import DashboardCharts

# Nota: st.set_page_config() deve ser chamado apenas no app.py principal


@st.cache_data
def load_and_process_data():
    """Carrega e processa dados."""
    df = pd.read_csv('data/dataset_avaliacoes.csv')

    text_cleaner = TextCleaner()
    category_extractor = CategoryExtractor()

    df['avaliacao_limpa'] = df['avaliacao'].apply(text_cleaner.clean_text)
    df[['categoria', 'categoria_confianca']] = df['avaliacao_limpa'].apply(
        lambda x: pd.Series(category_extractor.extract_category(x))
    )

    return df


st.title("🏷️ Análise por Categoria de Produtos")
st.markdown("Explore o desempenho e sentimento por categoria de produto.")
st.divider()

# Carrega dados
df = load_and_process_data()

# Estatísticas gerais
st.header("📊 Visão Geral das Categorias")

# Calcula estatísticas por categoria
cat_stats = df.groupby('categoria').agg({
    'nota': ['mean', 'count'],
    'sentimento': lambda x: (x == 'positivo').mean() * 100
}).round(2)

cat_stats.columns = ['Nota Média', 'Total Avaliações', '% Positivo']
cat_stats = cat_stats.sort_values('Nota Média', ascending=False)

# KPIs
col1, col2, col3 = st.columns(3)

with col1:
    melhor_categoria = cat_stats['Nota Média'].idxmax()
    melhor_nota = cat_stats['Nota Média'].max()
    st.metric("🏆 Melhor Categoria", melhor_categoria,
             delta=f"Nota: {melhor_nota:.2f}")

with col2:
    maior_volume = cat_stats['Total Avaliações'].idxmax()
    volume = cat_stats['Total Avaliações'].max()
    st.metric("📈 Maior Volume", maior_volume,
             delta=f"{int(volume)} avaliações")

with col3:
    mais_positiva = cat_stats['% Positivo'].idxmax()
    pct_pos = cat_stats['% Positivo'].max()
    st.metric("😊 Mais Positiva", mais_positiva,
             delta=f"{pct_pos:.1f}% positivo")

st.divider()

# Tabela de estatísticas
st.subheader("📋 Estatísticas Completas")

# Filtra categorias com pelo menos 10 avaliações
cat_stats_filtered = cat_stats[cat_stats['Total Avaliações'] >= 10]

st.dataframe(
    cat_stats_filtered,
    use_container_width=True,
    column_config={
        "Nota Média": st.column_config.NumberColumn(
            "Nota Média",
            format="⭐ %.2f",
        ),
        "Total Avaliações": st.column_config.NumberColumn(
            "Total Avaliações",
            format="%d",
        ),
        "% Positivo": st.column_config.ProgressColumn(
            "% Positivo",
            format="%.1f%%",
            min_value=0,
            max_value=100,
        ),
    }
)

st.divider()

# Gráficos comparativos
st.header("📊 Comparações Visuais")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Distribuição de Categorias")
    fig_pie = DashboardCharts.category_pie(df, 'categoria')
    st.plotly_chart(fig_pie, use_container_width=True)

with col_g2:
    st.subheader("Comparação de Métricas")
    fig_comparison = DashboardCharts.category_comparison(df, 'categoria')
    st.plotly_chart(fig_comparison, use_container_width=True)

st.divider()

# Análise detalhada por categoria selecionada
st.header("🔍 Análise Detalhada por Categoria")

categoria_selecionada = st.selectbox(
    "Selecione uma categoria para análise detalhada:",
    options=df['categoria'].unique().tolist()
)

if categoria_selecionada:
    df_cat = df[df['categoria'] == categoria_selecionada]

    # KPIs da categoria
    col_cat1, col_cat2, col_cat3, col_cat4 = st.columns(4)

    with col_cat1:
        st.metric("Total", len(df_cat))

    with col_cat2:
        nota_media_cat = df_cat['nota'].mean()
        st.metric("Nota Média", f"{nota_media_cat:.2f}")

    with col_cat3:
        pct_pos_cat = (df_cat['sentimento'] == 'positivo').mean() * 100
        st.metric("% Positivo", f"{pct_pos_cat:.1f}%")

    with col_cat4:
        cinco_estrelas_cat = (df_cat['nota'] == 5).sum()
        st.metric("5 Estrelas", cinco_estrelas_cat)

    st.divider()

    # Distribuições
    col_dist1, col_dist2 = st.columns(2)

    with col_dist1:
        st.subheader("Distribuição de Notas")
        fig_rating_cat = DashboardCharts.rating_distribution(df_cat)
        st.plotly_chart(fig_rating_cat, use_container_width=True)

    with col_dist2:
        st.subheader("Distribuição de Sentimentos")
        fig_sent_cat = DashboardCharts.sentiment_donut(df_cat)
        st.plotly_chart(fig_sent_cat, use_container_width=True)

    st.divider()

    # Amostra de avaliações
    st.subheader(f"📝 Avaliações de {categoria_selecionada}")

    # Filtro de sentimento
    sent_filter_cat = st.radio(
        "Mostrar:",
        ["Todas", "Positivas", "Negativas"],
        horizontal=True
    )

    df_cat_filtered = df_cat.copy()

    if sent_filter_cat == "Positivas":
        df_cat_filtered = df_cat_filtered[df_cat_filtered['sentimento'] == 'positivo']
    elif sent_filter_cat == "Negativas":
        df_cat_filtered = df_cat_filtered[df_cat_filtered['sentimento'] == 'negativo']

    # Ordena por nota
    df_cat_filtered = df_cat_filtered.sort_values('nota', ascending=False)

    num_show = st.slider("Quantidade a exibir", 5, 30, 10, key="cat_slider")

    for idx, row in df_cat_filtered.head(num_show).iterrows():
        sentiment_emoji = "😊" if row['sentimento'] == 'positivo' else "😞"
        star_rating = "⭐" * int(row['nota'])

        with st.expander(f"{sentiment_emoji} {star_rating} - Nota {row['nota']}", key=f"category_expander_{idx}"):
            st.markdown(row['avaliacao'])

st.divider()

# Comparação entre categorias
st.header("⚖️ Comparação entre Categorias")

col_comp1, col_comp2 = st.columns(2)

with col_comp1:
    cat1 = st.selectbox("Categoria 1", df['categoria'].unique().tolist(), key="cat1")

with col_comp2:
    cat2 = st.selectbox("Categoria 2", df['categoria'].unique().tolist(), key="cat2",
                       index=1 if len(df['categoria'].unique()) > 1 else 0)

if cat1 and cat2 and cat1 != cat2:
    df_comp1 = df[df['categoria'] == cat1]
    df_comp2 = df[df['categoria'] == cat2]

    # Tabela comparativa
    comp_data = {
        'Métrica': [
            'Total Avaliações',
            'Nota Média',
            '% Positivo',
            '% Negativo',
            'Avaliações 5⭐',
            'Avaliações 1⭐'
        ],
        cat1: [
            len(df_comp1),
            f"{df_comp1['nota'].mean():.2f}",
            f"{(df_comp1['sentimento'] == 'positivo').mean() * 100:.1f}%",
            f"{(df_comp1['sentimento'] == 'negativo').mean() * 100:.1f}%",
            (df_comp1['nota'] == 5).sum(),
            (df_comp1['nota'] == 1).sum()
        ],
        cat2: [
            len(df_comp2),
            f"{df_comp2['nota'].mean():.2f}",
            f"{(df_comp2['sentimento'] == 'positivo').mean() * 100:.1f}%",
            f"{(df_comp2['sentimento'] == 'negativo').mean() * 100:.1f}%",
            (df_comp2['nota'] == 5).sum(),
            (df_comp2['nota'] == 1).sum()
        ]
    }

    df_comparison = pd.DataFrame(comp_data)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)

else:
    st.info("Selecione duas categorias diferentes para comparar.")

st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏷️ <i>Categorias extraídas automaticamente via NLP</i></p>
</div>
""", unsafe_allow_html=True)
