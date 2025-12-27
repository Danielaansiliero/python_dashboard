# 📊 Dashboard de Análise de Sentimentos - E-commerce

Dashboard interativo desenvolvido em Python para análise de sentimentos de avaliações de e-commerce brasileiro, com detecção de risco de churn e identificação de oportunidades de crescimento.

## 🎯 Objetivo

Extrair insights valiosos de 15.500+ avaliações de clientes através de análise de sentimentos, NLP e visualizações interativas, auxiliando na tomada de decisões estratégicas.

## ✨ Funcionalidades Principais

### 📈 Análise de Sentimentos
- Classificação automática de sentimentos (positivo/negativo)
- Análise de intensidade emocional
- Distribuição de sentimentos por categoria
- Nuvens de palavras por sentimento

### 🏷️ Categorização Automática
- Extração de categorias de produtos via NLP
- Análise comparativa entre categorias
- Métricas de desempenho por categoria

### ⚠️ Detecção de Risco de Churn
- **Diferencial do projeto!**
- Identificação de clientes em risco de abandono
- Score de churn baseado em análise textual
- Classificação de risco (alto, médio, baixo)
- Identificação de aspectos problemáticos (entrega, qualidade, preço, atendimento)

### 💡 Identificação de Oportunidades
- Detecção de oportunidades de upsell e cross-sell
- Identificação de advogados da marca
- Perfil de clientes (fiel, satisfeito, advogado)
- Score de oportunidade

### 📊 Visualizações Interativas
- Gráficos Plotly responsivos
- KPIs dinâmicos
- Filtros interativos
- Tabelas detalhadas

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit** - Framework de dashboard
- **Pandas** - Manipulação de dados
- **Plotly** - Visualizações interativas
- **scikit-learn** - Machine Learning (TF-IDF, análise)
- **NLTK** - Processamento de linguagem natural
- **WordCloud** - Nuvens de palavras
- **Matplotlib** - Visualizações complementares

## 📂 Estrutura do Projeto

```
Python_Dashboard/
├── .streamlit/
│   └── config.toml              # Configuração de tema
├── data/
│   └── dataset_avaliacoes.csv   # Dataset de avaliações
├── src/
│   ├── preprocessing/
│   │   ├── text_cleaner.py      # Limpeza de texto PT-BR
│   │   └── category_extractor.py # Extração de categorias
│   ├── analysis/
│   │   ├── churn_detector.py     # Detecção de churn
│   │   └── opportunity_finder.py # Oportunidades
│   └── visualization/
│       ├── charts.py             # Gráficos Plotly
│       └── wordcloud_gen.py      # Nuvens de palavras
├── pages/
│   ├── 2_Analise_Sentimentos.py
│   ├── 3_Categorias.py
│   └── 4_Churn_Oportunidades.py  # Página destaque!
├── app.py                        # Página principal
├── requirements.txt
└── README.md
```

## 🚀 Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/Python_Dashboard.git
cd Python_Dashboard
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute o dashboard
```bash
streamlit run app.py
```

O dashboard estará disponível em `http://localhost:8501`

## 📊 Dataset

- **Fonte**: Avaliações de e-commerce brasileiro
- **Volume**: 15.500 avaliações
- **Colunas**:
  - `ID_avaliacao`: Identificador único
  - `avaliacao`: Texto da avaliação
  - `nota`: Classificação de 1 a 5
  - `sentimento`: positivo/negativo

### 🔒 Privacidade e Conformidade

**Este projeto utiliza dados educacionais anônimos:**

- ✅ **Sem informações pessoais identificáveis** (PII)
- ✅ **Conformidade com LGPD/GDPR**
- ✅ **Dados 100% anônimos**: Não contêm CPF, e-mail, telefone ou qualquer dado sensível
- ✅ **Finalidade educacional**: Projeto acadêmico e de portfólio
- ✅ **Avaliações públicas**: Textos genéricos de produtos de e-commerce

**Importante:** Este é um projeto demonstrativo. Os insights gerados são para fins educacionais e não devem ser utilizados para tomada de decisões comerciais reais.

## 🎨 Páginas do Dashboard

### 1️⃣ Home
- KPIs principais (total, nota média, % positivo)
- Distribuição de notas e sentimentos
- Preview de análise por categoria

### 2️⃣ Análise de Sentimentos
- Distribuição detalhada de sentimentos
- Heatmap sentimento vs nota
- Nuvens de palavras (positivo/negativo)
- Top palavras mais frequentes
- Explorador de avaliações com busca

### 3️⃣ Categorias
- Estatísticas por categoria de produto
- Comparação entre categorias
- Análise detalhada por categoria selecionada
- Drill-down em avaliações

### 4️⃣ Churn & Oportunidades ⭐
- **Análise de Risco de Churn**:
  - Gauge de risco
  - Lista de clientes críticos
  - Aspectos problemáticos identificados
- **Oportunidades de Crescimento**:
  - Identificação de leads para upsell
  - Advogados da marca
  - Clientes fiéis
- Visão combinada e recomendações estratégicas

## 🔍 Diferenciais do Projeto

1. **Análise de Churn Baseada em NLP**: Sistema único de detecção de risco usando análise de texto
2. **Identificação de Oportunidades**: Detecta automaticamente chances de upsell/cross-sell
3. **NLP em Português**: Léxico customizado para e-commerce brasileiro
4. **Categorização Automática**: Extrai categorias de produtos do texto
5. **Dashboard Profissional**: Interface moderna e responsiva
6. **Código Modular**: Arquitetura limpa e escalável

## 📈 Insights Gerados

O dashboard é capaz de responder questões como:

- Qual o percentual de clientes em risco de churn?
- Quais categorias têm maior satisfação?
- Quais aspectos geram mais reclamações?
- Quantos clientes são advogados da marca?
- Quais palavras-chave aparecem em avaliações negativas?
- Onde estão as oportunidades de cross-sell?

## 🎓 Aprendizados e Conceitos Aplicados

- Processamento de Linguagem Natural (NLP)
- Análise de Sentimentos
- Extração de Features Textuais
- Visualização de Dados
- Web Apps com Streamlit
- Arquitetura de Código Limpo
- Análise de Negócios

## 📝 Próximas Melhorias

- [ ] Integração com modelos de ML (BERT, transformers)
- [ ] Sistema de alertas automáticos
- [ ] Análise temporal de tendências
- [ ] Export de relatórios em PDF
- [ ] API REST para integração

## 👤 Autor

**Daniela**

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Nome](https://linkedin.com/in/seu-perfil)
- Email: seu.email@exemplo.com

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!
