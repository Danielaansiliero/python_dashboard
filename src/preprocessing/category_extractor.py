"""
Módulo para extração de categorias de produtos a partir de avaliações.
"""
import re
from typing import Dict, List, Tuple
from collections import Counter


class CategoryExtractor:
    """Extrai categorias de produtos a partir do texto das avaliações."""

    # Dicionário de categorias e suas palavras-chave
    CATEGORY_KEYWORDS = {
        'Smartphones': [
            'celular', 'smartphone', 'iphone', 'samsung', 'motorola',
            'moto g', 'galaxy', 'xiaomi', 'android', 'ios', 'fone',
            'bateria', 'camera', 'aplicativo', 'tela touch'
        ],
        'Notebooks e Computadores': [
            'notebook', 'laptop', 'computador', 'pc', 'desktop',
            'processador', 'memoria ram', 'ssd', 'hd', 'windows',
            'placa de video', 'cooler'
        ],
        'TVs e Monitores': [
            'tv', 'televisao', 'monitor', 'smart tv', 'led', 'lcd',
            '4k', 'hdmi', 'polegadas', 'controle remoto', 'netflix',
            'youtube', 'tela grande'
        ],
        'Eletrodomésticos': [
            'geladeira', 'freezer', 'microondas', 'fogao', 'forno',
            'liquidificador', 'batedeira', 'aspirador', 'lavadora',
            'ferro de passar', 'ar condicionado', 'ventilador', 'aquecedor'
        ],
        'Móveis': [
            'sofa', 'cama', 'colchao', 'mesa', 'cadeira', 'estante',
            'guarda-roupa', 'armario', 'rack', 'estofado', 'madeira',
            'movel', 'comoda'
        ],
        'Beleza e Saúde': [
            'shampoo', 'condicionador', 'perfume', 'maquiagem', 'creme',
            'protetor', 'cabelo', 'pele', 'hidratante', 'sabonete',
            'esmalte', 'batom', 'cosmetico'
        ],
        'Livros e Mídia': [
            'livro', 'romance', 'autor', 'paginas', 'leitura', 'historia',
            'capitulo', 'cd', 'dvd', 'filme', 'blu-ray'
        ],
        'Esporte e Lazer': [
            'bicicleta', 'bike', 'tenis', 'corrida', 'academia', 'peso',
            'exercicio', 'bola', 'esporte', 'treino'
        ],
        'Moda e Vestuário': [
            'roupa', 'camiseta', 'calca', 'vestido', 'sapato', 'bolsa',
            'tecido', 'tamanho', 'cor', 'estampa', 'moda'
        ],
        'Casa e Decoração': [
            'panela', 'cozinha', 'decoracao', 'quadro', 'vaso', 'tapete',
            'cortina', 'almofada', 'luminaria'
        ],
        'Informática e Acessórios': [
            'mouse', 'teclado', 'headset', 'webcam', 'impressora',
            'pen drive', 'cabo usb', 'adaptador', 'carregador'
        ]
    }

    def __init__(self):
        """Inicializa o extrator de categorias."""
        pass

    def extract_category(self, text: str) -> Tuple[str, float]:
        """
        Identifica a categoria do produto com score de confiança.

        Args:
            text: Texto da avaliação

        Returns:
            Tupla (categoria, confiança) onde confiança é um valor entre 0 e 1
        """
        if not text or not isinstance(text, str):
            return ('Outros', 0.0)

        text_lower = text.lower()
        scores = {}

        # Calcula score para cada categoria
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[category] = score

        # Se não encontrou nenhuma categoria
        if not scores:
            return ('Outros', 0.0)

        # Retorna a categoria com maior score
        best_category = max(scores, key=scores.get)
        # Confiança baseada no número de matches (normalizado)
        confidence = min(scores[best_category] / 3, 1.0)

        return (best_category, confidence)

    def extract_product_mentions(self, text: str) -> List[str]:
        """
        Extrai menções a produtos específicos.

        Args:
            text: Texto da avaliação

        Returns:
            Lista de produtos mencionados
        """
        if not text or not isinstance(text, str):
            return []

        text_lower = text.lower()
        mentions = []

        # Padrões para capturar nomes de produtos/marcas
        patterns = [
            r'\b(samsung|apple|lg|motorola|xiaomi|sony|philips|brastemp|consul)\b',
            r'\b(galaxy|iphone|moto g|redmi|positivo)\s*\w*\b',
            r'\b(\w+\s*\d{2,4})\b'  # Padrões como "Galaxy A5", "TV 55"
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            mentions.extend(matches)

        # Remove duplicatas mantendo ordem
        seen = set()
        unique_mentions = []
        for mention in mentions:
            if mention not in seen and len(mention) > 2:
                seen.add(mention)
                unique_mentions.append(mention)

        return unique_mentions[:5]  # Limita a 5 menções mais relevantes

    def get_category_distribution(self, texts: List[str]) -> Dict[str, int]:
        """
        Calcula a distribuição de categorias em uma lista de textos.

        Args:
            texts: Lista de textos de avaliações

        Returns:
            Dicionário com contagem por categoria
        """
        categories = [self.extract_category(text)[0] for text in texts]
        return dict(Counter(categories))

    def get_all_categories(self) -> List[str]:
        """
        Retorna lista de todas as categorias disponíveis.

        Returns:
            Lista de nomes de categorias
        """
        return list(self.CATEGORY_KEYWORDS.keys()) + ['Outros']
