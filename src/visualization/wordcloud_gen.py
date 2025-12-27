"""
Módulo para geração de nuvens de palavras customizadas.
"""
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import Dict, Optional
import numpy as np
from collections import Counter


class WordCloudGenerator:
    """Geração de nuvens de palavras customizadas."""

    # Stopwords para português brasileiro
    STOPWORDS_PT = {
        'o', 'a', 'os', 'as', 'de', 'da', 'do', 'das', 'dos',
        'um', 'uma', 'uns', 'umas', 'em', 'no', 'na', 'nos', 'nas',
        'para', 'com', 'sem', 'por', 'ao', 'aos', 'à', 'às',
        'e', 'ou', 'que', 'mais', 'muito', 'bem', 'já', 'também',
        'quando', 'como', 'está', 'foi', 'ser', 'ter', 'seu', 'sua',
        'produto', 'compra', 'comprei', 'chegou', 'recebi', 'entrega',
        'site', 'loja', 'prazo', 'recomendo', 'não', 'sim'
    }

    def __init__(self):
        """Inicializa o gerador de word clouds."""
        self.default_config = {
            'width': 800,
            'height': 400,
            'background_color': 'white',
            'max_words': 100,
            'collocations': False,
            'min_font_size': 10,
            'stopwords': self.STOPWORDS_PT,
            'relative_scaling': 0.5
        }

    def generate(self, text: str, **kwargs) -> WordCloud:
        """
        Gera word cloud a partir de texto.

        Args:
            text: Texto para gerar a word cloud
            **kwargs: Configurações adicionais

        Returns:
            Objeto WordCloud
        """
        config = self.default_config.copy()
        config.update(kwargs)

        wc = WordCloud(**config)
        return wc.generate(text)

    def generate_by_sentiment(self, positive_text: str,
                              negative_text: str) -> Dict[str, WordCloud]:
        """
        Gera word clouds separadas por sentimento.

        Args:
            positive_text: Texto das avaliações positivas
            negative_text: Texto das avaliações negativas

        Returns:
            Dicionário com word clouds por sentimento
        """
        def green_color_func(*args, **kwargs):
            """Função de cor verde para sentimentos positivos."""
            return f"hsl(140, 70%, {np.random.randint(25, 50)}%)"

        def red_color_func(*args, **kwargs):
            """Função de cor vermelha para sentimentos negativos."""
            return f"hsl(0, 70%, {np.random.randint(30, 55)}%)"

        positive_wc = self.generate(
            positive_text,
            color_func=green_color_func
        )

        negative_wc = self.generate(
            negative_text,
            color_func=red_color_func
        )

        return {
            'positivo': positive_wc,
            'negativo': negative_wc
        }

    def generate_by_category(self, texts_by_category: Dict[str, str]) -> Dict[str, WordCloud]:
        """
        Gera word clouds para cada categoria.

        Args:
            texts_by_category: Dicionário categoria -> texto

        Returns:
            Dicionário categoria -> WordCloud
        """
        wordclouds = {}

        for category, text in texts_by_category.items():
            if text and len(text.strip()) > 0:
                wordclouds[category] = self.generate(text)

        return wordclouds

    def get_top_words(self, text: str, n: int = 20) -> Dict[str, int]:
        """
        Extrai as N palavras mais frequentes do texto.

        Args:
            text: Texto para análise
            n: Número de palavras a retornar

        Returns:
            Dicionário palavra -> frequência
        """
        # Remove stopwords e tokeniza
        words = text.lower().split()
        words = [w for w in words
                if w not in self.STOPWORDS_PT and len(w) > 2]

        # Conta frequência
        word_counts = Counter(words)

        # Retorna top N
        return dict(word_counts.most_common(n))

    def to_matplotlib_figure(self, wordcloud: WordCloud,
                            title: str = "") -> plt.Figure:
        """
        Converte word cloud para figura matplotlib.

        Args:
            wordcloud: Objeto WordCloud
            title: Título da figura

        Returns:
            Figura matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_title(title, fontsize=16, pad=20)
        ax.axis('off')
        plt.tight_layout()

        return fig

    def create_comparison_figure(self, wordclouds: Dict[str, WordCloud]) -> plt.Figure:
        """
        Cria figura com múltiplas word clouds para comparação.

        Args:
            wordclouds: Dicionário nome -> WordCloud

        Returns:
            Figura matplotlib com subplots
        """
        n_clouds = len(wordclouds)
        if n_clouds == 0:
            return plt.figure()

        # Define layout de subplots
        if n_clouds == 2:
            rows, cols = 1, 2
        elif n_clouds <= 4:
            rows, cols = 2, 2
        else:
            rows = (n_clouds + 2) // 3
            cols = 3

        fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))

        # Garante que axes seja sempre array
        if n_clouds == 1:
            axes = np.array([axes])
        axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

        # Plota cada word cloud
        for idx, (name, wc) in enumerate(wordclouds.items()):
            if idx < len(axes):
                axes[idx].imshow(wc, interpolation='bilinear')
                axes[idx].set_title(name, fontsize=14, pad=10)
                axes[idx].axis('off')

        # Remove subplots vazios
        for idx in range(len(wordclouds), len(axes)):
            fig.delaxes(axes[idx])

        plt.tight_layout()
        return fig
