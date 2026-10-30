import streamlit as st

# ============================================================
# CONFIGURAÇÕES INICIAIS
# ============================================================

st.set_page_config(
    page_title="Study Cards",
    page_icon="🧠",
    layout="wide"
    
)


# ========================= SIDEBAR

st.sidebar.title('Study Cards')


# ========================= BODY
st.title('Study Cards', text_alignment="center")
st.subheader('🧠Estude qualquer assunto com cards de perguntas e respostas.', text_alignment="center")
st.markdown('---')
st.write('Crie cards com inteligência artificial a partir de um tema ou de um texto seu, ou carregue cards que você já tem. Depois é só virar, responder e revisar no seu ritmo.')

st.markdown("""

## Por onde começar

Escolha uma opção no menu à esquerda:

### 📚 Cards
Abra um arquivo de cards que você já tem e comece a estudar.

### ✨ Gerar Cards com IA
Digite um tema, como "Revolução Francesa" ou "Fundamentos de Python", e a IA cria os cards para você.

---

## Como funciona

1. **Escolha a origem:** um tema, um texto ou cards que você já tem.
2. **Gere ou carregue:** a IA cria os cards em poucos instantes.
3. **Estude:** vire os cards, teste sua memória e repita quantas vezes quiser.

---

## Por que estudar com cards?

Reler o conteúdo dá a sensação de que você sabe, mas responder perguntas mostra o que você realmente sabe. Os cards ajudam a lembrar melhor, encontrar lacunas e revisar em sessões curtas.

---

> ℹ️ Os cards são gerados por IA. Vale conferir as respostas, principalmente em assuntos importantes.

**Pronto para começar? Escolha uma opção no menu ao lado.** 👈
""")
