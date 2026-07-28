import os
import json
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Campanha de Oração Devocional", layout="centered")

GROQ_KEY = os.getenv("GROQ_API_KEY")

st.title("📖 Nosso Momento Devocional")
st.write("Estudo simples versículo por versículo para acompanhar a leitura em família.")
st.divider()

col1, col2 = st.columns([2, 1])
with col1:
    livro = st.text_input("Livro Bíblico", value="Salmos")
with col2:
    capitulo = st.number_input("Capítulo", min_value=1, value=23)

if st.button("🔍 Carregar Estudo Devocional", type="primary", use_container_width=True):
    if not GROQ_KEY:
        st.error("Chave GROQ_API_KEY não configurada nos Secrets do App!")
    else:
        with st.spinner("Buscando o capítulo e preparando o estudo com carinho..."):
            try:
                client = Groq(api_key=GROQ_KEY)
                
                prompt = f"""
                Você é um pastor muito acolhedor, amoroso e atencioso.
                Sua missão é gerar o estudo devocional completo do capítulo {livro} {capitulo}.
                O público-alvo é uma senhora idosa (uma avó querida) lendo junto com seu neto.

                Instruções Obrigatórias:
                1. Traga TODOS os versículos do capítulo {livro} {capitulo} na íntegra (em português).
                2. NÃO use termos teológicos difíceis (sem grego, hebraico, exegese, jargões acadêmicos, etc.).
                3. Explique versículo por versículo em 2 ou 3 frases simples, doces e carinhosas.
                4. Responda ESTRITAMENTE em formato JSON com a seguinte estrutura exata:
                {{
                    "versiculos": [
                        {{
                            "numero": 1,
                            "texto": "Texto bíblico exato do versículo 1",
                            "explicacao": "Explicação simples e afetuosa"
                        }}
                    ]
                }}
                """

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Você é um assistente pastoral especializado em devocionais simples e estruturação de respostas estritamente em JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                
                dados = json.loads(completion.choices[0].message.content)

                st.subheader(f"📖 {livro.capitalize()} {capitulo}")
                st.divider()

                for item in dados.get("versiculos", []):
                    st.markdown(f"#### Versículo {item['numero']}")
                    st.info(f"👉 **\"{item['texto']}\"**")
                    st.markdown(f"💡 **O que este versículo ensina:**\n{item['explicacao']}")
                    st.write("")

            except Exception as e:
                st.error(f"Erro ao gerar o estudo: {str(e)}")