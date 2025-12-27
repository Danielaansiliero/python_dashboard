"""
Módulo de visualizações com gráficos Plotly para o dashboard.
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional


class DashboardCharts:
    """Gráficos reutilizáveis para o dashboard."""

    # Paleta de cores consistente
    COLORS = {
        'positivo': '#2ecc71',
        'negativo': '#e74c3c',
        'neutro': '#95a5a6',
        'primary': '#3498db',
        'secondary': '#9b59b6',
        'accent': '#f39c12',
        'warning': '#e67e22',
        'success': '#27ae60',
        'danger': '#c0392b'
    }

    RATING_COLORS = {
        1: '#e74c3c',
        2: '#e67e22',
        3: '#f1c40f',
        4: '#27ae60',
        5: '#2ecc71'
    }

    @staticmethod
    def sentiment_donut(df: pd.DataFrame) -> go.Figure:
        """
        Gráfico de rosca para distribuição de sentimentos.

        Args:
            df: DataFrame com coluna 'sentimento'

        Returns:
            Figure do Plotly
        """
        sentiment_counts = df['sentimento'].value_counts()

        colors = [
            DashboardCharts.COLORS.get(s.lower(), '#95a5a6')
            for s in sentiment_counts.index
        ]

        fig = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.6,
            marker_colors=colors,
            textinfo='percent+label',
            textposition='outside',
            hovertemplate='%{label}<br>%{value} avaliações<br>%{percent}<extra></extra>'
        )])

        fig.update_layout(
            showlegend=False,
            annotations=[{
                'text': f'<b>{len(df):,}</b><br>avaliações',
                'x': 0.5, 'y': 0.5,
                'font_size': 16,
                'showarrow': False
            }],
            margin=dict(t=20, b=20, l=20, r=20),
            height=300
        )

        return fig

    @staticmethod
    def rating_distribution(df: pd.DataFrame) -> go.Figure:
        """
        Histograma de distribuição de notas.

        Args:
            df: DataFrame com coluna 'nota'

        Returns:
            Figure do Plotly
        """
        rating_counts = df['nota'].value_counts().sort_index()

        fig = go.Figure(data=[
            go.Bar(
                x=rating_counts.index,
                y=rating_counts.values,
                marker_color=[
                    DashboardCharts.RATING_COLORS.get(r, '#95a5a6')
                    for r in rating_counts.index
                ],
                text=rating_counts.values,
                textposition='outside',
                hovertemplate='Nota %{x}<br>%{y} avaliações<extra></extra>'
            )
        ])

        fig.update_layout(
            xaxis_title='Nota',
            yaxis_title='Quantidade de Avaliações',
            xaxis=dict(tickmode='linear', tick0=1, dtick=1),
            showlegend=False,
            margin=dict(t=30, b=50),
            height=300
        )

        return fig

    @staticmethod
    def sentiment_by_rating_heatmap(df: pd.DataFrame) -> go.Figure:
        """
        Heatmap mostrando relação entre nota e sentimento.

        Args:
            df: DataFrame com colunas 'nota' e 'sentimento'

        Returns:
            Figure do Plotly
        """
        pivot = pd.crosstab(df['nota'], df['sentimento'], normalize='index') * 100

        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='RdYlGn',
            text=pivot.values.round(1),
            texttemplate='%{text}%',
            textfont={"size": 12},
            showscale=True,
            hovertemplate='Nota %{y}<br>%{x}<br>%{z:.1f}%<extra></extra>'
        ))

        fig.update_layout(
            xaxis_title='Sentimento',
            yaxis_title='Nota',
            yaxis=dict(tickmode='linear'),
            height=300
        )

        return fig

    @staticmethod
    def category_comparison(df: pd.DataFrame,
                           category_col: str = 'categoria') -> go.Figure:
        """
        Comparação de métricas por categoria.

        Args:
            df: DataFrame com categoria, nota e sentimento
            category_col: Nome da coluna de categoria

        Returns:
            Figure do Plotly
        """
        if category_col not in df.columns:
            # Retorna figura vazia se categoria não existe
            return go.Figure()

        category_stats = df.groupby(category_col).agg({
            'nota': 'mean',
            'sentimento': lambda x: (x == 'positivo').mean() * 100,
            category_col: 'count'
        }).round(2)

        category_stats.columns = ['Nota Media', '% Positivo', 'Contagem']
        category_stats = category_stats.sort_values('Nota Media', ascending=True)

        # Filtra categorias com pelo menos 10 avaliações
        category_stats = category_stats[category_stats['Contagem'] >= 10]

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Nota Média por Categoria', '% Positivo por Categoria'),
            shared_yaxes=True
        )

        fig.add_trace(
            go.Bar(
                y=category_stats.index,
                x=category_stats['Nota Media'],
                orientation='h',
                marker_color=DashboardCharts.COLORS['primary'],
                name='Nota',
                text=category_stats['Nota Media'].round(2),
                textposition='outside',
                hovertemplate='%{y}<br>Nota: %{x:.2f}<extra></extra>'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                y=category_stats.index,
                x=category_stats['% Positivo'],
                orientation='h',
                marker_color=DashboardCharts.COLORS['positivo'],
                name='% Positivo',
                text=category_stats['% Positivo'].round(1),
                textposition='outside',
                hovertemplate='%{y}<br>Positivo: %{x:.1f}%<extra></extra>'
            ),
            row=1, col=2
        )

        fig.update_layout(
            height=max(400, len(category_stats) * 40),
            showlegend=False,
            margin=dict(l=150)
        )

        return fig

    @staticmethod
    def churn_gauge(churn_percentage: float) -> go.Figure:
        """
        Gauge para indicador de risco de churn.

        Args:
            churn_percentage: Percentual de alto risco

        Returns:
            Figure do Plotly
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=churn_percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "% Alto Risco de Churn"},
            delta={'reference': 10, 'increasing': {'color': "red"}},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkred"},
                'steps': [
                    {'range': [0, 10], 'color': DashboardCharts.COLORS['success']},
                    {'range': [10, 25], 'color': DashboardCharts.COLORS['warning']},
                    {'range': [25, 100], 'color': DashboardCharts.COLORS['danger']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': churn_percentage
                }
            }
        ))

        fig.update_layout(
            height=250,
            margin=dict(t=40, b=20, l=20, r=20)
        )

        return fig

    @staticmethod
    def opportunity_gauge(opportunity_percentage: float) -> go.Figure:
        """
        Gauge para indicador de oportunidades.

        Args:
            opportunity_percentage: Percentual de alta oportunidade

        Returns:
            Figure do Plotly
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=opportunity_percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "% Alta Oportunidade"},
            delta={'reference': 20, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 15], 'color': DashboardCharts.COLORS['danger']},
                    {'range': [15, 30], 'color': DashboardCharts.COLORS['warning']},
                    {'range': [30, 100], 'color': DashboardCharts.COLORS['success']}
                ],
                'threshold': {
                    'line': {'color': "green", 'width': 4},
                    'thickness': 0.75,
                    'value': opportunity_percentage
                }
            }
        ))

        fig.update_layout(
            height=250,
            margin=dict(t=40, b=20, l=20, r=20)
        )

        return fig

    @staticmethod
    def word_frequency_bar(word_counts: Dict[str, int], top_n: int = 15,
                          title: str = "Palavras Mais Frequentes") -> go.Figure:
        """
        Gráfico de barras com palavras mais frequentes.

        Args:
            word_counts: Dicionário palavra -> contagem
            top_n: Número de palavras a exibir
            title: Título do gráfico

        Returns:
            Figure do Plotly
        """
        # Ordena e pega top N
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1],
                             reverse=True)[:top_n]
        words, counts = zip(*sorted_words) if sorted_words else ([], [])

        fig = go.Figure(data=[
            go.Bar(
                y=list(words),
                x=list(counts),
                orientation='h',
                marker_color=DashboardCharts.COLORS['secondary'],
                text=list(counts),
                textposition='outside'
            )
        ])

        fig.update_layout(
            title=title,
            xaxis_title='Frequência',
            yaxis_title='',
            showlegend=False,
            height=max(400, top_n * 30),
            margin=dict(l=120)
        )

        # Inverte eixo Y para mostrar maior no topo
        fig.update_yaxes(autorange="reversed")

        return fig

    @staticmethod
    def category_pie(df: pd.DataFrame, category_col: str = 'categoria') -> go.Figure:
        """
        Gráfico de pizza para distribuição de categorias.

        Args:
            df: DataFrame com coluna de categoria
            category_col: Nome da coluna

        Returns:
            Figure do Plotly
        """
        if category_col not in df.columns:
            return go.Figure()

        category_counts = df[category_col].value_counts()

        fig = go.Figure(data=[go.Pie(
            labels=category_counts.index,
            values=category_counts.values,
            textinfo='label+percent',
            hovertemplate='%{label}<br>%{value} avaliações<extra></extra>'
        )])

        fig.update_layout(
            title='Distribuição por Categoria',
            showlegend=True,
            height=400,
            margin=dict(t=50, b=20, l=20, r=20)
        )

        return fig
