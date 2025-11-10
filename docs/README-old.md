# Simple RAG - Sistema de Recuperação e Geração Aumentada

Sistema de RAG (Retrieval-Augmented Generation) que utiliza LangChain, Ollama e LangGraph para criar um agente
conversacional com acesso a documentos médicos.

## Documentação Completa

- **[DOCUMENTATION.md](./DOCUMENTATION.md)** - Documentação completa com arquitetura, diagramas e explicações técnicas
- **[NOTEBOOK_EXPLANATION.md](./NOTEBOOK_EXPLANATION.md)** - Explicação detalhada do notebook `rag.ipynb` com exemplos práticos
- **[README.md](./README.md)** (este arquivo) - Guia rápido de instalação e uso

## TL;DR

```shell
# python 3.13
poetry install

# Iniciar aplicação CLI
poetry run python -m simple_rag.main

# Ou testar o vectorstore
poetry run python -m simple_rag.utils.vectorstore
```

## Descrição

Este projeto implementa um agente de IA que combina:

- **Retrieval**: Busca semântica em documentos usando embeddings
- **Generation**: Geração de respostas usando LLM (Llama 3.1)
- **Tools**: Ferramentas customizadas (calculadora e recuperação de documentos)

O agente atua como um assistente médico, respondendo perguntas com base em documentos de anamnese armazenados
localmente.

## Pré-requisitos

- **Python 3.13+** (requerido)
- Ollama instalado e rodando (com modelo `llama3.1:8b`)
- Servidor Ollama acessível (padrão: `http://localhost:11434`)

### Instalando Python 3.13

#### Linux (Ubuntu/Debian)

```bash
# Via deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

#### macOS

```bash
# Via Homebrew
brew install python@3.13
```

#### Windows

1. Baixe o instalador em: https://www.python.org/downloads/
2. Execute o instalador e marque "Add Python to PATH"
3. Verifique a instalação: `python --version`

### Instalar Ollama

#### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Ou manualmente:

```bash
# Download do binário
curl -L https://ollama.com/download/ollama-linux-amd64 -o ollama
chmod +x ollama
sudo mv ollama /usr/local/bin/
```

#### Windows

1. Baixe o instalador do Ollama em: https://ollama.com/download/windows
2. Execute o arquivo `.exe` e siga o assistente de instalação
3. O Ollama será instalado e iniciado automaticamente como serviço

#### macOS

```bash
# Via Homebrew
brew install ollama

# Ou baixe o .dmg em: https://ollama.com/download/mac
```

### Configurar e Iniciar Ollama

Após a instalação, inicie o serviço Ollama:

```bash
# Linux/macOS
ollama serve

# Windows: O serviço inicia automaticamente. Para iniciar manualmente:
# Procure por "Ollama" no menu iniciar e execute
```

O Ollama por padrão roda em `http://localhost:11434`

### Baixar o Modelo

Após instalar, baixe o modelo necessário:

```bash
ollama pull llama3.1:8b ou llama3.2:3b
```

Verifique se o modelo foi baixado:

```bash
ollama list
```

## Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd processamento-linguagem-natural-puc-minas
```

### 2. Instale o Poetry

O Poetry é o gerenciador de dependências usado neste projeto.

#### Linux/macOS/Windows (WSL)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### Windows (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Adicione o Poetry ao PATH conforme instruções exibidas após a instalação.

Verifique a instalação:

```bash
poetry --version
```

### 3. Configure o Poetry para usar Python 3.13

```bash
# Configure o Poetry para criar o ambiente virtual no diretório do projeto (opcional)
poetry config virtualenvs.in-project true

# Especifique o Python 3.13
poetry env use python3.13
```

### 4. Instale as dependências

```bash
# Instalar apenas dependências de produção
poetry install --without dev

# Ou instalar todas as dependências (incluindo desenvolvimento)
poetry install --with dev

# Nota: Com o formato PEP 621 atual, as dependências de desenvolvimento
# estão em [project.optional-dependencies] e podem ser instaladas com:
pip install -e ".[dev]"
```

### 5. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env com suas configurações
# Especialmente OLLAMA_BASE_URL se não estiver usando localhost
```

Principais variáveis no `.env`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
DATA_DIR=./data/anamnese
CHUNK_SIZE=1000
RETRIEVAL_K=4
LOG_LEVEL=INFO
```

## Estrutura do Projeto

```
processamento-linguagem-natural-puc-minas/
├── README.md                         # Este arquivo - guia rápido
├── DOCUMENTATION.md                  # Documentação completa
├── NOTEBOOK_EXPLANATION.md           # Explicação do notebook
├── pyproject.toml                    # Configuração Poetry e ferramentas
├── poetry.lock                       # Lock file das dependências
├── requirements.txt                  # Dependências pip
├── .env                             # Variáveis de ambiente
├── .gitignore
├── docker-compose.yml               # Configuração Docker
├── Dockerfile                       # Build da aplicação
│
├── rag.ipynb                        # Notebook de demonstração
│
├── data/
│   └── anamnese/                    # Documentos de entrada
│       └── anamnese1.txt           # Caso clínico J.G.
│
├── chromadb/                        # Dados persistentes ChromaDB
│
└── simple_rag/                      # Pacote principal
    ├── __init__.py
    ├── main.py                     # CLI e ponto de entrada principal
    │
    ├── config/                     # Configurações
    │   ├── __init__.py
    │   └── config.py              # Settings com Pydantic
    │
    ├── agent/                      # Agente LangGraph
    │   ├── __init__.py
    │   └── agent.py               # StateGraph + Nós (ollama_call, tool_node)
    │
    ├── tools/                      # Ferramentas LangChain
    │   ├── __init__.py
    │   ├── retriever.py           # retrieve_context tool
    │   └── calculator.py          # add, multiply tools
    │
    └── utils/                      # Utilitários
        ├── __init__.py
        ├── logger.py              # Setup de logging
        └── vectorstore.py         # Gerenciamento ChromaDB
```

Para mais detalhes sobre a arquitetura, consulte [DOCUMENTATION.md](./DOCUMENTATION.md).

## Como Usar

### Executar a Aplicação (Modo Principal)

```bash
# Usando Poetry (recomendado)
poetry run python -m simple_rag.main

# Ou ative o ambiente virtual do Poetry primeiro
poetry shell
python -m simple_rag.main

# Ou use o comando direto (se configurado no pyproject.toml)
poetry run simple-rag
```

**Exemplo de interação:**

```
============================================================
Simple RAG - Assistente Médico
============================================================
Digite suas perguntas. Para sair, digite 'exit'

Você: Qual é o diagnóstico da paciente Camila?

Assistente: Com base nos documentos, a paciente Camila Rodrigues
de Almeida foi diagnosticada com lúpus eritematoso sistêmico...

Você: exit

Até logo!
```

### Testar Módulos Individuais

**Importante:** Use `poetry run` ou ative o ambiente virtual primeiro para garantir que as dependências corretas sejam
carregadas.

**Testar vector store:**

```bash
poetry run python -m simple_rag.utils.vectorstore
```

**Testar agente:**

```bash
poetry run python -m simple_rag.agent.agent
```

**Alternativa (ativando o shell primeiro):**

```bash
poetry shell
python -m simple_rag.utils.vectorstore
python -m simple_rag.agent.agent
```

**Experimentar com Jupyter Notebook:**

```bash
jupyter notebook rag.ipynb
```

Consulte [NOTEBOOK_EXPLANATION.md](./NOTEBOOK_EXPLANATION.md) para entender cada célula do notebook.

## Funcionalidades

### Ferramentas Disponíveis

O agente possui três ferramentas:

1. **add(a, b)**: Soma dois números inteiros
2. **multiply(a, b)**: Multiplica dois números inteiros
3. **retriever(query)**: Busca documentos relevantes no vector store usando similaridade semântica

### Mascaramento de Dados Pessoais

O projeto inclui um módulo completo para mascaramento de dados pessoais sensíveis (PII), essencial para proteger informações de pacientes em documentos médicos.

#### Tipos de Dados Suportados

| Tipo | Exemplo Original | Exemplo Mascarado | O que Preserva |
|------|------------------|-------------------|----------------|
| **Nome** | `Nome: João da Silva` | `Nome: J*** da S****` | 1ª letra + preposições |
| **Data Nasc.** | `15/03/1953` | `**/**/****` | Nada (completo) |
| **Prontuário** | `0876532` | `****532` | Últimos 3 dígitos |
| **CPF** | `123.456.789-00` | `123.***.***-00` | 3 primeiros + 2 últimos |
| **RG** | `12.345.678-9` | `12.***.***-9` | 2 primeiros + 1 último |
| **Email** | `user@example.com` | `user@example.com` | 4 primeiros + domínio |
| **Telefone** | `(11) 98765-4321` | `(**) *****-4321` | 4 últimos |
| **CEP** | `12345-678` | `12345-***` | 5 primeiros |

#### Uso Rápido

```python
from simple_rag.utils import mask_all_pii

# Mascarar todos os dados pessoais
patient_data = """
Nome: João Gabriel da Silva
Data de Nascimento: 15/03/1953
CPF: 123.456.789-00
Prontuário: 0876532
Email: joao@hospital.com
Telefone: (11) 98765-4321
"""

masked = mask_all_pii(patient_data)
print(masked)
```

**Resultado:**
```
Nome: J*** G****** da S****
Data de Nascimento: **/**/****
CPF: 123.***.***-00
Prontuário: ****532
Email: joao@hospital.com
Telefone: (**) *****-4321
```

#### Mascaramento Seletivo

```python
from simple_rag.utils import mask_pii

# Mascarar apenas nome e CPF
text = "Nome: Maria Silva, CPF: 987.654.321-00"
masked = mask_pii(text, pii_types=['nome', 'cpf'])
# Resultado: Nome: M**** S****, CPF: 987.***.***-00
```

#### Funções Disponíveis

- `mask_name()` - Mascara nomes (mantém 1ª letra + preposições)
- `mask_birth_date()` - Mascara datas de nascimento (completo)
- `mask_prontuario()` - Mascara prontuários (mantém 3 últimos)
- `mask_cpf()` - Mascara CPF
- `mask_rg()` - Mascara RG
- `mask_email()` - Mascara emails
- `mask_phone()` - Mascara telefones
- `mask_cep()` - Mascara CEPs
- `mask_all_pii()` - Mascara todos os tipos
- `mask_pii()` - Mascaramento seletivo

#### Executar Demonstração

```bash
# Testes completos
python -m simple_rag.utils.test_data_masking

# Demonstração interativa
python examples/demo_final_masking.py

# Exemplo com arquivos de anamnese
python examples/mask_anamnese_example.py
```

#### Integração com Pipeline RAG

```python
from simple_rag.utils import mask_all_pii

def process_medical_document(file_path: str) -> str:
    """Processa documento mascarando dados sensíveis antes de indexar"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Aplicar mascaramento
    masked_content = mask_all_pii(content)

    # Continuar com pipeline RAG (chunking, embedding, etc.)
    return masked_content
```

#### Documentação Completa

Para mais detalhes sobre o módulo de mascaramento, consulte:
- `GUIA_RAPIDO_MASCARAMENTO.md` - Guia rápido de uso
- `RESUMO_MASCARAMENTO_FINAL.md` - Documentação completa
- `examples/NOVAS_FUNCIONALIDADES.md` - Detalhes das funcionalidades

### Arquitetura e Fluxo do Sistema

```mermaid
flowchart TD
    A[📄 Documentos Médicos] --> B[🔒 Mascaramento de PII]
    B --> C[✂️ Chunking]
    C --> D[🧮 Embeddings]
    D --> E[(🗄️ VectorStore ChromaDB)]

    F[👤 Query do Usuário] --> G[🤖 LLM Ollama]
    G -->|Precisa Contexto?| H[🔍 Retriever Tool]
    H --> E
    E -->|Documentos Relevantes| H
    H --> G
    G -->|Usa Calculadora?| I[🔢 Calculator Tools]
    I --> G
    G --> J[💬 Resposta Estruturada]

    style B fill:#ff6b6b
    style E fill:#4ecdc4
    style G fill:#95e1d3
    style J fill:#f7dc6f
```

**Fluxo de Processamento:**

1. **Indexação (Offline)**:
   - 📄 Documentos são carregados do diretório `data/anamnese/`
   - 🔒 Dados sensíveis são mascarados (CPF, RG, nomes, etc.)
   - ✂️ Textos são divididos em chunks
   - 🧮 Embeddings são gerados para cada chunk
   - 🗄️ Chunks são armazenados no ChromaDB

2. **Consulta (Online)**:
   - 👤 Usuário faz uma pergunta
   - 🤖 LLM analisa e decide quais ferramentas usar
   - 🔍 Retriever busca documentos relevantes no VectorStore
   - 🔢 Calculator executa cálculos se necessário
   - 💬 LLM gera resposta estruturada com contexto recuperado

## Configuração

### Configurar via .env

Todas as configurações estão centralizadas no arquivo `.env`:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TEMPERATURE=0

# Embedding Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Document Processing
DATA_DIR=./data/anamnese
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Retrieval
RETRIEVAL_K=4
RETRIEVAL_TYPE=similarity

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

### Cenários Comuns de Configuração

**Ollama rodando localmente (mesma máquina):**

```env
OLLAMA_BASE_URL=http://localhost:11434
```

**Ollama rodando em outra máquina na rede:**

```env
OLLAMA_BASE_URL=http://192.168.1.100:11434
```

**Ollama rodando em container Docker:**

```env
OLLAMA_BASE_URL=http://host.docker.internal:11434  # Windows/Mac
# ou
OLLAMA_BASE_URL=http://172.17.0.1:11434  # Linux
```

**Testar conexão com Ollama:**

```bash
curl http://localhost:11434/api/version
```

### Modelos Alternativos

Edite o `.env` para usar outro modelo:

```env
OLLAMA_MODEL=llama3.2:3b  # Modelo menor e mais rápido
# ou
OLLAMA_MODEL=mistral:7b   # Alternativa do Mistral AI
# ou
OLLAMA_MODEL=gemma2:9b    # Modelo do Google
```

Certifique-se de baixar o modelo antes:

```bash
ollama pull <nome-do-modelo>
```

### Modificar o Comportamento do Agente

Edite a variável `system_message` no `.env` ou diretamente em `simple_rag/config/config.py`:

```env
SYSTEM_MESSAGE="Você é um assistente médico especializado em anamnese..."
```

Ou edite diretamente em `simple_rag/agent/agent.py` (linha 51):

```python
SystemMessage(content=settings.system_message)
```

### Ajustar Parâmetros de Busca

Edite o `.env`:

```env
RETRIEVAL_K=4              # Número de documentos retornados
RETRIEVAL_TYPE=similarity  # Tipo de busca
```

### Modificar Chunking dos Documentos

Edite o `.env`:

```env
CHUNK_SIZE=1000      # Tamanho dos chunks
CHUNK_OVERLAP=200    # Overlap entre chunks
```

## Adicionando Novos Documentos

1. Coloque arquivos `.txt` no diretório `data/anamnese/`
2. Use encoding UTF-8
3. Os documentos serão carregados automaticamente na próxima execução

**Nota**: O projeto atualmente suporta apenas arquivos `.txt` com encoding UTF-8.

## Troubleshooting

### Erro: ImportError ou problemas com dependências

Se você encontrar erros como `ImportError: cannot import name '_imaging' from 'PIL'` ou
`Could not import sentence_transformers`, certifique-se de usar o ambiente virtual do Poetry:

```bash
# SEMPRE use poetry run ou ative o shell do Poetry
poetry run python -m simple_rag.main

# Ou ative o shell primeiro
poetry shell
python -m simple_rag.main
```

**Problema:** Executar `python -m simple_rag.main` diretamente pode usar o Python do sistema ao invés do ambiente
virtual, causando conflitos de dependências.

**Solução:** Use `poetry run` ou ative o shell com `poetry shell` primeiro.

### Erro: ModuleNotFoundError

```bash
# Execute a partir do diretório raiz
cd processamento-linguagem-natural-puc-minas
poetry run python -m simple_rag.main
```

### Erro de conexão com Ollama

Verifique se:

1. O servidor Ollama está rodando: `ollama serve`
2. O endereço está correto no `.env`
3. O modelo está baixado: `ollama list`

```bash
# Verificar se Ollama está rodando
curl http://localhost:11434/api/version

# Iniciar se necessário
ollama serve
```

### Modelo não encontrado

```bash
# Listar modelos instalados
ollama list

# Baixar modelo
ollama pull llama3.1:8b
```

### Diretório de dados não encontrado

Verifique o `.env`:

```env
DATA_DIR=./data/anamnese  # Caminho correto
```

### Validar Configuração

```python
from simple_rag.config import config

try:
    config.validate()
    print("✓ Configuração válida!")
except ValueError as e:
    print(f"✗ Erro: {e}")
```

## Logging

O sistema usa logs em dois níveis:

- **Console**: INFO e acima (formatação simples)
- **Arquivo**: DEBUG e acima (formatação detalhada com timestamps)

Para ajustar o nível de log, edite o `.env`:

```env
LOG_LEVEL=DEBUG  # Mais verboso
LOG_LEVEL=INFO   # Padrão
LOG_LEVEL=WARNING  # Apenas avisos e erros
```

## Dependências Principais

- **langchain** - Framework principal para LLM
- **langchain-ollama** - Interface com modelos Ollama
- **langgraph** - Orquestração de grafos de agentes
- **langchain-huggingface** - Embeddings
- **sentence-transformers** - Modelos de embedding pré-treinados
- **langchain-community** - Loaders de documentos
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## Documentação Adicional

### Documentação Técnica

- **[DOCUMENTATION.md](./DOCUMENTATION.md)** - Documentação completa com:
  - Diagrama de arquitetura do sistema
  - Diagramas de fluxo de execução
  - Explicação detalhada de cada componente
  - Conceitos técnicos (embeddings, similaridade, vectorstore)
  - Métricas e performance

- **[NOTEBOOK_EXPLANATION.md](./NOTEBOOK_EXPLANATION.md)** - Explicação do notebook `rag.ipynb`:
  - Passo a passo de cada célula
  - Conceitos de embeddings e busca vetorial
  - Exemplos práticos com scores de similaridade
  - Exercícios para experimentação

### Outras Documentações

- **[data/README.md](./data/README.md)** - Estrutura e formato dos dados (se existir)
- **[Docker README](./DOCKER_README.md)** - Instruções para execução com Docker

## Desenvolvimento

Este projeto utiliza **Python 3.13** e aproveita suas novas funcionalidades:

### Recursos do Python 3.13 utilizados

- **Better error messages** - Mensagens de erro mais claras e precisas
- **Improved typing** - Melhor suporte para type hints
- **Performance improvements** - ~15% mais rápido que Python 3.12
- **New REPL** - Interface interativa melhorada

### Ferramentas de desenvolvimento

Para desenvolvimento, instale as dependências adicionais:

```bash
# Usando Poetry - instalar todas as dependências incluindo dev
poetry install --with dev

# Ou usando pip com dependências opcionais
pip install -e ".[dev]"
```

Ferramentas incluídas:

- `pytest` - Testes automatizados
- `black` - Formatação de código (configurado para Python 3.13)
- `ruff` - Linting ultra-rápido (target: py313)
- `mypy` - Type checking (python_version = 3.13)
- `pydocstring` - Validação de docstrings

### Git Hooks

O projeto possui um pre-commit hook que executa automaticamente:

1. **Black** - Formatação de código
2. **Ruff** - Linting e correções automáticas
3. **Mypy** - Type checking
4. **Pydocstring** - Validação de docstrings

O hook é executado automaticamente antes de cada commit.

Consulte [docs/desenvolvimento.md](./docs/desenvolvimento.md) para mais detalhes.

## Comandos Úteis

### Gerenciamento de Dependências com Poetry

```bash
# Adicionar nova dependência de produção
poetry add <package>

# Adicionar dependência de desenvolvimento
poetry add --group dev <package>

# Atualizar dependências
poetry update

# Ver dependências instaladas
poetry show

# Ver dependências desatualizadas
poetry show --outdated

# Remover dependência
poetry remove <package>
```

### Executar Aplicação

```bash
# Executar aplicação
poetry run python -m simple_rag.main

# Ou ativar ambiente virtual primeiro
poetry shell
python -m simple_rag.main

# Testar módulos individuais
poetry run python -m simple_rag.utils.vectorstore
poetry run python -m simple_rag.agent.agent

# Verificar configuração
poetry run python -c "from simple_rag.config.config import settings; print(f'Modelo: {settings.ollama_model}')"
```

### Ferramentas de Desenvolvimento

```bash
# Formatar código
poetry run black simple_rag/

# Linting
poetry run ruff check simple_rag/

# Linting com auto-fix
poetry run ruff check --fix simple_rag/

# Type checking
poetry run mypy simple_rag/

# Executar testes
poetry run pytest

# Executar testes com coverage
poetry run coverage run -m pytest
poetry run coverage report
```

## Licença

[Especifique a licença do projeto]

## Contribuição

[Instruções para contribuição, se aplicável]
