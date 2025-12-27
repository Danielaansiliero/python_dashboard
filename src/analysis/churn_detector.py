"""
Módulo para detecção de risco de churn a partir de avaliações negativas.
"""
from typing import Dict, Tuple, List
import pandas as pd


class ChurnDetector:
    """Detecta sinais de risco de churn em avaliações de clientes."""

    # Sinais de churn categorizados por gravidade
    CHURN_SIGNALS = {
        'alta': [
            'nunca mais', 'não compro', 'não volto', 'péssimo', 'golpe',
            'fraude', 'processarei', 'procon', 'juizado', 'reclame aqui',
            'cancelei', 'devolvi', 'não recomendo', 'horrível', 'lixo',
            'pior compra', 'arrependimento total', 'dinheiro jogado fora'
        ],
        'media': [
            'decepcionado', 'decepção', 'arrependido', 'arrependimento',
            'não vale', 'não recomendo', 'insatisfeito', 'frustrado',
            'esperava mais', 'propaganda enganosa', 'mentira', 'enganação',
            'não presta', 'muito ruim', 'mal feito'
        ],
        'baixa': [
            'poderia ser melhor', 'esperava mais', 'deixou a desejar',
            'não é o que parece', 'não gostei', 'não atendeu',
            'demora', 'demorado', 'atraso', 'atrasado'
        ]
    }

    # Aspectos problemáticos
    PROBLEM_ASPECTS = {
        'qualidade': [
            'quebrou', 'defeito', 'quebrado', 'estragou', 'não funciona',
            'parou de funcionar', 'ruim', 'fraco', 'frágil', 'mal feito'
        ],
        'entrega': [
            'não chegou', 'não recebi', 'atraso', 'demora', 'perdido',
            'extraviado', 'atrasado', 'prazo', 'não entregaram'
        ],
        'atendimento': [
            'não respondem', 'mal atendido', 'grosseiro', 'não resolve',
            'não ajuda', 'ignoram', 'não atende', 'péssimo atendimento'
        ],
        'preco': [
            'caro demais', 'muito caro', 'não vale o preço', 'superfaturado',
            'abuso', 'preço abusivo', 'cobrou a mais'
        ]
    }

    def __init__(self):
        """Inicializa o detector de churn."""
        pass

    def detect_churn_risk(self, text: str, rating: int, sentiment: str) -> Dict:
        """
        Detecta o risco de churn baseado na avaliação.

        Args:
            text: Texto da avaliação
            rating: Nota da avaliação (1-5)
            sentiment: Sentimento da avaliação

        Returns:
            Dicionário com análise de risco de churn
        """
        if not text or not isinstance(text, str):
            return self._no_risk_result()

        text_lower = text.lower()

        # Detecta sinais de churn
        alta_count = sum(1 for signal in self.CHURN_SIGNALS['alta']
                         if signal in text_lower)
        media_count = sum(1 for signal in self.CHURN_SIGNALS['media']
                          if signal in text_lower)
        baixa_count = sum(1 for signal in self.CHURN_SIGNALS['baixa']
                          if signal in text_lower)

        # Calcula score de churn (0-100)
        churn_score = (alta_count * 30 + media_count * 15 + baixa_count * 5)
        churn_score = min(churn_score, 100)

        # Ajusta score baseado na nota
        if rating <= 2:
            churn_score = churn_score * 1.5
        elif rating == 3:
            churn_score = churn_score * 1.2
        churn_score = min(churn_score, 100)

        # Detecta aspectos problemáticos
        problem_aspects = self._detect_problem_aspects(text_lower)

        # Classifica o risco
        risk_level = self._classify_risk(churn_score, rating, sentiment)

        # Extrai motivos principais
        main_reasons = self._extract_main_reasons(
            text_lower, alta_count, media_count, baixa_count
        )

        return {
            'churn_score': round(churn_score, 2),
            'risk_level': risk_level,
            'problem_aspects': problem_aspects,
            'main_reasons': main_reasons,
            'signals_detected': {
                'alta_gravidade': alta_count,
                'media_gravidade': media_count,
                'baixa_gravidade': baixa_count
            },
            'is_critical': risk_level == 'alto_risco'
        }

    def _no_risk_result(self) -> Dict:
        """Retorna resultado padrão para sem risco."""
        return {
            'churn_score': 0.0,
            'risk_level': 'sem_risco',
            'problem_aspects': [],
            'main_reasons': [],
            'signals_detected': {
                'alta_gravidade': 0,
                'media_gravidade': 0,
                'baixa_gravidade': 0
            },
            'is_critical': False
        }

    def _classify_risk(self, churn_score: float, rating: int,
                       sentiment: str) -> str:
        """
        Classifica o nível de risco de churn.

        Args:
            churn_score: Score calculado
            rating: Nota da avaliação
            sentiment: Sentimento

        Returns:
            Nível de risco: alto_risco, medio_risco, baixo_risco, sem_risco
        """
        if sentiment == 'positivo' and rating >= 4:
            return 'sem_risco'

        if churn_score >= 40 or (rating <= 2 and churn_score >= 20):
            return 'alto_risco'
        elif churn_score >= 20 or (rating == 3 and churn_score >= 10):
            return 'medio_risco'
        elif churn_score > 0 or rating <= 3:
            return 'baixo_risco'
        else:
            return 'sem_risco'

    def _detect_problem_aspects(self, text: str) -> List[str]:
        """
        Detecta aspectos problemáticos mencionados.

        Args:
            text: Texto da avaliação em lowercase

        Returns:
            Lista de aspectos problemáticos
        """
        aspects_found = []

        for aspect, keywords in self.PROBLEM_ASPECTS.items():
            if any(keyword in text for keyword in keywords):
                aspects_found.append(aspect)

        return aspects_found

    def _extract_main_reasons(self, text: str, alta: int,
                              media: int, baixa: int) -> List[str]:
        """
        Extrai os principais motivos de insatisfação.

        Args:
            text: Texto da avaliação em lowercase
            alta, media, baixa: Contagens de sinais

        Returns:
            Lista de motivos principais
        """
        reasons = []

        # Verifica sinais de alta gravidade
        if alta > 0:
            for signal in self.CHURN_SIGNALS['alta']:
                if signal in text:
                    reasons.append(signal)
                    if len(reasons) >= 3:
                        break

        # Verifica sinais de média gravidade se necessário
        if len(reasons) < 3 and media > 0:
            for signal in self.CHURN_SIGNALS['media']:
                if signal in text:
                    reasons.append(signal)
                    if len(reasons) >= 3:
                        break

        # Verifica sinais de baixa gravidade se necessário
        if len(reasons) < 3 and baixa > 0:
            for signal in self.CHURN_SIGNALS['baixa']:
                if signal in text:
                    reasons.append(signal)
                    if len(reasons) >= 3:
                        break

        return reasons[:3]  # Retorna no máximo 3 motivos

    def get_churn_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calcula estatísticas de churn para um dataset.

        Args:
            df: DataFrame com colunas 'avaliacao', 'nota', 'sentimento'

        Returns:
            Dicionário com estatísticas agregadas
        """
        # Aplica detecção em todo o dataset
        churn_results = df.apply(
            lambda row: self.detect_churn_risk(
                row['avaliacao'],
                row['nota'],
                row['sentimento']
            ),
            axis=1
        )

        # Extrai níveis de risco
        risk_levels = churn_results.apply(lambda x: x['risk_level'])

        return {
            'total_avaliacoes': len(df),
            'alto_risco': (risk_levels == 'alto_risco').sum(),
            'medio_risco': (risk_levels == 'medio_risco').sum(),
            'baixo_risco': (risk_levels == 'baixo_risco').sum(),
            'sem_risco': (risk_levels == 'sem_risco').sum(),
            'percentual_alto_risco': (risk_levels == 'alto_risco').mean() * 100,
            'percentual_medio_risco': (risk_levels == 'medio_risco').mean() * 100,
            'score_medio': churn_results.apply(lambda x: x['churn_score']).mean()
        }
