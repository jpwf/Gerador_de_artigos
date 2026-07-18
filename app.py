#encoding: utf-8
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from agentes import Agent_formatter, Agent_online_search
import json

load_dotenv()

token = os.getenv("GOOGLE_API_KEY")
agente_formata = Agent_formatter()
agente_busca = Agent_online_search()

if not token:
    print("Nenhuma chave de API encontrada no sistema.")
    token = input("Por favor, insira a sua Google API Key (Gemini): ").strip()
    with open(".env", "a", encoding="utf-8") as f:
        f.write(f"GOOGLE_API_KEY={token}\n")
    os.environ['GOOGLE_API_KEY'] = token
    print("Chave salva com sucesso no arquivo .env para os próximos acessos!\n")
else:
    os.environ['GOOGLE_API_KEY'] = token

st.title("Gerador de textos para artigo")

if "processando" not in st.session_state:
    st.session_state.processando = False

def enviar_prompt():
    if st.session_state.campo_prompt:
        st.session_state.processando = True

with st.form(key="meu_formulario", clear_on_submit=False):
    prompt = st.text_input(
        'Diga seu tópico', 
        key="campo_prompt", 
        disabled=st.session_state.processando
    )
    botao_enviar = st.form_submit_button("Enviar", on_click=enviar_prompt)

template_titulo = PromptTemplate(
    input_variables=['topic'], 
    template="Me de um título para parágrafo sobre {topic} em português."
)

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.85, verbose=True)

template_prompt = PromptTemplate(
    input_variables=['titulo_gerado'],
    template="Me de um artigo formatado e numerado com o título: {titulo_gerado}; em português."
)

title_chain = template_titulo | llm
body_chain = template_prompt | llm
sequential_chain = title_chain | body_chain

if st.session_state.processando and prompt:
    with st.spinner("Os agentes estão trabalhando nisso... Por favor, aguarde."):
        llm_response = sequential_chain.invoke(prompt)
        texto_inicial = llm_response.content if hasattr(llm_response, 'content') else llm_response

        Agent_online_search_response = agente_busca.invoke({"messages": [("user", texto_inicial)]})
        texto_da_busca = Agent_online_search_response["messages"][-1].content

        input_formatador = f"Formate o seguinte texto no estilo de artigo científico: {texto_da_busca}"
        Agent_formatter_response = agente_formata.invoke({"messages": [("user", input_formatador)]})
        conteudo = Agent_formatter_response["messages"][-1].content
        resultado_final = conteudo[0].get("text", str(conteudo)) if isinstance(conteudo, list) else (conteudo.get("text", str(conteudo)) if isinstance(conteudo, dict) else conteudo)

    st.write(resultado_final)
    
    st.session_state.processando = False
    