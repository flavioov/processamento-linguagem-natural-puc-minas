# 🌐 Chainlit Frontend - Guia Completo

Este documento descreve como usar e personalizar a interface web Chainlit para o sistema de Document QA.

---

## 📖 O que é Chainlit?

Chainlit é um framework Python open-source para construir interfaces de chat conversacionais para aplicações de IA. Ele oferece:

- 🎨 Interface moderna e responsiva
- 💬 Histórico de conversas
- 🔧 Visualização de ferramentas e processos
- 🌓 Suporte a temas (claro/escuro)
- 📱 Design mobile-friendly
- ⚡ Integração nativa com LangChain e LangGraph

---

## 🚀 Início Rápido

### Instalação

As dependências do Chainlit já estão incluídas no `pyproject.toml`:

```bash
poetry install
```

### Executar a Aplicação

```bash
# Modo desenvolvimento (auto-reload)
chainlit run app.py -w

# Modo produção
chainlit run app.py
```

A aplicação estará disponível em: **http://localhost:8000**

### Opções de Linha de Comando

```bash
# Especificar porta customizada
chainlit run app.py -w --port 8080

# Modo headless (sem abrir navegador)
chainlit run app.py -w --headless

# Habilitar debug
chainlit run app.py -w --debug
```

---

## 🏗️ Arquitetura da Aplicação

### Estrutura de Arquivos

```
processamento-linguagem-natural-puc-minas/
├── app.py                    # Aplicação principal Chainlit
└── .chainlit/
    └── config.toml           # Configurações da interface
```

### Fluxo de Execução

```mermaid
flowchart TD
    A[Usuário acessa http://localhost:8000] --> B[@cl.on_chat_start]
    B --> C[Cria agente LangGraph]
    C --> D[Armazena na sessão]
    D --> E[Exibe mensagem de boas-vindas]

    E --> F[Usuário envia mensagem]
    F --> G[@cl.on_message]
    G --> H[Recupera agente da sessão]
    H --> I[Processa com LangGraph]
    I --> J[Executa tools se necessário]
    J --> K[Retorna resposta]
    K --> L[Atualiza UI]

    L --> F

    M[Usuário fecha chat] --> N[@cl.on_chat_end]
    N --> O[Limpa sessão]

    style B fill:#90CAF9
    style G fill:#90CAF9
    style N fill:#90CAF9
```

---

## 🎨 Personalização da Interface

### Configuração Básica

Edite `.chainlit/config.toml`:

```toml
[UI]
name = "Assistente Médico RAG"
description = "Sistema de Document QA para análise de anamneses"

# Ocultar chain of thought
hide_cot = false

# Permitir upload de arquivos
spontaneous_file_upload = true
```

### Temas e Cores

#### Tema Claro

```toml
[UI.theme.light]
    background = "#FAFAFA"
    paper = "#FFFFFF"

    [UI.theme.light.primary]
        main = "#2196F3"    # Azul principal
        dark = "#1976D2"
        light = "#64B5F6"
```

#### Tema Escuro

```toml
[UI.theme.dark]
    background = "#1a1a1a"
    paper = "#262626"

    [UI.theme.dark.primary]
        main = "#90CAF9"
        dark = "#42A5F5"
        light = "#BBDEFB"
```

### Logo e Branding

Adicione seu logo personalizado:

```bash
mkdir -p public
# Coloque seu logo em public/logo.png
```

Configure no `config.toml`:

```toml
[UI]
custom_logo = "/public/logo.png"
```

---

## 🔧 Funcionalidades Implementadas

### 1. Inicialização do Chat (`@cl.on_chat_start`)

Quando um usuário inicia um novo chat:

1. ✅ Cria uma instância do agente LangGraph
2. ✅ Armazena na sessão do usuário
3. ✅ Inicializa histórico de mensagens vazio
4. ✅ Exibe mensagem de boas-vindas com informações do sistema

```python
@cl.on_chat_start
async def start():
    agent = create_agent()
    cl.user_session.set("agent", agent)
    cl.user_session.set("message_history", [])
    await cl.Message(content=welcome_message).send()
```

### 2. Processamento de Mensagens (`@cl.on_message`)

Quando o usuário envia uma mensagem:

1. ✅ Recupera o agente da sessão
2. ✅ Cria mensagem LangChain (HumanMessage)
3. ✅ Adiciona ao histórico
4. ✅ Processa com o agente LangGraph
5. ✅ Detecta chamadas de ferramentas
6. ✅ Exibe ferramentas utilizadas
7. ✅ Retorna resposta formatada

```python
@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    result = agent.invoke({"messages": message_history})
    # Processa e exibe resposta...
```

### 3. Visualização de Ferramentas

O sistema detecta automaticamente quando ferramentas são utilizadas:

```
🔧 retrieve_context
🔧 add

Resposta do assistente...
```

### 4. Encerramento do Chat (`@cl.on_chat_end`)

Quando o usuário fecha o chat:

1. ✅ Limpa a sessão
2. ✅ Libera recursos
3. ✅ Registra log de encerramento

---

## 📝 Exemplos de Uso

### Exemplo 1: Consulta Médica Simples

**Usuário:** "Qual o diagnóstico do paciente João?"

**Sistema:**
```
🔧 retrieve_context

Com base nos documentos recuperados, o paciente João Gabriel,
72 anos, foi diagnosticado com hematúria (sangue na urina)...
```

### Exemplo 2: Cálculo com Contexto

**Usuário:** "Se o paciente tem 72 anos, em que ano ele nasceu?"

**Sistema:**
```
🔧 retrieve_context
🔧 add

Considerando que estamos em 2024, o paciente nasceu em 1952.
```

---

## ⚙️ Configurações Avançadas

### Ajustar Timeout de Sessão

```toml
[project]
session_timeout = 3600  # 1 hora em segundos
```

### Habilitar Cache

```toml
[project]
cache = true  # Cache de embeddings e LLM
```

### Playground de Prompts

```toml
[features]
prompt_playground = true  # Habilita editor de prompts
```

### Permitir HTML

```toml
[features]
unsafe_allow_html = false  # Segurança: desabilitado por padrão
```

---

## 🐛 Troubleshooting

### Erro: "Port 8000 already in use"

```bash
# Usar outra porta
chainlit run app.py -w --port 8080
```

### Erro: "ModuleNotFoundError: No module named 'chainlit'"

```bash
# Reinstalar dependências
poetry install
```

### Erro: "Agent not initialized"

O agente não foi criado corretamente. Verifique:

1. ✅ Ollama está rodando: `ollama serve`
2. ✅ Modelo está disponível: `ollama list`
3. ✅ Configuração do `.env` está correta

### Interface não carrega

```bash
# Limpar cache do Chainlit
rm -rf .chainlit/cache

# Reiniciar aplicação
chainlit run app.py -w
```

---

## 🔐 Segurança

### Variáveis de Ambiente Protegidas

Configure variáveis sensíveis em `.env`:

```env
OLLAMA_API_KEY=sua_chave_secreta
```

No `config.toml`, especifique quais variáveis cada usuário deve fornecer:

```toml
[project]
user_env = ["OLLAMA_API_KEY"]
```

### Origens Autorizadas

Em produção, restrinja origens:

```toml
[project]
allow_origins = ["https://seu-dominio.com"]
```

---

## 📊 Monitoramento e Logs

### Logs do Sistema

O sistema usa o logger do `simple_rag`:

```python
from simple_rag.utils.logger import setup_logger
logger = setup_logger(__name__)

logger.info("✓ Sessão iniciada")
logger.debug(f"Processando: {user_input}")
logger.error(f"Erro: {e}", exc_info=True)
```

### Estatísticas de Uso

O sistema rastreia:

- Número de chamadas LLM (`llm_calls`)
- Ferramentas utilizadas
- Tempo de resposta (via logs)

---

## 🚀 Deploy em Produção

### Docker

Crie um `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Instalar Poetry
RUN pip install poetry

# Copiar arquivos
COPY pyproject.toml poetry.lock ./
COPY . .

# Instalar dependências
RUN poetry install --no-dev

# Expor porta
EXPOSE 8000

# Executar aplicação
CMD ["poetry", "run", "chainlit", "run", "app.py", "--host", "0.0.0.0"]
```

Build e executar:

```bash
docker build -t simple-rag-chainlit .
docker run -p 8000:8000 simple-rag-chainlit
```

### Variáveis de Ambiente

```bash
docker run -p 8000:8000 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  simple-rag-chainlit
```

---

## 📚 Recursos Adicionais

### Documentação Oficial

- [Chainlit Documentation](https://docs.chainlit.io/)
- [Chainlit GitHub](https://github.com/Chainlit/chainlit)
- [LangChain Integration](https://docs.chainlit.io/integrations/langchain)

### Exemplos da Comunidade

- [Chainlit Cookbook](https://github.com/Chainlit/cookbook)
- [LangGraph Examples](https://langchain-ai.github.io/langgraph/)

---

## 🤝 Contribuindo

Para adicionar novas funcionalidades ao frontend:

1. Edite `app.py` para adicionar novos decoradores
2. Atualize `.chainlit/config.toml` com novas configurações
3. Teste localmente: `chainlit run app.py -w`
4. Documente as mudanças neste arquivo

---

## 📝 Changelog

### v1.0.0 (2024-12-12)

- ✅ Implementação inicial do frontend Chainlit
- ✅ Integração com LangGraph agent
- ✅ Visualização de ferramentas utilizadas
- ✅ Histórico de conversas
- ✅ Mensagem de boas-vindas personalizada
- ✅ Tratamento de erros
- ✅ Configuração de tema e UI

---

**Última atualização:** 2024-12-12
**Versão:** 1.0.0
