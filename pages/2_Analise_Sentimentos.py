"""
Página de Análise Detalhada de Sentimentos
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).parent.parent))

from src.preprocessing.text_cleaner import TextCleaner
from src.preprocessing.category_extractor import CategoryExtractor
from src.visualization.charts import DashboardCharts
from src.visualization.wordcloud_gen import WordCloudGenerator

st.set_page_config(page_title="Análise de Sentimentos", page_icon="😊", layout="wide")


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


st.title("😊 Análise Detalhada de Sentimentos")
st.markdown("Explore padrões de sentimentos positivos e negativos nas avaliações.")
st.divider()

# Carrega dados
df = load_and_process_data()

# Tabs
tab1, tab2, tab3 = st.tabs([
    "📊 Visão Geral",
    "☁️ Nuvens de Palavras",
    "🔍 Explorador de Avaliações"
])

# ========== TAB 1: VISÃO GERAL ==========
with tab1:
    st.header("📊 Distribuição de Sentimentos")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    total_positivo = (df['sentimento'] == 'positivo').sum()
    total_negativo = (df['sentimento'] == 'negativo').sum()
    pct_positivo = (total_positivo / len(df)) * 100
    nota_media_positivo = df[df['sentimento'] == 'positivo']['nota'].mean()

    with col1:
        st.metric("👍 Positivas", total_positivo,
                 delta=f"{pct_positivo:.1f}%")

    with col2:
        st.metric("👎 Negativas", total_negativo,
                 delta=f"{(100-pct_positivo):.1f}%")

    with col3:
        st.metric("⭐ Nota Média (Positivas)", f"{nota_media_positivo:.2f}")

    with col4:
        nota_media_negativo = df[df['sentimento'] == 'negativo']['nota'].mean()
        st.metric("⭐ Nota Média (Negativas)", f"{nota_media_negativo:.2f}")

    st.divider()

    # Gráficos
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("Sentimento vs Nota")
        fig_heatmap = DashboardCharts.sentiment_by_rating_heatmap(df)
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with col_g2:
        st.subheader("Distribuição Geral")
        fig_donut = DashboardCharts.sentiment_donut(df)
        st.plotly_chart(fig_donut, use_container_width=True)

    st.divider()

    # Análise por categoria
    st.subheader("📊 Sentimento por Categoria")

    if 'categoria' in df.columns:
        cat_sent = df.groupby(['categoria', 'sentimento']).size().unstack(fill_value=0)
        cat_sent['% Positivo'] = (cat_sent['positivo'] /
                                  (cat_sent['positivo'] + cat_sent['negativo']) * 100)
        cat_sent['Total'] = cat_sent['positivo'] + cat_sent['negativo']
        cat_sent = cat_sent[cat_sent['Total'] >= 10].sort_values('% Positivo',
                                                                  ascending=False)

        st.dataframe(
            cat_sent,
            use_container_width=True,
            column_config={
                "% Positivo": st.column_config.ProgressColumn(
                    "% Positivo",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
            }
        )

# ========== TAB 2: NUVENS DE PALAVRAS ==========
with tab2:
    st.header("☁️ Nuvens de Palavras")

    text_cleaner = TextCleaner()
    wc_generator = WordCloudGenerator()

    # Separar textos por sentimento
    texto_positivo = ' '.join(
        df[df['sentimento'] == 'positivo']['avaliacao_limpa'].tolist()
    )
    texto_negativo = ' '.join(
        df[df['sentimento'] == 'negativo']['avaliacao_limpa'].tolist()
    )

    col_wc1, col_wc2 = st.columns(2)

    with col_wc1:
        st.subheader("😊 Avaliações Positivas")
        with st.spinner("Gerando word cloud..."):
            wordclouds = wc_generator.generate_by_sentiment(
                texto_positivo, texto_negativo
            )

            fig_pos = wc_generator.to_matplotlib_figure(
                wordclouds['positivo'],
                "Palavras mais frequentes (Positivo)"
            )
            st.pyplot(fig_pos)

    with col_wc2:
        st.subheader("😞 Avaliações Negativas")
        with st.spinner("Gerando word cloud..."):
            fig_neg = wc_generator.to_matplotlib_figure(
                wordclouds['negativo'],
                "Palavras mais frequentes (Negativo)"
            )
            st.pyplot(fig_neg)

    st.divider()

    # Top palavras
    st.subheader("🔤 Top Palavras por Sentimento")

    col_top1, col_top2 = st.columns(2)

    with col_top1:
        st.markdown("### 👍 Positivas")
        top_pos = wc_generator.get_top_words(texto_positivo, n=15)
        fig_bar_pos = DashboardCharts.word_frequency_bar(
            top_pos, title="Top 15 Palavras (Positivo)"
        )
        st.plotly_chart(fig_bar_pos, use_container_width=True)

    with col_top2:
        st.markdown("### 👎 Negativas")
        top_neg = wc_generator.get_top_words(texto_negativo, n=15)
        fig_bar_neg = DashboardCharts.word_frequency_bar(
            top_neg, title="Top 15 Palavras (Negativo)"
        )
        st.plotly_chart(fig_bar_neg, use_container_width=True)

# ========== TAB 3: EXPLORADOR ==========
with tab3:
    st.header("🔍 Explorador de Avaliações")

    # Filtros
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        sent_filter = st.selectbox(
            "Sentimento",
            ["Todos", "positivo", "negativo"]
        )

    with col_f2:
        nota_filter_exp = st.multiselect(
            "Nota",
            options=[1, 2, 3, 4, 5],
            default=[1, 2, 3, 4, 5]
        )

    with col_f3:
        if 'categoria' in df.columns:
            cat_filter = st.selectbox(
                "Categoria",
                ["Todas"] + df['categoria'].unique().tolist()
            )

    # Aplicar filtros
    df_filtered = df.copy()

    if sent_filter != "Todos":
        df_filtered = df_filtered[df_filtered['sentimento'] == sent_filter]

    df_filtered = df_filtered[df_filtered['nota'].isin(nota_filter_exp)]

    if 'categoria' in df.columns and cat_filter != "Todas":
        df_filtered = df_filtered[df_filtered['categoria'] == cat_filter]

    st.info(f"Mostrando {len(df_filtered)} de {len(df)} avaliações")

    # Busca por palavra-chave
    search_term = st.text_input("🔍 Buscar por palavra-chave na avaliação:")

    if search_term:
        df_filtered = df_filtered[
            df_filtered['avaliacao'].str.contains(search_term, case=False, na=False)
        ]
        st.success(f"Encontradas {len(df_filtered)} avaliações com '{search_term}'")

    # Exibir avaliações
    num_display = st.slider("Número de avaliações a exibir", 5, 50, 20)

    df_display = df_filtered.head(num_display)

    for idx, row in df_display.iterrows():
        sentiment_emoji = "😊" if row['sentimento'] == 'positivo' else "😞"
        star_rating = "⭐" * int(row['nota'])

        with st.expander(
            f"{sentiment_emoji} {star_rating} | Categoria: {row.get('categoria', 'N/A')}"
        ):
            st.markdown(row['avaliacao'])

st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 <i>Análise baseada em processamento de linguagem natural</i></p>
</div>
""", unsafe_allow_html=True)
