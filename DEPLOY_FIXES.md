# Correções para Deploy no Streamlit Community Cloud

## Problemas Identificados e Corrigidos

### 1. **PROBLEMA CRÍTICO: Múltiplas chamadas a `st.set_page_config()`**

**Causa do erro DOM:**
- Todas as páginas estavam chamando `st.set_page_config()`
- No Streamlit, apenas o arquivo principal (`app.py`) pode chamar esta função
- Páginas secundárias não devem redefinir configurações

**Correção aplicada:**
- ✅ Removido `st.set_page_config()` de `pages/2_Analise_Sentimentos.py`
- ✅ Removido `st.set_page_config()` de `pages/3_Categorias.py`
- ✅ Removido `st.set_page_config()` de `pages/4_Churn_Oportunidades.py`
- ✅ Mantido apenas em `app.py`

### 2. **Vazamento de Memória com Matplotlib**

**Problema:**
- Figuras matplotlib não estavam sendo fechadas após `st.pyplot()`
- Isso causa acúmulo de memória e problemas de renderização

**Correção aplicada:**
- ✅ Adicionado `plt.close(fig)` após cada `st.pyplot()` em `pages/2_Analise_Sentimentos.py`

### 3. **Conflito de Keys em Widgets**

**Problema:**
- Múltiplos sliders e selectboxes sem keys únicas
- Pode causar conflitos de estado entre páginas

**Correção aplicada:**
- ✅ Adicionado `key="sentiment_display_slider"` ao slider da página de Sentimentos
- ✅ Adicionado `key="churn_display_slider"` ao slider da página de Churn
- ✅ Adicionado `key="churn_min_score_slider"` ao slider de score mínimo
- ✅ Adicionado `key="opp_display_slider"` ao slider de oportunidades

### 4. **Otimização de Configuração**

**Melhorias aplicadas:**
- ✅ Atualizado `.streamlit/config.toml` com configurações otimizadas:
  - `enableCORS = false`
  - `enableXsrfProtection = true`
  - `fastReruns = true`

## Como Fazer o Deploy no Streamlit Community Cloud

### Passo 1: Preparar o Repositório Git

```bash
# Adicionar as mudanças
git add .

# Fazer commit
git commit -m "Fix: Corrigido erro DOM no deploy - removido st.set_page_config duplicado"

# Push para o GitHub
git push origin main
```

### Passo 2: Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Selecione:
   - **Repository:** seu repositório
   - **Branch:** main
   - **Main file path:** app.py
5. Clique em "Deploy!"

### Passo 3: Verificar Logs

Se houver erros:
1. Clique em "Manage app" → "Logs"
2. Verifique se há erros de importação ou dependências
3. Se necessário, atualize `requirements.txt`

## Estrutura de Arquivos Correta

```
Python_Dashbord/
├── app.py                          # ✅ Único arquivo com st.set_page_config()
├── requirements.txt                # ✅ Dependências
├── .streamlit/
│   └── config.toml                 # ✅ Configurações otimizadas
├── data/
│   └── dataset_avaliacoes.csv      # ✅ Dataset
├── pages/
│   ├── 2_Analise_Sentimentos.py   # ✅ SEM st.set_page_config()
│   ├── 3_Categorias.py             # ✅ SEM st.set_page_config()
│   └── 4_Churn_Oportunidades.py   # ✅ SEM st.set_page_config()
└── src/
    ├── preprocessing/
    ├── analysis/
    └── visualization/
```

## Checklist de Deploy

- [x] Removido `st.set_page_config()` de todas as páginas
- [x] Adicionado `plt.close()` após `st.pyplot()`
- [x] Adicionado keys únicas em widgets
- [x] Atualizado `.streamlit/config.toml`
- [ ] Fazer commit e push das alterações
- [ ] Fazer deploy no Streamlit Cloud
- [ ] Verificar logs e funcionamento

## Solução de Problemas

### Se o erro persistir:

1. **Limpar cache do Streamlit:**
   - No Streamlit Cloud: Menu → "Clear cache" → "Clear app cache"

2. **Reiniciar a aplicação:**
   - No Streamlit Cloud: Menu → "Reboot app"

3. **Verificar versão do Streamlit:**
   - Garantir que `requirements.txt` tem `streamlit==1.29.0` ou superior

4. **Verificar logs de erro:**
   - Procurar por erros relacionados a importações, arquivos não encontrados, etc.

## Teste Local Antes do Deploy

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar localmente
streamlit run app.py
```

Se funcionar localmente sem erros, deve funcionar no Streamlit Cloud também!

## Suporte

Se ainda houver problemas após essas correções:
1. Verifique os logs do Streamlit Cloud
2. Procure por erros específicos na console do navegador (F12)
3. Certifique-se de que todos os arquivos foram commitados e pushed corretamente
