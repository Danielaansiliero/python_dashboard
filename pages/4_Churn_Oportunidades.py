"""
Página de Análise de Churn e Oportunidades
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.analysis.churn_detector import ChurnDetector
from src.analysis.opportunity_finder import OpportunityFinder
from src.preprocessing.text_cleaner import TextCleaner
from src.preprocessing.category_extractor import CategoryExtractor
from src.visualization.charts import DashboardCharts
from src.visualization.wordcloud_gen import WordCloudGenerator

st.set_page_config(page_title="Churn & Oportunidades", page_icon="🎯", layout="wide")


@st.cache_data
def load_and_process_data():
    """Carrega e processa dados."""
    df = pd.read_csv('data/dataset_avaliacoes.csv')

    # Processadores
    text_cleaner = TextCleaner()
    category_extractor = CategoryExtractor()

    df['avaliacao_limpa'] = df['avaliacao'].apply(text_cleaner.clean_text)
    df[['categoria', 'categoria_confianca']] = df['avaliacao_limpa'].apply(
        lambda x: pd.Series(category_extractor.extract_category(x))
    )

    return df


st.title("🎯 Análise de Churn e Oportunidades")
st.markdown("""
Identifique **clientes em risco** de abandono e **oportunidades de crescimento**
através de análise avançada de sentimentos e padrões textuais.
""")

# Disclaimer
st.info("""
ℹ️ **Aviso:** Esta análise é baseada em dados educacionais anônimos e tem finalidade demonstrativa.
Os scores de churn e oportunidades são gerados por algoritmos de NLP para fins acadêmicos.
""")

st.divider()

# Carrega dados
df = load_and_process_data()

# Detectores
churn_detector = ChurnDetector()
opportunity_finder = OpportunityFinder()

# Tabs principais
tab_churn, tab_opportunities, tab_combined = st.tabs([
    "⚠️ Risco de Churn",
    "💡 Oportunidades",
    "📊 Visão Combinada"
])

# ========== TAB: RISCO DE CHURN ==========
with tab_churn:
    st.header("⚠️ Análise de Risco de Churn")

    # Aplica detecção de churn
    with st.spinner("Analisando riscos de churn..."):
        df['churn_analysis'] = df.apply(
            lambda row: churn_detector.detect_churn_risk(
                row['avaliacao'],
                row['nota'],
                row['sentimento']
            ),
            axis=1
        )

    df['churn_score'] = df['churn_analysis'].apply(lambda x: x['churn_score'])
    df['risk_level'] = df['churn_analysis'].apply(lambda x: x['risk_level'])

    # KPIs de Churn
    col1, col2, col3, col4 = st.columns(4)

    alto_risco = (df['risk_level'] == 'alto_risco').sum()
    medio_risco = (df['risk_level'] == 'medio_risco').sum()
    baixo_risco = (df['risk_level'] == 'baixo_risco').sum()
    score_medio = df['churn_score'].mean()

    with col1:
        st.metric("🔴 Alto Risco", alto_risco,
                 delta=f"{(alto_risco/len(df)*100):.1f}%")

    with col2:
        st.metric("🟡 Médio Risco", medio_risco,
                 delta=f"{(medio_risco/len(df)*100):.1f}%")

    with col3:
        st.metric("🟢 Baixo Risco", baixo_risco,
                 delta=f"{(baixo_risco/len(df)*100):.1f}%")

    with col4:
        st.metric("📊 Score Médio", f"{score_medio:.1f}")

    st.divider()

    # Gauge de risco
    col_gauge1, col_gauge2 = st.columns(2)

    with col_gauge1:
        pct_alto_risco = (alto_risco / len(df)) * 100
        fig_gauge = DashboardCharts.churn_gauge(pct_alto_risco)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_gauge2:
        st.subheader("📋 Distribuição de Risco")
        risk_dist = df['risk_level'].value_counts()
        fig_risk = DashboardCharts.sentiment_donut(
            pd.DataFrame({'sentimento': df['risk_level']})
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    st.divider()

    # Avaliações críticas
    st.subheader("🚨 Avaliações Críticas (Alto Risco)")

    df_alto_risco = df[df['risk_level'] == 'alto_risco'].copy()
    df_alto_risco = df_alto_risco.sort_values('churn_score', ascending=False)

    if len(df_alto_risco) > 0:
        # Filtros
        col_f1, col_f2 = st.columns(2)

        with col_f1:
            top_n = st.slider("Número de avaliações a exibir", 5, 50, 10)

        with col_f2:
            min_score = st.slider("Score mínimo de churn", 0, 100,
                                 int(df_alto_risco['churn_score'].min()))

        df_display = df_alto_risco[df_alto_risco['churn_score'] >= min_score].head(top_n)

        for idx, row in df_display.iterrows():
            with st.expander(
                f"⚠️ Score: {row['churn_score']:.1f} | Nota: {row['nota']} | "
                f"Categoria: {row['categoria']}"
            ):
                st.markdown(f"**Avaliação:**")
                st.info(row['avaliacao'])

                analysis = row['churn_analysis']
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("**Aspectos Problemáticos:**")
                    if analysis['problem_aspects']:
                        for aspect in analysis['problem_aspects']:
                            st.markdown(f"- {aspect}")
                    else:
                        st.markdown("_Nenhum aspecto específico detectado_")

                with col_b:
                    st.markdown("**Principais Motivos:**")
                    if analysis['main_reasons']:
                        for reason in analysis['main_reasons']:
                            st.markdown(f"- _{reason}_")
                    else:
                        st.markdown("_Sinais gerais de insatisfação_")

    else:
        st.success("✅ Nenhuma avaliação com alto risco de churn encontrada!")

# ========== TAB: OPORTUNIDADES ==========
with tab_opportunities:
    st.header("💡 Oportunidades de Crescimento")

    # Aplica detecção de oportunidades
    with st.spinner("Identificando oportunidades..."):
        df['opportunity_analysis'] = df.apply(
            lambda row: opportunity_finder.find_opportunities(
                row['avaliacao'],
                row['nota'],
                row['sentimento']
            ),
            axis=1
        )

    df['opportunity_score'] = df['opportunity_analysis'].apply(
        lambda x: x['opportunity_score']
    )
    df['opportunity_level'] = df['opportunity_analysis'].apply(
        lambda x: x['opportunity_level']
    )
    df['customer_profile'] = df['opportunity_analysis'].apply(
        lambda x: x['customer_profile']
    )

    # KPIs de Oportunidades
    col1, col2, col3, col4 = st.columns(4)

    alta_opp = (df['opportunity_level'] == 'alta_oportunidade').sum()
    media_opp = (df['opportunity_level'] == 'media_oportunidade').sum()
    advogados = (df['customer_profile'] == 'advogado_marca').sum()
    fieis = (df['customer_profile'] == 'cliente_fiel').sum()

    with col1:
        st.metric("🌟 Alta Oportunidade", alta_opp,
                 delta=f"{(alta_opp/len(df)*100):.1f}%")

    with col2:
        st.metric("⭐ Média Oportunidade", media_opp,
                 delta=f"{(media_opp/len(df)*100):.1f}%")

    with col3:
        st.metric("📢 Advogados da Marca", advogados)

    with col4:
        st.metric("💚 Clientes Fiéis", fieis)

    st.divider()

    # Gauge de oportunidades
    col_opp1, col_opp2 = st.columns(2)

    with col_opp1:
        pct_alta_opp = (alta_opp / len(df)) * 100
        fig_opp_gauge = DashboardCharts.opportunity_gauge(pct_alta_opp)
        st.plotly_chart(fig_opp_gauge, use_container_width=True)

    with col_opp2:
        st.subheader("👥 Perfis de Clientes")
        profile_dist = df['customer_profile'].value_counts()
        fig_profiles = DashboardCharts.sentiment_donut(
            pd.DataFrame({'sentimento': df['customer_profile']})
        )
        st.plotly_chart(fig_profiles, use_container_width=True)

    st.divider()

    # Top Oportunidades
    st.subheader("🎯 Top Oportunidades")

    df_oportunidades = df[df['opportunity_score'] > 0].copy()
    df_oportunidades = df_oportunidades.sort_values('opportunity_score',
                                                    ascending=False)

    if len(df_oportunidades) > 0:
        top_opp_n = st.slider("Número de oportunidades a exibir", 5, 30, 10)

        df_top_opp = df_oportunidades.head(top_opp_n)

        for idx, row in df_top_opp.iterrows():
            profile_emoji = {
                'advogado_marca': '📢',
                'cliente_fiel': '💚',
                'altamente_satisfeito': '😊',
                'cliente_satisfeito': '👍',
                'cliente_comum': '👤'
            }

            emoji = profile_emoji.get(row['customer_profile'], '👤')

            with st.expander(
                f"{emoji} Score: {row['opportunity_score']:.1f} | "
                f"Nota: {row['nota']} | Perfil: {row['customer_profile']}"
            ):
                st.markdown(f"**Avaliação:**")
                st.success(row['avaliacao'])

                analysis = row['opportunity_analysis']
                col_x, col_y = st.columns(2)

                with col_x:
                    st.markdown("**Tipos de Oportunidade:**")
                    if analysis['opportunity_types']:
                        for opp_type in analysis['opportunity_types']:
                            st.markdown(f"- {opp_type}")
                    else:
                        st.markdown("_Cliente satisfeito_")

                with col_y:
                    st.markdown("**Sinais Detectados:**")
                    signals = analysis['signals_detected']
                    for key, value in signals.items():
                        if value > 0:
                            st.markdown(f"- {key}: {value}")

    else:
        st.info("Nenhuma oportunidade significativa detectada.")

# ========== TAB: VISÃO COMBINADA ==========
with tab_combined:
    st.header("📊 Visão Combinada: Churn vs Oportunidades")

    col_comb1, col_comb2 = st.columns(2)

    with col_comb1:
        st.subheader("Resumo de Churn")
        st.metric("Total em Risco", alto_risco + medio_risco)
        st.metric("Taxa de Risco Crítico", f"{(alto_risco/len(df)*100):.2f}%")

    with col_comb2:
        st.subheader("Resumo de Oportunidades")
        st.metric("Total de Oportunidades", alta_opp + media_opp)
        st.metric("Taxa de Alta Oportunidade", f"{(alta_opp/len(df)*100):.2f}%")

    st.divider()

    # Análise por categoria
    st.subheader("📈 Análise por Categoria")

    if 'categoria' in df.columns:
        cat_analysis = df.groupby('categoria').agg({
            'churn_score': 'mean',
            'opportunity_score': 'mean',
            'categoria': 'count'
        }).round(2)

        cat_analysis.columns = ['Churn Médio', 'Oportunidade Média', 'Total']
        cat_analysis = cat_analysis[cat_analysis['Total'] >= 10]
        cat_analysis = cat_analysis.sort_values('Churn Médio', ascending=False)

        st.dataframe(
            cat_analysis,
            use_container_width=True,
            column_config={
                "Churn Médio": st.column_config.ProgressColumn(
                    "Churn Médio",
                    format="%.1f",
                    min_value=0,
                    max_value=100,
                ),
                "Oportunidade Média": st.column_config.ProgressColumn(
                    "Oportunidade Média",
                    format="%.1f",
                    min_value=0,
                    max_value=100,
                ),
            }
        )

    st.divider()

    # Recomendações
    st.subheader("💡 Recomendações Estratégicas")

    col_rec1, col_rec2 = st.columns(2)

    with col_rec1:
        st.markdown("### ⚠️ Ações Anti-Churn")
        st.markdown(f"""
        1. **Priorizar {alto_risco} clientes** em alto risco
        2. Investigar aspectos mais problemáticos
        3. Implementar recuperação proativa
        4. Monitorar categorias com maior churn
        """)

    with col_rec2:
        st.markdown("### 🚀 Ações de Crescimento")
        st.markdown(f"""
        1. **Engajar {advogados} advogados** da marca
        2. Criar programas de fidelidade para {fieis} clientes fiéis
        3. Incentivar cross-sell e upsell
        4. Solicitar referências de clientes satisfeitos
        """)

st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 <i>Análise baseada em padrões de linguagem natural e scores ponderados</i></p>
</div>
""", unsafe_allow_html=True)
