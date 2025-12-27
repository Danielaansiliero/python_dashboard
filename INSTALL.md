# 🚀 Guia de Instalação e Execução

## ✅ Status do Projeto

Todos os arquivos foram validados e testados:

- ✓ **app.py** - Sintaxe OK
- ✓ **text_cleaner.py** - Sintaxe OK
- ✓ **churn_detector.py** - Sintaxe OK
- ✓ **opportunity_finder.py** - Sintaxe OK
- ✓ **charts.py** - Sintaxe OK
- ✓ **4_Churn_Oportunidades.py** - Sintaxe OK
- ✓ **2_Analise_Sentimentos.py** - Sintaxe OK
- ✓ **3_Categorias.py** - Sintaxe OK

## 📋 Pré-requisitos

- **Python 3.8+** (Testado com Python 3.12.3)
- **pip** (gerenciador de pacotes Python)

## 🔧 Instalação

### Opção 1: Instalação Básica

```bash
# 1. Entre no diretório do projeto
cd /home/daniela/Documentos/Projetos_Pessoais/Python_Dashbord

# 2. (Opcional) Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o dashboard
streamlit run app.py
```

### Opção 2: Instalação com pip3

```bash
pip3 install -r requirements.txt
streamlit run app.py
```

### Opção 3: Instalação Manual das Bibliotecas Principais

Se houver problemas com o requirements.txt, instale manualmente:

```bash
pip install streamlit==1.29.0
pip install pandas==2.1.4
pip install plotly==5.18.0
pip install matplotlib==3.8.2
pip install wordcloud==1.9.3
pip install nltk==3.8.1
pip install scikit-learn==1.3.2
pip install unidecode==1.3.7
```

## 🌐 Acessando o Dashboard

Após executar `streamlit run app.py`, o dashboard estará disponível em:

- **Local**: http://localhost:8501
- **Network**: http://192.168.x.x:8501 (será exibido no terminal)

O Streamlit abrirá automaticamente o navegador padrão.

## 🧪 Testando Sem Streamlit

Se você não conseguir instalar o Streamlit, pode testar a lógica do código:

```bash
python3 test_dashboard.py
```

Este script testa todos os módulos principais sem interface gráfica.

## 📂 Estrutura dos Arquivos

```
Python_Dashboard/
├── app.py                    # ⭐ Página principal - COMECE AQUI
├── requirements.txt          # Dependências
├── test_dashboard.py         # Teste sem Streamlit
│
├── data/
│   └── dataset_avaliacoes.csv  # Dataset (15.500 avaliações)
│
├── src/                      # Módulos do backend
│   ├── preprocessing/
│   │   ├── text_cleaner.py      # Limpeza de texto
│   │   └── category_extractor.py # Extração de categorias
│   ├── analysis/
│   │   ├── churn_detector.py     # 🔥 Detecção de churn
│   │   └── opportunity_finder.py # 💡 Oportunidades
│   └── visualization/
│       ├── charts.py             # Gráficos Plotly
│       └── wordcloud_gen.py      # Nuvens de palavras
│
└── pages/                    # Páginas do dashboard
    ├── 2_Analise_Sentimentos.py
    ├── 3_Categorias.py
    └── 4_Churn_Oportunidades.py  # 🎯 Página destaque
```

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'X'"

```bash
# Reinstale a dependência específica
pip install <nome_do_modulo>
```

### Erro: "pip: command not found"

```bash
# Use pip3 no lugar de pip
pip3 install -r requirements.txt
```

### Erro: "Permission denied"

```bash
# Instale com --user
pip install -r requirements.txt --user
```

### Dashboard não abre no navegador

```bash
# Execute com porta específica
streamlit run app.py --server.port 8502

# Ou desabilite abertura automática
streamlit run app.py --server.headless true
```

## 📊 Recursos do Dashboard

### Página 1: Home
- KPIs principais
- Visão geral dos dados
- Navegação rápida

### Página 2: Análise de Sentimentos
- Word clouds positivo/negativo
- Distribuição de sentimentos
- Explorador com busca

### Página 3: Categorias
- Comparação entre categorias
- Estatísticas detalhadas
- Drill-down por categoria

### Página 4: Churn & Oportunidades ⭐
- **Detecção de risco de churn**
- **Identificação de oportunidades**
- **Recomendações estratégicas**

## 🎯 Funcionalidades Especiais

### Filtros Interativos
- Por sentimento (positivo/negativo)
- Por nota (1-5 estrelas)
- Por categoria de produto

### Análises Avançadas
- Score de churn (0-100)
- Score de oportunidade (0-100)
- Perfil de cliente (fiel, advogado, satisfeito)
- Aspectos problemáticos (entrega, qualidade, preço)

## 📚 Recursos Adicionais

- **README.md**: Documentação completa do projeto
- **test_dashboard.py**: Script de teste dos módulos
- **.gitignore**: Arquivos a ignorar no Git

## 💬 Suporte

Se encontrar problemas:

1. Verifique a versão do Python: `python3 --version`
2. Verifique se pip está instalado: `pip --version`
3. Teste a sintaxe: `python3 -m py_compile app.py`
4. Execute o teste: `python3 test_dashboard.py`

## 🎉 Pronto!

Após a instalação bem-sucedida, você terá um dashboard completo de análise de sentimentos com detecção de churn e oportunidades!

---

**Desenvolvido com ❤️ usando Python, Streamlit e NLP**
