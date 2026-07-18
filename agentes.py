#encoding: utf-8
import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

import urllib.parse
import http.client
import json

load_dotenv()



@tool
def buscar_dados_online(termo_busca: str) -> str:
    """Pesquisa informações atualizadas na internet, para validar o texto gerado pela LLM. 
    Use esta ferramenta sempre que precisar de fatos recentes, notícias ou dados que não sabe.
    """
    try:
        termo_enc = urllib.parse.quote(termo_busca)
        conn = http.client.HTTPSConnection("api.duckduckgo.com")
        conn.request("GET", f"/?q={termo_enc}&format=json&no_html=1")
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        
        abstract = data.get("AbstractText", "")
        if abstract:
            return abstract
            
        related = data.get("RelatedTopics", [])
        if related and "Text" in related[0]:
            return related[0]["Text"]
            
        return "Nenhum resultado direto encontrado para essa busca online."
    except Exception as e:
        return f"Erro ao acessar a internet: {str(e)}"
    
@tool
def aplicar_formatacao_texto(texto: str, estilo: str) -> str:
    """Aplica estilos de formatação a um texto.
    Estilos aceitos: 'uppercase' (tudo maiúsculo), 'lowercase' (tudo minúsculo) ou 'titulo'.
    """
    estilo_limpo = estilo.lower().strip()
    if "maiusculo" in estilo_limpo or "uppercase" in estilo_limpo:
        return texto.upper()
    elif "minusculo" in estilo_limpo or "lowercase" in estilo_limpo:
        return texto.lower()
    elif "titulo" in estilo_limpo or "title" in estilo_limpo:
        return texto.title()
    return texto

def Agent_formatter():

    llm_format = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.4, verbose=True)

    agent =  create_agent(tools=[aplicar_formatacao_texto], model=llm_format, system_prompt="Você é um agente que formata textos para estrutura de artigo científico")
    return agent


def Agent_online_search():
    llm_format = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.85, verbose=True)

    agent =  create_agent(tools=[buscar_dados_online], model=llm_format, system_prompt="Você é um agente que pesquisa informações online para validar o texto recebido e retorna resultados em forma de artigo científico para que outro agente formate.")
    return agent
