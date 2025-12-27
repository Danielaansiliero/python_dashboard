"""
Módulo para limpeza e normalização de textos de avaliações em português brasileiro.
"""
import re
import unicodedata
from typing import List
import pandas as pd


class TextCleaner:
    """Limpeza e normalização de textos de avaliações em português."""

    # Stopwords específicas para e-commerce brasileiro
    ECOMMERCE_STOPWORDS = {
        'o', 'a', 'de', 'da', 'do', 'em', 'para', 'com', 'por', 'no', 'na',
        'os', 'as', 'dos', 'das', 'um', 'uma', 'ao', 'aos', 'à', 'às',
        'produto', 'comprei', 'compra', 'chegou', 'recebi', 'entrega',
        'prazo', 'site', 'loja', 'e', 'que', 'mais', 'muito', 'bem',
        'quando', 'como', 'também', 'já', 'está', 'foi', 'ser', 'ter'
    }

    # Contrações comuns em português
    CONTRACTIONS = {
        'tá': 'está',
        'pra': 'para',
        'pro': 'para o',
        'né': 'não é',
        'vc': 'você',
        'vcs': 'vocês',
        'mt': 'muito',
        'mto': 'muito',
        'tb': 'também',
        'tbm': 'também',
        'q': 'que',
        'oq': 'o que',
        'pq': 'porque',
        'td': 'tudo',
        'blz': 'beleza',
        'vlw': 'valeu'
    }

    def clean_text(self, text: str) -> str:
        """
        Pipeline completo de limpeza de texto.

        Args:
            text: Texto a ser limpo

        Returns:
            Texto limpo e normalizado
        """
        if pd.isna(text):
            return ""

        text = str(text).lower()
        text = self._remove_urls(text)
        text = self._remove_emails(text)
        text = self._expand_contractions(text)
        text = self._normalize_unicode(text)
        text = self._remove_special_chars(text)
        text = self._remove_extra_spaces(text)

        return text.strip()

    def _remove_urls(self, text: str) -> str:
        """Remove URLs do texto."""
        return re.sub(r'https?://\S+|www\.\S+', '', text)

    def _remove_emails(self, text: str) -> str:
        """Remove emails do texto."""
        return re.sub(r'\S+@\S+', '', text)

    def _expand_contractions(self, text: str) -> str:
        """Expande contrações comuns em português."""
        words = text.split()
        expanded = [self.CONTRACTIONS.get(word, word) for word in words]
        return ' '.join(expanded)

    def _normalize_unicode(self, text: str) -> str:
        """Normaliza caracteres Unicode."""
        # Mantém acentos, apenas normaliza a forma
        return unicodedata.normalize('NFKC', text)

    def _remove_special_chars(self, text: str) -> str:
        """Remove caracteres especiais mantendo espaços e acentos."""
        # Mantém letras, números, espaços e pontuação básica
        text = re.sub(r'[^\w\s!?.,áàâãéèêíïóôõöúçñ-]', '', text)
        # Remove pontuação extra
        text = re.sub(r'[!?.,-]{2,}', ' ', text)
        return text

    def _remove_extra_spaces(self, text: str) -> str:
        """Remove espaços extras."""
        return re.sub(r'\s+', ' ', text)

    def tokenize_for_analysis(self, text: str,
                               remove_stopwords: bool = True) -> List[str]:
        """
        Tokeniza texto para análise.

        Args:
            text: Texto a ser tokenizado
            remove_stopwords: Se True, remove stopwords

        Returns:
            Lista de tokens
        """
        tokens = text.split()
        if remove_stopwords:
            tokens = [t for t in tokens if t not in self.ECOMMERCE_STOPWORDS]
        # Remove tokens muito curtos
        return [t for t in tokens if len(t) > 2]

    def extract_emojis(self, text: str) -> List[str]:
        """
        Extrai emojis do texto.

        Args:
            text: Texto contendo emojis

        Returns:
            Lista de emojis encontrados
        """
        # Padrão para detectar emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # símbolos & pictogramas
            "\U0001F680-\U0001F6FF"  # transporte & símbolos de mapas
            "\U0001F1E0-\U0001F1FF"  # bandeiras
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.findall(text)
