# 📊 DeepSearch-to-Article: Multi-Agent Researcher

Um orquestrador de agentes autônomos baseado em **LangChain/LangGraph** e **Streamlit** que realiza buscas online profundas, consolida informações estruturadas e renderiza artigos científicos ou relatórios técnicos formatados sob demanda, utilizando os modelos da família **Gemini (Google AI Studio)**.

## 🚀 Funcionalidades

- **Orquestração Multi-Agente**: Divisão clara de tarefas entre um agente especialista em busca online profunda e um agente especialista em formatação técnico-científica.
- **Arquitetura de Cota Otimizada**: Configuração inteligente de modelos para evitar o esgotamento de limites de requisições diárias (RPD):
  - **`gemini-2.0-flash-lite`** nos agentes para lidar com múltiplos loops de raciocínio econômicos e de baixíssima latência.
  - **`gemini-2.0-flash`** no módulo principal para consolidação e escrita estilística de alta qualidade com suporte a *streaming* nativo.
- **Interface Fluida com Streamlit**: Renderização e exibição das respostas em tempo real conforme o artigo é construído passo a passo.
- **Suporte Avançado a LaTeX**: Tratamento de caracteres e quebras de linha literal para perfeita renderização de fórmulas matemáticas complexas diretamente na interface.

## 📁 Estrutura do Projeto

```text
├── .env                  # Chaves de API e variáveis de ambiente (Não enviado ao Git)
├── .gitignore            # Filtro de arquivos protegidos
├── agentes.py            # Definição e lógica de pensamento dos agentes e ferramentas
├── app.py                # Interface gráfica do usuário e orquestração final (Streamlit)
└── requirements.txt      # Dependências do ecossistema Python
```

## 🛠️ Pré-requisitos & Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie e ative o seu ambiente virtual (`.venv`):**
   ```bash
   python -m venv .venv
   # No Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # No Linux/macOS:
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as Variáveis de Ambiente:**
   Crie um arquivo chamado `.env` na raiz do projeto e insira sua chave do Google AI Studio:
   ```text
   GOOGLE_API_KEY=seu_api_key_aqui
   ```

## 💻 Como Executar

Com o ambiente virtual ativado e as chaves configuradas, inicialize o servidor do Streamlit:
```bash
streamlit run app.py
```

## 📄 Licença

Este projeto está licenciado sob a licença **MIT** — consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.
