"""
Módulo para detecção de oportunidades de upsell, cross-sell e fidelização.
"""
from typing import Dict, List
import pandas as pd


class OpportunityFinder:
    """Detecta oportunidades de crescimento a partir de avaliações positivas."""

    # Sinais de oportunidade de upsell
    UPSELL_SIGNALS = [
        'vou comprar', 'comprarei', 'quero comprar', 'vou pegar',
        'versão maior', 'modelo maior', 'próxima compra', 'quero outro',
        'precisando de outro', 'comprar mais', 'já estou de olho',
        'próximo será', 'vou trocar por'
    ]

    # Sinais de cross-sell
    CROSS_SELL_SIGNALS = [
        'combina com', 'agora preciso', 'falta só', 'vou comprar também',
        'agora falta', 'próximo passo', 'agora quero', 'complementa',
        'junto com', 'para acompanhar', 'pensando em pegar'
    ]

    # Sinais de fidelidade
    LOYALTY_SIGNALS = [
        'sempre compro', 'cliente fiel', 'toda vez', 'compro sempre',
        'já é a segunda', 'já é o terceiro', 'compro todo mês',
        'cliente há anos', 'confio', 'só compro aqui', 'minha marca favorita',
        'não troco', 'única loja', 'só compro dessa marca'
    ]

    # Sinais de advogado da marca
    BRAND_ADVOCATE_SIGNALS = [
        'indiquei', 'recomendo', 'recomendei', 'toda família', 'todos da família',
        'todo mundo', 'já indiquei', 'super recomendo', 'recomendo muito',
        'indico', 'todo mundo deveria', 'todos deveriam', 'melhor que existe',
        'não existe melhor', 'compartilhei', 'mostrei para', 'convenci'
    ]

    # Sinais de satisfação excepcional
    EXCEPTIONAL_SATISFACTION = [
        'superou', 'excedeu', 'além das expectativas', 'melhor que esperado',
        'surpreendeu', 'impressionado', 'incrível', 'perfeito', 'impecável',
        'maravilhoso', 'sensacional', 'fantástico', 'excepcional'
    ]

    def __init__(self):
        """Inicializa o detector de oportunidades."""
        pass

    def find_opportunities(self, text: str, rating: int,
                          sentiment: str) -> Dict:
        """
        Detecta oportunidades de negócio na avaliação.

        Args:
            text: Texto da avaliação
            rating: Nota da avaliação (1-5)
            sentiment: Sentimento da avaliação

        Returns:
            Dicionário com análise de oportunidades
        """
        if not text or not isinstance(text, str):
            return self._no_opportunity_result()

        text_lower = text.lower()

        # Conta sinais de cada tipo
        upsell_count = sum(1 for signal in self.UPSELL_SIGNALS
                          if signal in text_lower)
        cross_sell_count = sum(1 for signal in self.CROSS_SELL_SIGNALS
                               if signal in text_lower)
        loyalty_count = sum(1 for signal in self.LOYALTY_SIGNALS
                           if signal in text_lower)
        advocate_count = sum(1 for signal in self.BRAND_ADVOCATE_SIGNALS
                            if signal in text_lower)
        exceptional_count = sum(1 for signal in self.EXCEPTIONAL_SATISFACTION
                               if signal in text_lower)

        # Calcula score de oportunidade (0-100)
        opportunity_score = (
            upsell_count * 20 +
            cross_sell_count * 15 +
            loyalty_count * 25 +
            advocate_count * 30 +
            exceptional_count * 10
        )

        # Bônus para notas altas
        if rating == 5:
            opportunity_score = opportunity_score * 1.3
        elif rating == 4:
            opportunity_score = opportunity_score * 1.1

        opportunity_score = min(opportunity_score, 100)

        # Classifica o nível de oportunidade
        opportunity_level = self._classify_opportunity(
            opportunity_score, rating, sentiment
        )

        # Identifica tipos de oportunidade
        opportunity_types = self._identify_opportunity_types(
            upsell_count, cross_sell_count, loyalty_count,
            advocate_count, exceptional_count
        )

        # Identifica características do cliente
        customer_profile = self._profile_customer(
            loyalty_count, advocate_count, exceptional_count
        )

        return {
            'opportunity_score': round(opportunity_score, 2),
            'opportunity_level': opportunity_level,
            'opportunity_types': opportunity_types,
            'customer_profile': customer_profile,
            'signals_detected': {
                'upsell': upsell_count,
                'cross_sell': cross_sell_count,
                'loyalty': loyalty_count,
                'brand_advocate': advocate_count,
                'exceptional_satisfaction': exceptional_count
            },
            'is_high_value': opportunity_level == 'alta_oportunidade'
        }

    def _no_opportunity_result(self) -> Dict:
        """Retorna resultado padrão para sem oportunidade."""
        return {
            'opportunity_score': 0.0,
            'opportunity_level': 'sem_oportunidade',
            'opportunity_types': [],
            'customer_profile': 'cliente_comum',
            'signals_detected': {
                'upsell': 0,
                'cross_sell': 0,
                'loyalty': 0,
                'brand_advocate': 0,
                'exceptional_satisfaction': 0
            },
            'is_high_value': False
        }

    def _classify_opportunity(self, score: float, rating: int,
                             sentiment: str) -> str:
        """
        Classifica o nível de oportunidade.

        Args:
            score: Score calculado
            rating: Nota da avaliação
            sentiment: Sentimento

        Returns:
            Nível: alta_oportunidade, media_oportunidade, baixa_oportunidade,
                  sem_oportunidade
        """
        if sentiment == 'negativo' or rating < 4:
            return 'sem_oportunidade'

        if score >= 50 or (rating == 5 and score >= 30):
            return 'alta_oportunidade'
        elif score >= 25 or (rating == 5 and score >= 15):
            return 'media_oportunidade'
        elif score > 0:
            return 'baixa_oportunidade'
        else:
            return 'sem_oportunidade'

    def _identify_opportunity_types(self, upsell: int, cross_sell: int,
                                    loyalty: int, advocate: int,
                                    exceptional: int) -> List[str]:
        """
        Identifica tipos de oportunidade presentes.

        Returns:
            Lista de tipos de oportunidade
        """
        types = []

        if upsell > 0:
            types.append('upsell')
        if cross_sell > 0:
            types.append('cross_sell')
        if loyalty > 0:
            types.append('fidelidade')
        if advocate > 0:
            types.append('advogado_marca')
        if exceptional > 0:
            types.append('satisfacao_excepcional')

        return types

    def _profile_customer(self, loyalty: int, advocate: int,
                         exceptional: int) -> str:
        """
        Cria perfil do cliente baseado nos sinais.

        Returns:
            Perfil do cliente
        """
        total_signals = loyalty + advocate + exceptional

        if advocate >= 2 or (advocate >= 1 and loyalty >= 1):
            return 'advogado_marca'
        elif loyalty >= 2 or (loyalty >= 1 and exceptional >= 1):
            return 'cliente_fiel'
        elif exceptional >= 2:
            return 'altamente_satisfeito'
        elif total_signals > 0:
            return 'cliente_satisfeito'
        else:
            return 'cliente_comum'

    def get_opportunity_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calcula estatísticas de oportunidades para um dataset.

        Args:
            df: DataFrame com colunas 'avaliacao', 'nota', 'sentimento'

        Returns:
            Dicionário com estatísticas agregadas
        """
        # Aplica detecção em todo o dataset
        opportunity_results = df.apply(
            lambda row: self.find_opportunities(
                row['avaliacao'],
                row['nota'],
                row['sentimento']
            ),
            axis=1
        )

        # Extrai níveis de oportunidade
        opportunity_levels = opportunity_results.apply(
            lambda x: x['opportunity_level']
        )

        # Extrai perfis de clientes
        customer_profiles = opportunity_results.apply(
            lambda x: x['customer_profile']
        )

        return {
            'total_avaliacoes': len(df),
            'alta_oportunidade': (opportunity_levels == 'alta_oportunidade').sum(),
            'media_oportunidade': (opportunity_levels == 'media_oportunidade').sum(),
            'baixa_oportunidade': (opportunity_levels == 'baixa_oportunidade').sum(),
            'sem_oportunidade': (opportunity_levels == 'sem_oportunidade').sum(),
            'percentual_alta_oportunidade': (
                opportunity_levels == 'alta_oportunidade'
            ).mean() * 100,
            'advogados_marca': (customer_profiles == 'advogado_marca').sum(),
            'clientes_fieis': (customer_profiles == 'cliente_fiel').sum(),
            'score_medio': opportunity_results.apply(
                lambda x: x['opportunity_score']
            ).mean()
        }

    def get_top_opportunities(self, df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """
        Retorna as top N oportunidades do dataset.

        Args:
            df: DataFrame com avaliações
            n: Número de oportunidades a retornar

        Returns:
            DataFrame com top oportunidades
        """
        # Aplica detecção
        df_copy = df.copy()
        opportunity_results = df_copy.apply(
            lambda row: self.find_opportunities(
                row['avaliacao'],
                row['nota'],
                row['sentimento']
            ),
            axis=1
        )

        df_copy['opportunity_score'] = opportunity_results.apply(
            lambda x: x['opportunity_score']
        )
        df_copy['opportunity_level'] = opportunity_results.apply(
            lambda x: x['opportunity_level']
        )
        df_copy['customer_profile'] = opportunity_results.apply(
            lambda x: x['customer_profile']
        )

        # Filtra e ordena
        top = df_copy[df_copy['opportunity_score'] > 0].nlargest(
            n, 'opportunity_score'
        )

        return top[[
            'avaliacao', 'nota', 'sentimento',
            'opportunity_score', 'opportunity_level', 'customer_profile'
        ]]
